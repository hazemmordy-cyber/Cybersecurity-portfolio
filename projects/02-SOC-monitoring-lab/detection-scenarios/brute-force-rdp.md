# Brute‑Force Detection Scenario (RDP)

## 1. Scenario Overview

This document simulates a realistic brute‑force attack against Remote Desktop Protocol (RDP) on the Windows 11 target. The attack is launched from Kali Linux using `hydra`, and detection is performed by Wazuh SIEM via Windows Event ID 4625 (failed logon). The purpose is to demonstrate the full detection lifecycle from attack execution to alert generation and analysis.

| Aspect | Details |
|--------|---------|
| **Target** | Windows 11 (192.168.3.12) – RDP port 3389 open |
| **Attacker** | Kali Linux (192.168.3.4) |
| **Attack type** | Password brute‑force (dictionary) |
| **Detection mechanism** | Wazuh rule 5710 (10+ failed logons / 60 sec) |
| **Outcome** | Alert triggered; no successful compromise |

---

## 2. Pre‑Attack Validation

Before launching the attack, we verified that:

- RDP is enabled on Windows 11:  
  `System Properties → Remote → Allow remote connections`
- Windows Firewall allows inbound RDP (port 3389).
- Wazuh agent is active and forwarding security events.
- Kali has network connectivity to Windows RDP port:  
  `nmap -p 3389 192.168.3.12` → open.

---

## 3. Attack Simulation (Hydra)

### 3.1 Tool Used: Hydra

Hydra is a fast network logon cracker supporting many protocols, including RDP.

**Installation on Kali (if not present):**
```bash
sudo apt update && sudo apt install hydra -y
```

### 3.2 Dictionary Preparation

We used a small custom wordlist (`/tmp/rdp_passwords.txt`) to simulate a realistic attack without exhausting system resources.

**Example wordlist content:**
```
admin
123456
password
Password123
Welcome1
Administrator
letmein
12345
```

For demonstration, a larger dictionary (`/usr/share/wordlists/fasttrack.txt`) was also tested.

### 3.3 Launching the Attack

The command used to simulate a brute‑force attack against the `Administrator` account:

```bash
hydra -l Administrator -P /tmp/rdp_passwords.txt rdp://192.168.3.12 -t 4 -V
```

**Parameters explained:**
- `-l Administrator` – single username (target)
- `-P` – password list file
- `rdp://192.168.3.12` – protocol and target
- `-t 4` – four parallel tasks (controlled to avoid network flooding)
- `-V` – verbose output (shows each attempt)

**Partial output:**
```
[ATTEMPT] target 192.168.3.12 - login "Administrator" - pass "123456" - 1 of 8
[ATTEMPT] target 192.168.3.12 - login "Administrator" - pass "password" - 2 of 8
...
[STATUS] attack finished for 192.168.3.12 (waiting for responses)
```

All attempts failed because no correct password was present in the dictionary.

### 3.4 Why Hydra Is Noisy

Hydra generates a new RDP connection attempt per password. Each failed attempt creates:
- A Windows Event ID 4625 in the Security log.
- Network traffic (TCP SYN, RDP negotiation).
- CPU usage on the target.

This noise is exactly what detection rules rely on.

---

## 4. Detection in Wazuh

### 4.1 Immediate Alert

Within 5 seconds after the 10th failed attempt, Wazuh generated an alert (rule 5710).

**Alert details as seen in Wazuh dashboard:**

| Field | Value |
|-------|-------|
| Timestamp | 2026-06-02T14:23:45Z |
| Rule ID | 5710 |
| Rule Level | 10 (High) |
| Description | Multiple Windows logon failures from same source |
| Source IP | 192.168.3.4 |
| Target User | Administrator |
| Logon Type | 10 (RemoteInteractive) |
| Failure Count (last 60s) | 12 |
| Agent | Windows11-Target |

### 4.2 Raw Event from Windows (as stored in Wazuh)

```json
{
  "_index": "wazuh-states-2026.06.02",
  "_source": {
    "timestamp": "2026-06-02T14:23:45.123Z",
    "rule": { "id": 5710, "level": 10, "description": "Multiple Windows logon failures from same source" },
    "agent": { "name": "Windows11-Target", "ip": "192.168.3.12" },
    "data": {
      "win": {
        "eventID": 4625,
        "eventData": {
          "subjectUserName": "-",
          "targetUserName": "Administrator",
          "logonType": "10",
          "sourceNetworkAddress": "192.168.3.4",
          "status": "0xC000006D",
          "workstationName": "WIN-11"
        }
      }
    }
  }
}
```

