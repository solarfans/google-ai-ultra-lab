# Cloudflare Infrastructure Knowledge & Integration Guide

> 本文档由 ChatGPT Seat A 历史资产梳理与 MacBook 本地实时核验整合蒸馏而成，为 `google-ai-ultra-lab` 及 AI OS 跨平台联动提供统一的 Cloudflare 基础设施指引与权威凭据接入方式。严禁在代码或 Git 提交中包含任何明文 Key。

---

## 1. 账号与认证凭据 (Authentication)

### 1.1 核心身份信息
- **Cloudflare 登录邮箱**：`wowsengkang@gmail.com`（注意包含 `wows`，非 `wow`）
- **Cloudflare Account ID**：`b4f8e703a45f54ba7a89684cef863016`（Name: `Wowsengkang@gmail.com's Account`）
- **主域名 Zone**：`solarfans.cc`（Zone ID: `abc0748a77f3821f392c694e7add915b`，Status: `active`）

### 1.2 本机凭据存储
凭据安全保存在 MacBook 本机受保护路径：
```bash
~/.hermes/.env
```
包含以下关键环境变量：
- `CLOUDFLARE_GLOBAL_API`：Global API Key（最高权限，用于 Tunnel、DNS、Workers、WAF、KV 管理）
  - HTTP 请求头格式：
    ```http
    X-Auth-Email: wowsengkang@gmail.com
    X-Auth-Key: <从 ~/.hermes/.env 读取>
    ```
- `CLOUDFLARE_API`：Scoped API Token
  - HTTP 请求头格式：
    ```http
    Authorization: Bearer <从 ~/.hermes/.env 读取>
    ```
  - *注：Scoped Token 在部分管理接口（如特定 Workers/Tunnel 修改）可能权限不足，依 AI OS Global Canon D-042 规则，优先直接使用 Global API Key。*

### 1.3 权威 Python 认证代码复用
在 `solarfans/ai-agent-lab-canon` 中已有经过生产验收的认证加载脚本：
`scripts/agentops/cloudflare_global_auth.py`

**快速调用示例**：
```python
import os, urllib.request, json
from pathlib import Path

def get_cf_auth():
    env_lines = (Path.home() / ".hermes" / ".env").read_text().splitlines()
    env = dict(l.split("=", 1) for l in env_lines if "=" in l and not l.strip().startswith("#"))
    email = "wowsengkang@gmail.com"
    key = env.get("CLOUDFLARE_GLOBAL_API", "").strip("\"'")
    return {
        "X-Auth-Email": email,
        "X-Auth-Key": key,
        "Content-Type": "application/json"
    }
```

---

## 2. 现有域名与资产拓扑 (Asset Mapping)

| 子域名 / 接入点 | 承载基础设施 | 对应本地服务 / 后端 | 核心职责与仓库 |
| :--- | :--- | :--- | :--- |
| `solarfans.cc`<br>`www.solarfans.cc` | **Cloudflare Pages**<br>(`solarfans-ai-lab.pages.dev`) | 静态前端 / 生产部署 | 官方门户网站。<br>源码仓库: `solarfans/solarfans-ai-lab` |
| `ops.solarfans.cc` | **Cloudflare Access + Worker + KV** | 本机 AgentOps SQLite 投影 | 私有运维看板，需要 One-Time PIN 邮箱校验。<br>规范: `ai-agent-lab-canon#50` |
| `mcp.solarfans.cc` | **Cloudflare Tunnel (Remote)**<br>(ID: `326dc18f-...`) | 本机 `127.0.0.1:8765` | ALB Track B ChatGPT MCP 穿透网关。<br>守护进程: `cc.solarfans.ai-local-bridge.track-b-cloudflared` |
| `llm.solarfans.cc` | **Cloudflare Tunnel (Remote)**<br>+ Edge WAF API Key | 本机 `127.0.0.1:11434` (Ollama) | 本地无审查大模型 (DeepSeek-V4-Pro / Qwen3.5 9B) 全球穿透接入点，供 iPhone/Chatbox 等全终端使用。<br>- 鉴权方式: HTTP Bearer Token<br>- 凭据读取: `CF_WAF_BEARER_KEY` (存入 `~/.hermes/.env`)<br>- 边缘防护: 403 阻断无 Key 扫描 |
| `hooks.solarfans.cc` | **Cloudflare Tunnel** + Edge WAF | 本机 Webhook 接收端口 | 自动化事件回调与告警。带有签名验证 WAF 规则。 |
| `instabox-direct-mcp-v1.wowsengkang.workers.dev` | **Cloudflare Workers** + KV | 边缘 Serverless | InstaBox Direct MCP 托管。<br>源码仓库: `solarfans/instabox-ops` |

---

## 3. 本地穿透守护程序与 Tunnel 管理

### 3.1 活跃 Tunnel 状态
- **Tunnel 名称**：`ai-local-bridge-track-b`
- **Tunnel ID**：`326dc18f-e2f0-41d2-9216-a79908ad7e1e`
- **公网 CNAME 目标**：`326dc18f-e2f0-41d2-9216-a79908ad7e1e.cfargotunnel.com`
- **管理模式**：Cloudflare Remote Managed（可通过 Cloudflare API 直接下发 `ingress` 规则，无需频繁重启或手改本地文件）
- **本地 LaunchAgent**：
  ```bash
  ~/Library/LaunchAgents/cc.solarfans.ai-local-bridge.track-b-cloudflared.plist
  ```
  该守护进程在系统后台随 MacBook 开机常驻，多域名共用此单管道实现多端口反向代理。

---

## 4. Google AI Ultra 业务联动场景

1. **Colab 远程渲染任务进度直报**：
   - 当 Colab G4 (Blackwell) 执行耗时视频/音频批处理时，可通过 `https://hooks.solarfans.cc` 或 Cloudflare Worker 直接向 MacBook 节点回传任务状态，无需持有长链接。
2. **轻量模型边缘与本地混合路由**：
   - 复杂推理任务与生图调度由 Google Colab GPU / 本地 Ollama 承接，外围移动端（iPhone / iPad Chatbox）统一通过 `https://llm.solarfans.cc/v1` 访问。
3. **安全准则**：
   - 所有暴露于公网的接口，必须在 Cloudflare Edge 配置 WAF Custom Rule 或 Access 白名单保护，禁止裸开无鉴权端口。
