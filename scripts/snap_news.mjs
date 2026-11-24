#!/usr/bin/env node
/**
 * Zero-dependency headless Chrome CDP news/article screenshot + DOM keyword rect locator
 * (adapted from HeyChengC/wallstreet-explainer, MIT).
 *
 * Usage:
 *   node scripts/snap_news.mjs <jobs.json> [id1 id2 ...]
 *
 * jobs.json:
 *   [{"id":"burn","url":"https://...","find":["$280 billion by 2030"],"off":140,"to":"optional anchor text"}]
 *
 * Outputs:
 *   <jobs_dir>/docs/<id>.png   (1600x1000 @ 2x Retina)
 *   <jobs_dir>/docs/news.json  ({id: {url, title, h1, h1text, hits: [{k, tag, rects}]}})
 */

import { spawn } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';

const CHROME_BIN =
  process.env.CHROME_PATH ||
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

const BLOCKED_URL_PATTERNS = [
  '*doubleclick*',
  '*googlesyndication*',
  '*googletagservices*',
  '*adservice*',
  '*adsystem*',
  '*taboola*',
  '*outbrain*',
  '*criteo*',
  '*pubmatic*',
  '*rubicon*',
  '*onetrust*',
  '*cookielaw*',
  '*privacy-mgmt*',
  '*tinypass*',
];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function getFreePort() {
  return new Promise((resolve, reject) => {
    const srv = net.createServer();
    srv.unref();
    srv.on('error', reject);
    srv.listen(0, '127.0.0.1', () => {
      const { port } = srv.address();
      srv.close(() => resolve(port));
    });
  });
}

class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.nextId = 1;
    this.pending = new Map();
    this.listeners = new Map();
  }

  async connect() {
    await new Promise((resolve, reject) => {
      const ws = new WebSocket(this.wsUrl);
      this.ws = ws;
      ws.addEventListener('open', () => resolve(), { once: true });
      ws.addEventListener('error', (err) => reject(new Error(`CDP WS error: ${err.message || err.type}`)), { once: true });
      ws.addEventListener('message', (ev) => {
        const msg = JSON.parse(String(ev.data));
        if (msg.id !== undefined) {
          const p = this.pending.get(msg.id);
          if (p) {
            this.pending.delete(msg.id);
            if (msg.error) p.reject(new Error(`${msg.error.message} (${msg.error.code})`));
            else p.resolve(msg.result);
          }
        } else if (msg.method) {
          const list = this.listeners.get(msg.method);
          if (list) {
            for (const fn of [...list]) fn(msg.params || {}, msg.sessionId);
          }
        }
      });
    });
  }

  send(method, params = {}, sessionId = undefined) {
    const id = this.nextId++;
    const payload = { id, method, params };
    if (sessionId) payload.sessionId = sessionId;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify(payload));
    });
  }

  waitForEvent(method, sessionId, timeoutMs = 45000) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        off();
        resolve({ timedOut: true });
      }, timeoutMs);
      const handler = (params, sid) => {
        if (!sessionId || sid === sessionId) {
          clearTimeout(timer);
          off();
          resolve(params);
        }
      };
      const off = () => {
        const set = this.listeners.get(method);
        if (set) set.delete(handler);
      };
      if (!this.listeners.has(method)) this.listeners.set(method, new Set());
      this.listeners.get(method).add(handler);
    });
  }

  close() {
    for (const { reject } of this.pending.values()) {
      reject(new Error('CDP closed'));
    }
    this.pending.clear();
    if (this.ws && this.ws.readyState <= 1) {
      this.ws.close();
    }
  }
}

