# Environment Setup Guide

## 1. Overview

This document describes how the SOC monitoring environment was built. The lab consists of three virtual machines connected via an isolated VirtualBox internal network, with Wazuh acting as the central SIEM platform.

| Component | IP Address | Purpose |
|-----------|------------|---------|
| Wazuh Server (Linux) | 192.168.3.20 | Wazuh manager + indexer + dashboard |
| Windows 11 (Target) | 192.168.3.12 | Endpoint with Wazuh agent |
| Kali Linux | 192.168.3.4 | Attack simulation machine |

All machines are on the same internal network (`cyber-lab`) with no internet gateway, ensuring a controlled, repeatable environment.

---

## 2. Network Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    INTERNAL NETWORK (cyber-lab)                 │
│                        192.168.3.0/24                           │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │   Wazuh Server  │    │   Windows 11    │    │    Kali     │ │
│  │   (Linux)       │    │   (Agent)       │    │   (Attack)  │ │
│  │                 │    │                 │    │             │ │
│  │ 192.168.3.20    │◄──►│ 192.168.3.12    │    │192.168.3.4  │ │
│  └─────────────────┘    └─────────────────┘    └─────────────┘ │
│           ▲                       ▲                             │
│           │                       │                             │
│           │   Port 1514 (agent →  │                             │
│           │   manager, encrypted) │                             │
│           └───────────────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

**Communication flow:**
- Wazuh agent (Windows 11) sends logs to Wazuh manager (Linux) via TCP port 1514.
- Wazuh dashboard is accessible from any machine in the network via port 443 (HTTPS).
- Kali Linux only initiates attack traffic (RDP to Windows 11) and does not interact with Wazuh directly.

---

## 3. Wazuh Server Installation (Linux – 192.168.3.20)

### 3.1 System Requirements
- Ubuntu 22.04 or 24.04 (minimal server)
- 4 GB RAM, 2 CPU cores, 20 GB disk (minimum for lab)
- Network access to the internal network

### 3.2 Installation Steps (Quick Reference)

The official all‑in‑one installation script was used:

```bash
# Download and run the assistant
curl -sO https://packages.wazuh.com/4.9/wazuh-install.sh
sudo bash wazuh-install.sh --generate-config-files

# Run the installation with dashboard access
sudo bash wazuh-install.sh --wazuh-indexer node-1 \
  --wazuh-server wazuh-1 \
  --wazuh-dashboard dashboard \
  --start-cluster
```

After installation, the dashboard was accessible at:  
`https://192.168.3.20:443` (default credentials: admin / admin)

> ⚠️ In a real enterprise, credentials would be changed immediately and SSL certificates properly configured.

### 3.3 Verification

- All containers/services running:  
  `sudo systemctl status wazuh-manager`
- Indexer accessible:  
  `curl -k -u admin:admin https://localhost:9200`
- Dashboard reachable from browser:  
  `https://192.168.3.20`

---

## 4. Wazuh Agent Installation (Windows 11 – 192.168.3.12)

### 4.1 Download & Install

1. From the Wazuh dashboard, navigate to **Wazuh** → **Agents** → **Add agent**.
2. Select Windows as the operating system.
3. Set the manager IP address: `192.168.3.20`
4. Copy the generated installation command (similar to below).

**Example command (run as Administrator in PowerShell):**

```powershell
Invoke-WebRequest -Uri https://packages.wazuh.com/4.x/wazuh-agent-4.9.0-1.msi -OutFile ${env:tmp}\wazuh-agent.msi
msiexec.exe /i ${env:tmp}\wazuh-agent.msi /q WAZUH_MANAGER="192.168.3.20" WAZUH_AGENT_NAME="Windows11-Target" WAZUH_REGISTRATION_SERVER="192.168.3.20"
```

### 4.2 Post‑Installation Checks

- The agent service should be running:  
  `Get-Service -Name WazuhSvc`
- Firewall rule for outbound port 1514 must be allowed (default Windows Firewall permits).
- Verify agent connection in Wazuh dashboard:  
  **Agents** → should show `Windows11-Target` with status `Active`.

### 4.3 Confirming Log Forwarding

