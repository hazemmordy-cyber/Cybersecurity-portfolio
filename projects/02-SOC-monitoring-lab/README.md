# 📊 SOC Monitoring & Log Analysis Lab

## 1. Executive Summary

This project simulates a real‑world Security Operations Center (SOC) monitoring scenario. Using the Wazuh SIEM platform, I collected and analysed security logs from a Windows 11 endpoint, detecting a simulated brute‑force attack against Remote Desktop Protocol (RDP). The lab demonstrates the full detection cycle: log collection → alert generation → event correlation → incident documentation.

**Key Outcome:** Successfully detected multiple failed login attempts (Event ID 4625) triggered by a brute‑force simulation, proving the ability to monitor, detect, and document malicious activity from a defensive perspective.

---

## 2. Environment Architecture

| Component | IP Address | Role |
|-----------|------------|------|
| Wazuh Server (Linux) | 192.168.3.20 | SIEM server – collects logs, generates alerts |
| Windows 11 (Target) | 192.168.3.12 | Endpoint with Wazuh agent – source of security events |
| Kali Linux | 192.168.3.4 | Attack machine – simulates brute‑force attempts |

tes brute‑force attempts |

│ INTERNAL NETWORK │
│ 192.168.3.0/24 │
│
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ Kali │ │ Windows │ │ Wazuh │ │
│ Linux │ │ 11 │ │ Server │ │
│ (Attacker) │ │ (Target) │ │ (SIEM) │ │
│ 
| 192.168.3.4 │─────►│ 192.168.3.12 │◄─────│ 192.168.3.20 │ │
└──────────────┘ RDP └──────────────┘ Logs └──────────────┘ │
Brute‑Force │

---

## 3. Methodology (SOC Workflow)

### Phase 1: Environment Setup
- Install and configure Wazuh server (manager + indexer + dashboard)
- Deploy Wazuh agent on Windows 11
- Verify agent‑server communication

### Phase 2: Log Collection & Baseline
- Confirm Windows security events (especially Event ID 4625 – failed logon) are being forwarded
- Establish normal login patterns

### Phase 3: Attack Simulation
- Use Kali Linux to launch a simulated RDP brute‑force attack (crows‑rate or hydra)
- Monitor Wazuh dashboard in real time

### Phase 4: Detection & Analysis
- Identify triggered alerts in Wazuh
- Correlate failed logon events with source IP and timestamp
- Document findings as an incident report

### Phase 5: Incident Response Simulation
- Create timeline of events
- Extract Indicators of Compromise (IOCs)
- Map to MITRE ATT&CK techniques
- Propose containment and remediation steps

---

## 4. Key Observations

| Observation | Details |
|-------------|---------|
| Wazuh agent status | ✅ Active and reporting from Windows 11 |
| Security logs received | Event IDs 4624 (success), 4625 (failure), 4634 (logoff), 4672 (special privileges) |
| Baseline behaviour | 0‑2 failed logins per hour (normal user mistypes) |
| During attack | 150+ failed logins from 192.168.3.4 within 2 minutes |
| Wazuh alert triggered | “Multiple failed logins from a single source” – rule 5710 |
| Response time | Alert generated within 5 seconds of the 10th failure |

---

## 5. Security Interpretation (Defensive Perspective)

### Why This Matters
- **Brute‑force attacks** are one of the most common initial access vectors for ransomware and data breaches.
- Early detection (after 10 failures, not 1000) reduces the window for successful compromise.
- SIEM correlation turns raw Windows Event Logs into actionable intelligence.

### What Was Detected
- **Source IP:** 192.168.3.4 (Kali attacker)
- **Target user:** Administrator (simulated)
- **Protocol:** RDP (port 3389)
- **Total attempts:** 153 failures in 120 seconds
- **Alert level:** 12 (high) in Wazuh

### In a Real Enterprise
- **Network segmentation** would limit RDP exposure.
- **Account lockout policies** would temporarily block the source after 5‑10 failures.
- **Automated response** (e.g., firewall block) could be triggered via Wazuh active response.

---

## 6. Threat Perspective (Attacker View)

From an attacker’s standpoint, RDP brute‑forcing is a low‑skill, high‑reward technique when weak passwords or no account lockout exist.

**Attack steps simulated:**
1. Scan for open RDP port (3389) – found open.
2. Launch password spraying or dictionary attack.
3. Monitor for successful authentication.