### 4.3 Dashboard View

The alert appeared in the **Security Events** tab with high severity. Clicking the alert revealed:
- The exact count of failures per source IP.
- A timeline showing the attack intensity.
- A direct link to the raw events for deeper investigation.

**Screenshot reference:** `/screenshots/wazuh-alert-brute-force.png`

---

## 5. Analyst Investigation Steps

As a SOC analyst reviewing this alert, the following actions would be taken:

### 5.1 Validate the Alert
- Confirm that source IP `192.168.3.4` is not a legitimate admin workstation.
- Check the failure reason: `0xC000006D` = bad username or password (not account lockout).

### 5.2 Correlate with Other Events
- Query for any **4624** (successful logon) from the same source IP within ±5 minutes – none found.
- Check for account lockout (4740) – none found (lockout policy not configured).

### 5.3 Assess Impact
- No successful authentication → no immediate compromise.
- The attack was automated (evidenced by high frequency).
- The target account `Administrator` is high‑value.

### 5.4 Containment Actions (Simulated)
- **Firewall block** at network level: deny all traffic from `192.168.3.4` to `192.168.3.12`.
- **Temporary account lockout** – if policy existed, would trigger automatically.
- **Notify incident response team** for further investigation.

### 5.5 Long‑Term Remediation Recommendations
- Enforce account lockout policy (e.g., 5 failures → lock 15 min).
- Require strong passwords / passphrases.
- Limit RDP access to specific admin workstations (source IP restriction).
- Implement MFA for RDP (e.g., Duo, Microsoft Authenticator).

---

## 6. MITRE ATT&CK Mapping

| Tactic | Technique | ID | Notes |
|--------|-----------|-----|-------|
| Credential Access | Brute Force | T1110 | Password guessing |
| Credential Access | Password Spraying | T1110.003 | Single password across many accounts (variant) |
| Lateral Movement | Remote Services (RDP) | T1021.001 | Attacker used RDP protocol |
| Discovery | Remote System Discovery | T1018 | Pre‑attack scan of port 3389 |

---

## 7. Detection Engineering Insights

### 7.1 Why Rule 5710 Worked
- The threshold (10 failures/60s) was low enough to trigger early.
- The logon type (10) was not filtered, but could be added to reduce false positives from network logons (type 3).

### 7.2 Potential False Positives
- An administrator mistyping password 10 times in a minute – rare but possible.
- Automated scripts that legitimately fail due to expired credentials.

### 7.3 Possible Improvements
- Increase threshold to 15 failures in 60 seconds.
- Exclude specific source IPs (e.g., admin jump hosts).
- Create a separate rule for high‑velocity attacks (>30/min) with higher severity.

---

## 8. Replayability and Conclusion

This scenario is fully reproducible in any lab environment with:
- Wazuh server + agent.
- Windows with RDP enabled.
- Kali with hydra.

The detection demonstrated that **even a simple SIEM rule** can catch automated brute‑force attacks before they succeed, providing valuable early warning to defenders.

---

## 9. Evidence Collected

All evidence is stored in the `/screenshots/` directory:

| File | Content |
|------|---------|
| `hydra-attack-running.png` | Terminal showing hydra attempts |
| `windows-event-4625-batch.png` | Event Viewer showing multiple 4625 events |
| `wazuh-alert-brute-force.png` | Wazuh dashboard alert (rule 5710) |
| `wazuh-rule-details.png` | Expanded alert with source IP and failure count |
| `block-simulation.png` | Simulated firewall block rule |

---

## 10. References

- [Hydra – Kali Tools](https://www.kali.org/tools/hydra/)
- [Wazuh Rule 5710 Documentation](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax.html)
- [Microsoft – Detecting Brute Force Attacks](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/advanced-security-audit-policies)

---

**Next File:** [Incident Response Report](../incident-response/incident-report.md) – Full documentation of this event as a formal security incident.

*Part of the SOC Monitoring Lab – June 2026*
