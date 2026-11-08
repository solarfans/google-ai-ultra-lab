# Google Cloud 双机接力私人 VPN 架构与运维手册

**部署日期**：2026-11-08 SGT  
**验收状态**：`DEPLOYED / CONNECTIVITY_VERIFIED / US_AND_TW_IP_VERIFIED / GUARDRAILS_ACTIVE`  
**适用场景**：中国大陆差旅期间，为 Owner 及家人（MacBook + iPhone 多设备并发）提供低延迟、抗封锁的独享美国原生 IP 与台湾备用直连通道。

---

## 1. 架构拓扑与选型理由

针对中国大陆晚高峰跨太平洋直连美西延迟高（200ms+）、丢包严重的问题，本方案采用 **「台湾低延迟入口 ➡️ Google 全球私有骨干内网（VPC） ➡️ 美西原生出口」** 双机接力架构，同时在台湾入口机开放第 2 端口提供台湾本地直连备用线路：

```text
[中国大陆/海外客户端: MacBook & iPhone (Hiddify)]
        │
        ├─(端口 8443: VLESS + REALITY + Vision)─► [node-tw-entry-01 (台湾 asia-east1-b)]
        │                                                │
        │                                   (Google 跨洋内网 VPC: 10808)
        │                                                ▼
        │                                        [node-us-exit-01 (美西 us-west1-b)]
        │                                                │
        │                                                ▼
        │                                  🇺🇸 独享美国原生出口 (35.247.83.37, Oregon)
        │
        └─(端口 2053: VLESS + REALITY + Vision)─► [node-tw-entry-01 (台湾 asia-east1-b)]
                                                         │
                                                         ▼
                                           🇹🇼 独享台湾原生出口 (35.194.245.4, Taipei)
```

---

## 2. 云端资源清单（非敏感配置）

- **Google Cloud Project ID**：`project-665ac784-237e-4a71-ad0`
- **关联结算账户**：`My Billing Account`（由 Free Trial US$300 / SGD 384.83 与 Google AI Ultra 月度 US$100 / SGD 128.28 Credits 覆盖）

| 资源名称 | 类型 / 规格 | 区域 / 可用区 | 网络配置 | 角色与说明 |
| :--- | :--- | :--- | :--- | :--- |
| `node-tw-entry-01` | VM (`e2-micro`, Debian 12, 10GB `pd-standard`) | `asia-east1-b` (台湾) | 静态公网 IP: `35.194.245.4` (`ip-node-tw-01`)<br>内网 IP: `10.140.0.2` | 入口跳板机 + 台湾直连出口（带 `proxy-entry` 标签） |
| `node-us-exit-01` | VM (`e2-micro`, Debian 12, 10GB `pd-standard`) | `us-west1-b` (美国俄勒冈) | 公网出口 IP: `35.247.83.37` | 美西 AI 专线落地出口机（命中 GCP Free Tier 区域） |
| `fw-allow-proxy-in` | VPC 防火墙入站规则 | Global (`proxy-entry`) | `tcp:8443,2053`, `udp:8443,2053` | 仅对台湾入口机放行 VLESS REALITY 服务端口 |
| `fw-allow-internal-xray` | VPC 防火墙内部规则 | Global (`10.128.0.0/9`) | `tcp:10808`, `udp:10808` | 仅允许 GCP 内部 VPC 子网访问美西落地转发端口 |

---

## 3. 服务端软件与费用安全护栏

1. **核心协议栈**：
   - 服务端程序：`Xray-core v26.1.23`（systemd 服务名：`xray.service`，开机自启）
   - 外部接入协议：`VLESS + XTLS-RPRX-Vision + REALITY`（伪装 SNI：`www.apple.com:443`，指纹：`chrome`）
   - 内核网络优化：已启用 TCP BBR 拥塞控制与大缓冲区优化（`/etc/sysctl.d/99-bbr-highspeed.conf`）
2. **后台遥测黑洞（防偷跑流量）**：
   - Xray 路由层已配置 `domain:play.googleapis.com` 指向 `blackhole` 出站，阻断客户端后台无意义诊断日志上传。
3. **250GB 月度物理熔断锁**：
   - 台湾入口机已部署 `/usr/local/bin/traffic_guard.sh` 及定时任务 `/etc/cron.d/xray-traffic-guard`；
   - 每 10 分钟通过 `vnstat` 检查当月出站流量，一旦超过 **250GB**（约消耗 US$60~65 赠金，远低于每月 US$100 赠金上限）自动执行 `systemctl stop xray`，并于次月 1 日 00:05 自动恢复启动。
4. **账单防扣卡底线**：
   - 账户保持 **Free Trial / Credits 抵扣模式**，未点击升级全额付费账户（Paid Account），从机制上杜绝超额扣除信用卡现金。

---

## 4. 端到端实测验收记录（2026-11-08）

- **服务端配置校验**：`xray run -test -config /usr/local/etc/xray/config.json` 返回 `Configuration OK`。
- **链路 1（🇺🇸 GCP-美西专线，`35.194.245.4:8443`）**：
  - `ipinfo.io` 实测返回：`35.247.83.37`（`The Dalles, Oregon, US`，`AS396982 Google LLC`）
  - MacBook Hiddify & iPhone Hiddify 均连接成功。
- **链路 2（🇹🇼 GCP-台湾直连，`35.194.245.4:2053`）**：
  - `ipinfo.io` 实测返回：`35.194.245.4`（`Taipei, Taiwan, TW`，`AS396982 Google LLC`）
  - MacBook Hiddify & iPhone Hiddify 均连接成功。
- **密钥与隐私保护**：UUID、REALITY 私钥/公钥、ShortId 及客户端导入二维码仅保存在本地私有环境，**未写入本仓库**。

---

## 5. 日常运维常用指令（在 Google Cloud Shell 中执行）

### 查看服务运行状态
```bash
gcloud compute ssh node-tw-entry-01 --zone=asia-east1-b --quiet -- "sudo systemctl status xray"
gcloud compute ssh node-us-exit-01 --zone=us-west1-b --quiet -- "sudo systemctl status xray"
```

### 重启 VPN 服务
```bash
gcloud compute ssh node-tw-entry-01 --zone=asia-east1-b --quiet -- "sudo systemctl restart xray"
gcloud compute ssh node-us-exit-01 --zone=us-west1-b --quiet -- "sudo systemctl restart xray"
```

### 查看当月流量统计
```bash
gcloud compute ssh node-tw-entry-01 --zone=asia-east1-b --quiet -- "vnstat -m"
```

### 暂停 / 启动机器（长期不出差时可停机省固定租金）
```bash
# 暂停机器
gcloud compute instances stop node-tw-entry-01 --zone=asia-east1-b
gcloud compute instances stop node-us-exit-01 --zone=us-west1-b

# 重新启动机器
gcloud compute instances start node-us-exit-01 --zone=us-west1-b
gcloud compute instances start node-tw-entry-01 --zone=asia-east1-b
```
