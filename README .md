# 🌐 Enterprise Network Discovery & Attack Surface Analysis

> Simulating real-world internal reconnaissance — from host discovery to risk interpretation.

---

## 📋 Project Overview

| Aspect | Details |
|--------|---------|
| **Role** | Junior Security Analyst |
| **Objective** | Identify active hosts, enumerate services, map attack surface in enterprise-like environment |
| **Environment** | Isolated Virtual Network (VirtualBox) |
| **Tools** | Nmap, Kali Linux, Windows 11 |
| **Status** | ✅ Complete |

---

## 🏗️ Network Architecture

![Network Architecture Diagram](./diagrams/network-architecture.png)



---

## 🎯 Objectives

- Simulate internal reconnaissance phase of enterprise security assessment
- Discover active hosts without prior knowledge of the network
- Enumerate services and identify exposed attack surface
- Document findings with **security interpretation**, not just raw output
- Demonstrate analyst-level thinking (not just tool execution)

---

## 📁 Project Structure

enterprise-network-discovery-1/
├── README.md # This landing page
├── screenshots/ # Evidence of execution
├── diagrams/ # Network architecture
├── raw-results/ # Nmap outputs
├── reports/ # Detailed analysis
│ └── attack-surface-analysis.md
└── findings/ # Risk assessment
└── service-risk-matrix.md


---

## 🔍 Methodology

### Phase 1: Discovery
- Identify IP addresses (`ipconfig` / `ip addr`)
- Test connectivity (ICMP ping)
- Sweep network for live hosts (`nmap -sn`)

### Phase 2: Enumeration
- Service version detection (`nmap -sV -O`)
- Targeted Windows port scan (135,139,445,3389)
- UDP top ports scan (`--top-ports 100`)

### Phase 3: Analysis
- Map exposed services
- Categorize risk levels
- Interpret findings in enterprise context

---

## 📊 Key Findings

| Finding | Result |
|---------|--------|
| Active Host | ✅ 192.168.3.12 (Windows 11) |
| ICMP (ping) | ❌ Blocked by firewall |
| TCP Ports (1000) | 🚫 All filtered |
| UDP Ports (100) | ⚠️ Open/Filtered (inconclusive) |
| Windows Services (135,139,445,3389) | 🚫 All filtered |
| OS Fingerprint | ❌ Inconclusive (firewall interference) |

---

## 🛡️ Security Interpretation

**What this means in an enterprise context:**

1. **Restrictive firewall is working** — No external attack surface exposed
2. **ARP visibility is unavoidable** — Hosts must respond to ARP; this is why monitoring matters
3. **"No results" is a finding** — Filtered ports indicate security controls are functioning
4. **UDP uncertainty** — Requires further investigation or network-level logging

**Risk Assessment: LOW** — The target demonstrates a strong security baseline.

---

## 📸 Evidence

| Screenshot | Description |
|------------|-------------|
| [ipconfig-windows.png](./screenshots/ipconfig-windows.png) | Windows IP configuration |
| [ping-fail-kali.png](./screenshots/ping-fail-kali.png) | Failed ICMP from Kali → Windows |
| [nmap-sn-sweep.png](./screenshots/nmap-sn-sweep.png) | Host discovery via ARP |
| [nmap-sV-O-results.png](./screenshots/nmap-sV-O-results.png) | Service enumeration (filtered ports) |

---

## 📈 Risk Matrix (Summary)

| Service | Port | State | Risk Level | Reason |
|---------|------|-------|------------|--------|
| msrpc | 135 | Filtered | Low | Blocked by firewall |
| netbios-ssn | 139 | Filtered | Low | Blocked by firewall |
| microsoft-ds | 445 | Filtered | Low | SMB properly restricted |
| ms-wbt-server | 3389 | Filtered | Low | RDP access protected |
| UDP Services | Top 100 | Open/Filtered | Low-Medium | Requires investigation |

📄 [Full Risk Matrix →](./findings/service-risk-matrix.md)

---

## 📝 Reports

- [Attack Surface Analysis Report](./reports/attack-surface-analysis.md) — Comprehensive documentation with methodology, findings, and recommendations

---

## 🧠 Lessons Learned

1. **Documentation separates analysts from technicians** — Interpreting results is the core skill
2. **Enterprise context changes everything** — Same scan, different meaning based on environment
3. **Firewall behavior is a finding** — Filtered ports tell a story about security controls
4. **Visuals matter** — One architecture diagram explains more than paragraphs of text

---

## 🚀 Future Enhancements

- [ ] Add automated scanning script (Python)
- [ ] Expand to multi-host enterprise simulation
- [ ] Introduce logging and SIEM monitoring layer
- [ ] Create video walkthrough of assessment process

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| Nmap 7.95 | Port scanning, service detection, OS fingerprinting |
| Ping (ICMP) | Connectivity testing |
| VirtualBox | Internal network isolation |
| Windows 11 | Target system |
| Kali Linux | Security analysis platform |

---

## 🔗 Related Projects

- [SOC Monitoring Lab](../02-soc-monitoring-lab/README.md) *(Coming Soon)*
- [Python Security Tools](../03-python-security-tools/README.md) *(Coming Soon)*

---

## 📧 Contact

**Hazem Mordy** — Junior Security Analyst

📁 [GitHub Portfolio](https://github.com/hazemmordy-cyber/Cybersecurity-portfolio)

---

*Last Updated: June 2026*
