# 🔐 Security Port Auditor – Python Automation Tool

## 1. Objective

Build a lightweight, reusable Python script for TCP port discovery and structured logging inside an isolated lab environment. This tool automates reconnaissance steps, turning manual scanning into an **auditable, repeatable process** – a foundational skill for security automation.

## 2. Features

- TCP port scanning (common ports or user‑specified)
- Simple banner grabbing for open ports
- Real‑time console output with open/closed status
- Saves results in **JSON** and **CSV** formats (timestamped)
- No external dependencies – uses only Python standard library
- Configurable timeout per port

## 3. Lab Environment

| Component | Details |
|-----------|---------|
| Platform | Kali Linux (or any Python 3 environment) |
| Target | Windows 11 (192.168.3.12) – isolated VirtualBox network |
| Network | `cyber-lab` internal network (192.168.3.0/24) |

## 4. Usage

### 4.1 Clone / Navigate

``bash
cd projects/03-python-security-auditor

### 4.2 Run the scanner
Basic scan (common ports):
python src/port_auditor.py 192.168.3.12

Scan specific ports:
python src/port_auditor.py 192.168.3.12 --ports 22,80,443,3389

Adjust timeout (seconds):
python src/port_auditor.py 192.168.3.12 --timeout 2.0

### 4.3 Example output (console)
text
Starting port scan on 192.168.3.12 with timeout 1.0s
✗ 21/tcp -> closed
✗ 22/tcp -> closed
...
✓ 3389/tcp -> open
...
==================================================
Scan completed for 192.168.3.12
Total ports checked: 20
Open ports: 1
Open ports details:
  3389/tcp -> banner: (none)
==================================================
JSON output saved to: outputs/scan_192.168.3.12_20260602_143022.json
CSV output saved to: outputs/scan_192.168.3.12_20260602_143022.csv
### 4.4 Output files
JSON – structured, machine‑readable.

CSV – easy to open in spreadsheets for analysis.

Example JSON entry:

json
{
  "target": "192.168.3.12",
  "port": 3389,
  "state": "open",
  "service_banner": ""
}

## 5. Security & Ethical Use
⚠️ This tool is for authorised environments only (your own lab, systems you own, or explicit permission). It performs active TCP connections – unauthorised scanning may violate laws or policies. The developer is not responsible for misuse.

## 6. Findings from the Lab
When run against the Windows 11 target (192.168.3.12) with default common ports:

Port	Service	State	Banner
3389	RDP	Open	(none)
Others	–	Closed/Filtered	–
Interpretation: The host’s firewall (Windows Defender) blocked most ports except RDP (which was intentionally enabled for the SOC lab). This tool proved that RDP was reachable – consistent with our earlier manual Nmap results.

## 7. Limitations & Future Improvements
Limitation	Planned Enhancement
No UDP scanning	Add UDP probe option
Single‑threaded	Implement threading for speed
Basic banner grabbing	Expand with protocol‑specific banners
No service versioning	Integrate with Nmap’s service detection logic (future)
## 8. Lessons Learned
Socket programming gives direct control over network probes.

Structured output (JSON/CSV) makes results reusable for further analysis or SIEM ingestion.

CLI arguments make the tool flexible and scriptable.

Timeout handling is critical – too short = false negatives; too long = slow scans.

Documentation is as important as code – a clean README proves engineering mindset.

## 9. How This Fits the Portfolio
Project	Skills Demonstrated
Project 1 (Network Discovery)	Nmap, manual recon, interpretation
Project 2 (SOC Lab)	SIEM, log analysis, incident response
Project 3 (Python Auditor)	Automation, Python, data serialisation, tool building
Together they show offensive awareness, defensive monitoring, and automation – a well‑rounded junior security professional.

## 10. References
Python socket documentation

Port scanning ethics

Created: June 2026
Author: Hazem Mordy
Environment: Python 3.10+, VirtualBox isolated network