Security logs are forwarded by default via the `ossec.conf` configuration:

```xml
<localfile>
  <location>Security</location>
  <log_format>eventchannel</log_format>
</localfile>
```

To test, generate a failed logon event (e.g., wrong password on RDP) and check if it appears in Wazuh dashboard under **Events**.

---

## 5. Kali Linux Attack Machine Setup (192.168.3.4)

Kali Linux was already available. Only a few tools were needed for RDP brute‑force simulation.

### 5.1 Install Hydra (if not present)

```bash
sudo apt update
sudo apt install hydra -y
```

### 5.2 Basic connectivity test to Windows RDP

```bash
nmap -p 3389 192.168.3.12
# Expected: 3389/tcp open  ms-wbt-server
```

---

## 6. Wazuh Rule Configuration for Brute‑Force Detection

Wazuh comes with a built‑in rule for multiple failed logins (rule 5710). However, we customised the threshold for demonstration purposes.

### 6.1 Default rule location (no modification needed for lab)

`/var/ossec/ruleset/rules/0365-windows_rules.xml`

**Relevant rule snippet:**

```xml
<rule id="5710" level="10">
  <if_sid>5710</if_sid>
  <match>Windows EventID: 4625</match>
  <description>Multiple Windows logon failures from same source</description>
  <group>authentication_failed,</group>
</rule>
```

### 6.2 Verification that the rule is active

In Wazuh dashboard: **Rules** → search for `5710`. Should be enabled by default.

---

## 7. Testing the Full Pipeline

### 7.1 Generate a single failed logon (baseline)

From Kali, attempt one wrong password via RDP using `xfreerdp`:

```bash
xfreerdp /v:192.168.3.12 /u:Administrator /p:wrongpassword
```

### 7.2 Check Wazuh Events

In Wazuh dashboard → **Events** → filter by `data.win.eventdata.ipAddress:192.168.3.4`  
You should see Event ID 4625 with logon type 3 or 10.

### 7.3 Simulate brute‑force (covered in detail in detection scenario)

```bash
hydra -l Administrator -P /usr/share/wordlists/fasttrack.txt rdp://192.168.3.12 -t 4 -V
```

After ~10 failures within 60 seconds, rule 5710 will trigger an alert.

---

## 8. Environment Validation Checklist

| Check | Status |
|-------|--------|
| Wazuh manager service running | ✅ |
| Wazuh dashboard accessible | ✅ |
| Windows agent installed and active | ✅ |
| Agent reporting to manager (last seen <1 min) | ✅ |
| Security events visible in dashboard | ✅ |
| Kali can reach Windows RDP port | ✅ |
| Hydra installed on Kali | ✅ |
| Default rule 5710 enabled | ✅ |

---

## 9. Troubleshooting Common Issues

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Agent status "Never connected" | Firewall blocking port 1514 | Allow outbound TCP 1514 on Windows |
| No events in dashboard | Agent not reading Security log | Check `ossec.conf` for `<localfile>` section |
| RDP connection from Kali fails | Windows RDP disabled or firewall block | Enable RDP via System Properties → Remote |
| Hydra shows "connection refused" | RDP service not listening | Verify `netstat -an | findstr 3389` on Windows |
| Rule 5710 not firing | Threshold not met (10 failures in short time) | Increase attempts or reduce time window |

---

## 10. Security Notes for the Lab Environment

- **Isolation:** The internal network has no internet gateway, so no accidental exposure.
- **Credentials:** All default passwords changed in production; lab uses throwaway VMs.
- **RDP exposure:** Simulated intentionally for detection testing; never exposed to real internet.
- **Wazuh dashboard:** In production, restrict access via VPN or dedicated management network.

---

## 11. References

- [Wazuh Documentation – Installation](https://documentation.wazuh.com/current/installation-guide/index.html)
- [Wazuh – Windows agent deployment](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-windows.html)
- [Microsoft Event ID 4625](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4625)

---

**Next File:** [Windows Event Log Analysis](./logs/windows-event-analysis.md) – deep dive into Event IDs relevant to SOC monitoring.

*Part of the SOC Monitoring Lab – June 2026*
```
