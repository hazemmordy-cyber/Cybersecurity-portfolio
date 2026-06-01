#  SOC Monitoring & Log Analysis Lab

> Simulating a Security Operations Center environment — from log collection to incident detection and response.

---

##  Project Overview

| Aspect | Details |
|--------|---------|
| **Role** | Junior SOC Analyst |
| **Objective** | Deploy a SIEM, collect logs from Windows/Linux, detect a brute-force attack, and document an incident |
| **Environment** | Wazuh SIEM (Manager + Agent), Kali Linux (attacker simulation), Windows 11 (target) |
| **Tools** | Wazuh, Elastic Stack, Windows Event Viewer, Linux auth logs, Wireshark |
| **Status** |  In Progress |

---

##  Lab Architecture

┌─────────────────────────────────────────────────────────────────┐
│ SOC LABORATORY ENVIRONMENT │
├─────────────────────────────────────────────────────────────────┤
│ │
│ ┌──────────────┐ ┌──────────────┐ ┌─────────────┐ │
│ │ Wazuh │◄────►│ Windows │ │ Kali │ │
│ │ Manager │ │ 11 Agent │ │ (Attacker) │ │
│ │ (SIEM) │ │ (Target) │ │ │ │
│ └──────────────┘ └──────────────┘ └──────┬──────┘ │
│ │ │ │
│ │ │ │
│ ▼ ▼ │
│ ┌──────────────┐ ┌──────────────┐ ┌─────────────┐ │
│ │ Elastic │ │ Logstash │ │ Brute │ │
│ │ Search │◄────►│ (Parsing) │ │ Force │ │
│ │ & Kibana │ │ │ │ Attack │ │
│ └──────────────┘ └──────────────┘ └─────────────┘ │
│ │
│ Internal Network (192.168.3.0/24) │
└─────────────────────────────────────────────────────────────────┘


---

##  Objectives

- Deploy **Wazuh** (open-source SIEM) in a virtual environment
- Install Wazuh agent on **Windows 11** to collect security logs
- Simulate a **brute-force attack** (RDP/SSH) from Kali Linux
- Detect the attack via Wazhu rules and **Windows Event IDs**
- Analyze logs from **Windows Event Viewer** and **Linux auth logs**
- Correlate events across multiple sources
- Write a professional **Incident Report** (timeline, IOCs, MITRE mapping)

---

##  Project Structure

02-soc-monitoring-lab/
├── README.md # This landing page
├── environment/
│ └── setup-guide.md # Step-by-step installation of Wazuh + agents
├── logs/
│ ├── windows-events.md # Key Event IDs and analysis examples
│ └── linux-logs.md # auth.log, syslog analysis
├── traffic/
│ └── wireshark-analysis.md # Capturing and inspecting attack traffic
├── incident-scenario/
│ ├── brute-force-detection.md # How the attack was detected
│ └── incident-report.md # Full incident response documentation
└── screenshots/ # Evidence from Wazuh, Kibana, Event Viewer


---

##  Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Wazuh** | SIEM platform (manager, agents, rules) |
| **Elastic Stack** | Storage, search, visualization (Kibana) |
| **Windows 11** | Target system with Wazuh agent |
| **Kali Linux** | Attacker machine (Hydra, Nmap) |
| **Wireshark** | Network traffic inspection |
| **Event Viewer** | Windows native log analysis |
| **/var/log/auth.log** | Linux authentication logs |

---

##  What We'll Detect

| Attack Type | Detection Method | Key Indicators |
|-------------|------------------|----------------|
| RDP Brute Force | Windows Event ID 4625 (failed logon) | Multiple failures from same source IP |
| SSH Brute Force | Linux auth.log | Failed password attempts, user enumeration |
| Port Scanning | Wazuh active response / Firewall logs | Rapid connection attempts to multiple ports |

---

##  SOC Skills Demonstrated

| Skill | How It's Proven |
|-------|------------------|
| **Log Analysis** | Manual review of Windows/Linux logs |
| **SIEM Deployment** | Wazuh installation and configuration |
| **Rule Writing** | Custom detection rules (if applicable) |
| **Event Correlation** | Connecting Wazuh alerts with raw logs |
| **Incident Response** | Full incident report with timeline, IOCs, MITRE |
| **Documentation** | Professional write-up for each phase |

---

##  Key Resources

- [Wazuh Documentation](https://documentation.wazuh.com/)
- [Windows Security Event IDs](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)

---

##  Related Projects

- [Enterprise Network Discovery Lab](../01-enterprise-network-discovery-lab/README.md)

---

*Last Updated: June 2026*
