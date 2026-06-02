# Screenshots – SOC Monitoring Lab

This directory contains all visual evidence supporting the SOC Monitoring Lab project. Each screenshot is named according to its content and referenced throughout the documentation.

---

## 1. Wazuh Environment

| Filename | Description | Reference in docs |
|----------|-------------|--------------------|
| `wazuh-dashboard-login.png` | Wazuh dashboard login page (https://192.168.3.20) | `setup-guide.md` |
| `wazuh-agents-active.png` | List of active agents – Windows 11 shown as "Active" | `setup-guide.md` |
| `wazuh-agent-details.png` | Agent details for Windows11-Target (IP, version, last check-in) | `setup-guide.md` |
| `wazuh-events-security.png` | Security events tab showing Windows Event ID 4625 | `windows-event-analysis.md` |

---

## 2. Windows Event Logs (Target)

| Filename | Description | Reference in docs |
|----------|-------------|--------------------|
| `windows-event-4625-single.png` | Event Viewer – single 4625 failed logon event | `windows-event-analysis.md` |
| `windows-event-4625-details.png` | Expanded 4625 event with source IP, logon type, status code | `windows-event-analysis.md` |
| `windows-event-4625-batch.png` | Multiple 4625 events from same source IP within seconds | `brute-force-rdp.md` |
| `windows-event-4624-success.png` | (If applicable) Successful logon – not observed in this lab | – |

---

## 3. Attack Simulation (Kali Linux)

| Filename | Description | Reference in docs |
|----------|-------------|--------------------|
| `kali-rdp-scan.png` | Nmap scan confirming port 3389 open on Windows | `brute-force-rdp.md` |
| `hydra-install.png` | Installing hydra on Kali (`sudo apt install hydra`) | `brute-force-rdp.md` |
| `hydra-attack-running.png` | Hydra terminal showing password attempts in real time | `brute-force-rdp.md` |
| `hydra-attack-complete.png` | Hydra output – all attempts failed | `brute-force-rdp.md` |

---

## 4. Wazuh Alerts & Detection

| Filename | Description | Reference in docs |
|----------|-------------|--------------------|
| `wazuh-alert-brute-force.png` | Wazuh dashboard – rule 5710 alert triggered | `brute-force-rdp.md`, `incident-report.md` |
| `wazuh-alert-details.png` | Expanded alert – source IP 192.168.3.4, 12 failures in 60s | `incident-report.md` |
| `wazuh-rule-5710-config.png` | Rule 5710 configuration (threshold, level, description) | `windows-event-analysis.md` |
| `wazuh-raw-event-4625.png` | Raw JSON event as stored in Wazuh index | `incident-report.md` |

---

## 5. Incident Response & Containment

| Filename | Description | Reference in docs |
|----------|-------------|--------------------|
| `firewall-block-simulation.png` | Windows Firewall rule blocking 192.168.3.4 | `incident-report.md` |
| `wazuh-active-response.png` | (Optional) Wazuh active response configuration | `future-improvements.md` |
| `incident-timeline.png` | Visual timeline of events (drawn manually or via tool) | `incident-report.md` |

---

## 6. Full Lab Environment (Overview)

| Filename | Description | Reference in docs |
|----------|-------------|--------------------|
| `lab-network-topology.png` | Diagram showing all VMs and network connections | `README.md`, `setup-guide.md` |
| `vbox-network-settings.png` | VirtualBox internal network configuration (`cyber-lab`) | `setup-guide.md` |
| `all-vms-running.png` | VirtualBox manager showing all three VMs running | `README.md` |

---

## 7. How to Take These Screenshots (For Your Lab)

If you haven't captured all screenshots yet, here are quick instructions:

| Screenshot | How to capture |
|------------|----------------|
| Wazuh dashboard | Open browser → `https://192.168.3.20` → login → navigate to relevant page |
| Windows Event Viewer | `eventvwr.msc` → Windows Logs → Security → right‑click → Filter Current Log → Event ID 4625 |
| Hydra attack | Run `hydra` command → screenshot terminal before and during attack |
| Wazuh alert | Dashboard → Security Events → find rule 5710 → expand |
| Firewall rule | `wf.msc` → Inbound Rules → screenshot the created block rule |

---

## 8. Naming Convention & Quality

- **Format:** PNG (recommended) or JPG.
- **Naming:** Lowercase, words separated by hyphens (`-`), no spaces.  
  ✅ `hydra-attack-running.png`  
  ❌ `Hydra Attack Running.png`
- **Quality:** Ensure text is readable (zoom in if necessary). Crop irrelevant areas.

---

## 9. Placeholder for Missing Screenshots

If a specific screenshot is not yet available, create a text file with the same name ending in `.placeholder` to indicate it will be added later.

Example: `wazuh-active-response.png.placeholder`

---

**All screenshots referenced in the SOC Monitoring Lab documentation are stored here. For the lab to be complete, at minimum the following five screenshots are required:**

1. `windows-event-4625-single.png`
2. `hydra-attack-running.png`
3. `wazuh-alert-brute-force.png`
4. `wazuh-alert-details.png`
5. `lab-network-topology.png`

---

*Part of the SOC Monitoring Lab – June 2026*