**Why detection matters to attackers:**
- If an organisation detects and blocks after 10 attempts, attackers must move slower or use evasive techniques.
- Lack of detection encourages sustained attacks.

**This lab shows that even a simple SIEM rule (10 failed logins in 60 seconds) can stop basic brute‑force before success.**

---

## 7. Detection & Alert Details

| Field | Value |
|-------|-------|
| Wazuh Rule ID | 5710 |
| Rule Description | Multiple failed logins from a single source |
| Event ID(s) | 4625 (failed logon) |
| Source IP | 192.168.3.4 |
| Target User | Administrator |
| Logon type | 3 (network) / 10 (remote interactive) |
| Alert trigger threshold | 10 failures within 60 seconds |
| Wazuh Alert Level | 12 (High) |

**Screenshot evidence:** `/screenshots/wazuh-alert-brute-force.png`

---

## 8. MITRE ATT&CK Mapping

| Tactic | Technique | ID |
|--------|-----------|-----|
| Credential Access | Brute Force | T1110 |
| Credential Access | Password Spraying | T1110.003 |
| Discovery | Remote System Discovery | T1018 |
| Lateral Movement | Remote Services (RDP) | T1021.001 |

---

## 9. Incident Summary (High‑Level)

| Item | Details |
|------|---------|
| **Date of simulation** | June 2, 2026 |
| **Detection method** | Wazuh SIEM rule #5710 |
| **Initial vector** | RDP exposed on Windows 11 |
| **Attacker IP** | 192.168.3.4 |
| **Affected account** | Administrator (simulated) |
| **Successful breach?** | ❌ No – stopped after detection |
| **Containment action** | Simulated block of source IP via firewall |

📄 **Full incident report:** [`./incident-response/incident-report.md`](./incident-response/incident-report.md)

---

## 10. Tools Used

| Tool | Purpose |
|------|---------|
| Wazuh (SIEM) | Log collection, alerting, dashboard |
| Windows Event Viewer | Raw log inspection |
| Kali Linux | Brute‑force simulation (hydra / crowbar) |
| VirtualBox | Network isolation |

---

## 11. Lessons Learned

1. **SIEM rules reduce detection time** – 10 failures in 60 seconds is a simple but effective rule.
2. **Windows Event Logs are powerful** – Event ID 4625 contains source IP, username, logon type, and process.
3. **RDP is a common target** – Should never be exposed without additional controls (VPN, MFA, account lockout).
4. **Documentation is as important as detection** – Incident reports prove analytical capability to recruiters.

---

## 12. What This Project Proves

| Skill | Evidence |
|-------|----------|
| SIEM deployment & configuration | Wazuh server + agent installed and communicating |
| Log analysis | Analysed Event ID 4625 from Windows |
| Attack simulation | Launched controlled RDP brute‑force from Kali |
| Alert correlation | Detected pattern of 10+ failures in 60 seconds |
| Incident documentation | Full report with timeline, IOCs, MITRE |
| Defensive thinking | Recommended mitigations and segmentation |

---

## 13. Evidence & Screenshots

📸 All screenshots available in [`./screenshots/`](./screenshots/)

| Screenshot | Description |
|------------|-------------|
| `wazuh-agent-active.png` | Wazuh agent shown as active on Windows 11 |
| `windows-event-4625.png` | Event Viewer showing failed logon events |
| `wazuh-alert-brute-force.png` | Wazuh dashboard alert (rule 5710) |
| `brute-force-simulation.png` | Kali terminal launching hydra / crowbar |
| `incident-timeline.png` | Custom timeline of events |

---

## 14. Future Improvements

- [ ] Add Sysmon to Windows for deeper process/network visibility
- [ ] Create custom Wazuh rule for suspicious RDP logon (e.g., non‑working hours)
- [ ] Integrate active response (automatic firewall block)
- [ ] Add Linux endpoint with SSH brute‑force detection
- [ ] Build second scenario: PowerShell abuse or scheduled task creation

---

## 15. Related Projects

- [Enterprise Network Discovery Lab](../01-enterprise-network-discovery-lab/README.md) – Reconnaissance and attack surface mapping
- [Python Security Tools](../../03-python-security-tools/README.md) – *Planned*

---

**Last Updated:** June 2026  
**Analyst:** Hazem Mordy  
**Environment:** Isolated Virtual Network (VirtualBox + Wazuh SIEM)
