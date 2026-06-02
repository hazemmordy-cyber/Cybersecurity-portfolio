# Hazem Mordey Galal

**Computer Science Student | Cybersecurity Track**

> Building hands-on security experience through enterprise-style projects and technical documentation.

---

##  About Me

I am a Computer Science student specializing in Cybersecurity with a strong interest in:
- Network security and reconnaissance
- Security operations (SOC) and log analysis
- Security automation with Python

This portfolio demonstrates practical cybersecurity labs in isolated environments — not just theory.

---

##  Technical Areas

| Category | Skills |
|----------|--------|
| **Networking** | TCP/IP, Subnetting, VLANs, Routing |
| **Security** | Nmap, Reconnaissance, Attack Surface Analysis, Firewall Behavior |
| **Monitoring** | Wireshark, Windows Event Logs, Linux Logs, Wazuh SIEM |
| **OS** | Kali Linux, Windows 11, Ubuntu (Wazuh Server) |
| **Virtualization** | VirtualBox, Internal Networking |
| **Automation** | Python (socket, argparse, JSON/CSV), Security Tooling |

---

##  Portfolio Projects

### 1.  Enterprise Network Discovery & Attack Surface Mapping

**Status:**  Complete

**What I did:**
- Simulated internal reconnaissance in isolated virtual network (VirtualBox)
- Discovered active hosts, enumerated services, analyzed firewall behavior
- Documented findings with security interpretation and risk matrix
- **Key insight:** "No open ports" is still a finding – it tells us the firewall is working

**Skills:** Nmap, Kali Linux, Windows 11, ARP, Firewall Analysis

 [View Project →](https://github.com/hazemmordy-cyber/Cybersecurity-portfolio/blob/main/projects/01-enterprise-network-discovery-lab/README%20.md)

---

### 2.  SOC Monitoring & Log Analysis Lab

**Status:**  Complete

**What I did:**
- Deployed Wazuh SIEM (manager + agent) on isolated network
- Collected Windows Security Events (Event ID 4625 – failed logons)
- Simulated RDP brute‑force attack using Kali (hydra)
- Triggered Wazuh rule 5710 (10+ failures/60s) and documented incident
- Produced full incident report with timeline, IOCs, and MITRE mapping

**Skills:** Wazuh, Windows Event Logs, Attack simulation, Incident response, SIEM correlation

 [View Project →](./projects/02-soc-monitoring-lab/README.md)

---

### 3.  Python Security Automation – Port Auditor

**Status:**  Complete

**What I did:**
- Built a lightweight TCP port scanner with banner grabbing using Python standard library (socket, argparse, json, csv)
- Implemented structured logging to JSON and CSV with timestamps
- Scanned the lab’s Windows 11 target (192.168.3.12) to verify open ports
- Designed for isolated lab environments, demonstrating automation and data serialisation

**Skills:** Python (socket programming), CLI arguments, Data serialisation (JSON/CSV), Network automation

 [View Project →](./projects/03-python-security-auditor/README.md)

---

##  Lab Environment

| Tool | Purpose |
|------|---------|
| VirtualBox | Virtualization platform |
| Kali Linux | Security analysis & attack simulation |
| Windows 11 | Target system |
| Ubuntu (Wazuh Server) | SIEM platform (Project 2) |
| Internal Network | Isolated lab environment (cyber-lab) |
| Wireshark | Traffic analysis (optional) |

![Network Topology](./assets/network-topology.png)

---

##  Current Objective

Building practical, documentable cybersecurity experience through enterprise-style projects that demonstrate:
- **Execution** (can I do it?)
- **Documentation** (can I explain it?)
- **Interpretation** (do I understand the risk?)
- **Automation** (can I script it?)

---

##  Progress

| Project | Status | Completion |
|---------|--------|------------|
| Enterprise Network Discovery |  Complete | 100% |
| SOC Monitoring & Log Analysis |  Complete | 100% |
| Python Security Port Auditor |  Complete | 100% |

---

##  Links

-  [LinkedIn](https://www.linkedin.com/in/hazem-mordy-115763353/)
-  [GitHub Profile](https://github.com/hazemmordy-cyber)

---

*Last Updated: June 2026*