async function waitForWsEndpoint(port, timeoutMs = 15000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json/version`);
      if (res.ok) {
        const data = await res.json();
        if (data.webSocketDebuggerUrl) return data.webSocketDebuggerUrl;
      }
    } catch {}
    await sleep(150);
  }
  throw new Error(`Chrome CDP did not become ready on port ${port}`);
}

const STRIP_OVERLAYS_EXPR = `(() => {
  for (const e of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(e);
    if ((cs.position === 'fixed' || cs.position === 'sticky') && e.getBoundingClientRect().height > 40) {
      e.remove();
    }
  }
  document.documentElement.style.overflow = 'auto';
  document.body.style.overflow = 'auto';
  document.body.style.filter = 'none';
})()`;

async function evalInPage(cdp, sid, expression) {
  const res = await cdp.send(
    'Runtime.evaluate',
    { expression, returnByValue: true, awaitPromise: true },
    sid
  );
  if (res.exceptionDetails) {
    throw new Error(res.exceptionDetails.text || 'Runtime.evaluate failed');
  }
  return res.result ? res.result.value : undefined;
}

async function main() {
  const jobsArg = process.argv[2];
  if (!jobsArg) {
    console.error('Usage: node scripts/snap_news.mjs <jobs.json> [id1 id2 ...]');
    process.exit(2);
  }
  if (!fs.existsSync(CHROME_BIN)) {
    console.error(`Chrome not found at: ${CHROME_BIN}`);
    process.exit(2);
  }

  const jobsPath = path.resolve(jobsArg);
  const onlyIds = new Set(process.argv.slice(3));
  const jobs = JSON.parse(fs.readFileSync(jobsPath, 'utf8'));
  const outDir = path.join(path.dirname(jobsPath), 'docs');
  fs.mkdirSync(outDir, { recursive: true });
  const metaPath = path.join(outDir, 'news.json');
  const out = fs.existsSync(metaPath) ? JSON.parse(fs.readFileSync(metaPath, 'utf8')) : {};

  const port = await getFreePort();
  const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'snap-news-chrome-'));
  const chrome = spawn(
    CHROME_BIN,
    [
      '--headless=new',
      '--disable-gpu',
      '--no-first-run',
      '--no-default-browser-check',
      '--disable-background-networking',
      `--remote-debugging-port=${port}`,
      `--user-data-dir=${userDataDir}`,
      '--window-size=1600,1000',
      'about:blank',
    ],
    { stdio: 'ignore' }
  );

  let cdp = null;
  try {
    const wsUrl = await waitForWsEndpoint(port);
    cdp = new CDPClient(wsUrl);
    await cdp.connect();

    for (const j of jobs) {
      if (onlyIds.size > 0 && !onlyIds.has(j.id)) continue;
      const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
      const { sessionId: sid } = await cdp.send('Target.attachToTarget', {
        targetId,
        flatten: true,
      });

      try {
        await cdp.send('Page.enable', {}, sid);
        await cdp.send('Network.enable', {}, sid);
        await cdp.send('Runtime.enable', {}, sid);
        await cdp.send('Network.setBlockedURLs', { urls: BLOCKED_URL_PATTERNS }, sid);
        await cdp.send(
          'Network.setUserAgentOverride',
          {
            userAgent:
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            acceptLanguage: 'en-US,en;q=0.9',
          },
          sid
        );
        await cdp.send(
          'Emulation.setDeviceMetricsOverride',
          { width: 1600, height: 1000, deviceScaleFactor: 2, mobile: false },
          sid
        );

        const loadPromise = cdp.waitForEvent('Page.loadEventFired', sid, 45000);
        await cdp.send('Page.navigate', { url: j.url }, sid);
        await loadPromise;
        await sleep(j.waitMs ?? 1200);

        for (let k = 0; k < 2; k++) {
          try {
            await evalInPage(cdp, sid, STRIP_OVERLAYS_EXPR);
          } catch {}
          await sleep(300);
        }

        const off = Number.isFinite(j.off) ? j.off : 140;
        const toText = j.to ?? null;
        await evalInPage(
          cdp,
          sid,
          `((o, to) => {
            let el = document.querySelector('h1');
            if (to) {
              const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
              let n;
              while ((n = w.nextNode())) {
                if (n.textContent.includes(to)) { el = n.parentElement; break; }
              }
            }
            if (el) {
              window.scrollTo(0, Math.max(0, el.getBoundingClientRect().top + scrollY - o));
            }
          })(${JSON.stringify(off)}, ${JSON.stringify(toText)})`
        );

        await evalInPage(cdp, sid, 'document.fonts.ready');
        await sleep(400);
        try {
          await evalInPage(cdp, sid, STRIP_OVERLAYS_EXPR);
        } catch {}

        const words = Array.isArray(j.find) ? j.find : [];
        const info = await evalInPage(
          cdp,
          sid,
          `((words) => {
            const h = document.querySelector('h1');
            const hr = h ? h.getBoundingClientRect() : null;
            const hits = [];
            const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
            let n;
            while ((n = w.nextNode())) {
              for (const k of words) {
                const i = n.textContent.indexOf(k);
                if (i < 0) continue;
                const r = document.createRange();
                r.setStart(n, i);
                r.setEnd(n, i + k.length);
                const bb = r.getBoundingClientRect();
                if (bb.width > 0 && bb.top > 0 && bb.top < innerHeight) {
                  hits.push({
                    k,
                    tag: n.parentElement ? n.parentElement.tagName : '',
                    rects: [...r.getClientRects()].map((q) =>
                      [q.left, q.top, q.width, q.height].map((v) => Math.round(v * 10) / 10)
                    ),
                  });
                }
              }
            }
            return {
              title: document.title,
              h1: hr ? [hr.left, hr.top, hr.width, hr.height].map(Math.round) : null,
              h1text: h ? h.innerText : '',
              hits,
            };
          })(${JSON.stringify(words)})`
        );

        const shot = await cdp.send('Page.captureScreenshot', { format: 'png' }, sid);
        fs.writeFileSync(path.join(outDir, `${j.id}.png`), Buffer.from(shot.data, 'base64'));
        out[j.id] = { url: j.url, ...info };
        const blocked = /验证|captcha|apolog|blocked|access denied/i.test(
          (info.title || '') + (info.h1text || '')
        );
        console.log(
          j.id,
          blocked ? '[BLOCKED_SUSPECTED]' : '[OK]',
          '|',
          (info.h1text || info.title || '').slice(0, 80),
          '| hits:',
          info.hits.length
        );
      } finally {
        try {
          await cdp.send('Target.closeTarget', { targetId });
        } catch {}
      }
    }

    fs.writeFileSync(metaPath, JSON.stringify(out, null, 2));
  } finally {
    if (cdp) cdp.close();
    if (!chrome.killed) {
      chrome.kill('SIGTERM');
      await sleep(300);
      try {
        process.kill(chrome.pid, 0);
        chrome.kill('SIGKILL');
      } catch {}
    }
    fs.rmSync(userDataDir, { recursive: true, force: true });
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
