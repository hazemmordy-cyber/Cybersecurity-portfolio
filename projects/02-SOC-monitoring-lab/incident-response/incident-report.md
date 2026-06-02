# Incident Response Report – RDP Brute‑Force Attempt

## 1. Incident Summary

| Field | Details |
|-------|---------|
| **Incident ID** | SOC‑IR‑2026‑001 |
| **Date & Time Detected** | 2026‑06‑02 14:23:45 UTC |
| **Detection Method** | Wazuh SIEM (rule 5710) |
| **Reporter** | Wazuh alert (automated) |
| **Affected Asset** | Windows 11 (192.168.3.12) – hostname: WIN‑11 |
| **Attacker Source** | 192.168.3.4 (Kali Linux) |
| **Incident Type** | Credential brute‑force (RDP) |
| **Success** | ❌ No successful authentication |
| **Containment Status** | Simulated – source IP blocked at network level |
| **Current Status** | Closed – investigation complete |

---

## 2. Executive Summary

On 2026‑06‑02 at 14:23:45 UTC, Wazuh SIEM triggered a high‑severity alert (rule 5710) indicating 12 failed Windows logon attempts from source IP `192.168.3.4` against the `Administrator` account on the Windows 11 target (`192.168.3.12`) within a 60‑second window. The logon type was `10` (Remote Interactive – RDP), confirming the attack was network‑based.

Investigation revealed no successful logons (Event ID 4624) following the failures, and the account was not locked out due to the absence of an account lockout policy in the lab environment. The attack was simulated using `hydra` from a Kali Linux machine within the same internal network.

Immediate containment was simulated by blocking the attacker IP via a firewall rule. This incident demonstrates the effectiveness of simple SIEM correlation rules in detecting automated brute‑force attempts at an early stage.

---

## 3. Incident Timeline (All timestamps UTC)

| Time | Event | Source |
|------|-------|--------|
| 14:22:30 | Kali begins TCP connect scan to Windows port 3389 – confirms RDP open | Nmap (pre‑attack reconnaissance) |
| 14:23:15 | Hydra launches dictionary attack against `Administrator` account | Kali terminal log |
| 14:23:17 | First failed logon (4625) recorded – source 192.168.3.4 | Windows Security Event Log |
| 14:23:18–14:23:44 | 11 additional failed logons (4625) – same source and username | Windows Security Event Log |
| 14:23:45 | Wazuh rule 5710 triggers – 12 failures within 60 seconds | Wazuh dashboard |
| 14:23:46 | SOC analyst acknowledges alert | Simulated |
| 14:24:00 | Analyst confirms no successful logons (4624) from attacker IP | Wazuh query |
| 14:25:00 | Containment action simulated – firewall block of 192.168.3.4 | Simulated |
| 14:30:00 | Incident declared closed – no compromise | SOC lead |

---

## 4. Affected Systems & Scope

| System | IP Address | Role | Impact |
|--------|------------|------|--------|
| Windows 11 | 192.168.3.12 | Target endpoint | No compromise – only failed attempts |
| Wazuh Server | 192.168.3.20 | SIEM platform | None – monitoring continued normally |
| Kali Linux | 192.168.3.4 | Attacker machine | Simulated attacker, not an asset under defence |

**Lateral movement:** None – no successful authentication occurred.

**Data exposure:** None – attacker never gained access.

---

## 5. Detection Details

### 5.1 Alert Information (Wazuh)

| Field | Value |
|-------|-------|
| Alert ID | `wazuh-alert-20260602-142345` |
| Rule ID | 5710 |
| Rule Level | 10 / 15 (High) |
| Rule Description | Multiple Windows logon failures from same source |
| MITRE Technique | T1110 – Brute Force |
| Log source | Windows 11 (agent: Windows11-Target) |
| Trigger count | 12 failures in 60 seconds |
| Attacker IP | 192.168.3.4 |
| Target account | Administrator |
| Logon type | 10 (RemoteInteractive – RDP) |

### 5.2 Raw Event Sample (Wazuh stored JSON)

```json
{
  "timestamp": "2026-06-02T14:23:45.123Z",
  "rule": { "id": 5710, "level": 10, "description": "Multiple Windows logon failures from same source" },
  "agent": { "id": "002", "name": "Windows11-Target", "ip": "192.168.3.12" },
  "data": {
    "win": {
      "eventID": 4625,
      "eventData": {
        "targetUserName": "Administrator",
        "logonType": "10",
        "sourceNetworkAddress": "192.168.3.4",
        "status": "0xC000006D",
        "workstationName": "WIN-11"
      }
    }
  }
}
```

---

## 6. Indicators of Compromise (IOCs)

| Type | Value | Description |
|------|-------|-------------|
| Source IP | 192.168.3.4 | Attacker machine address |
| Target account | Administrator | Targeted local admin account |
| Protocol/Port | RDP / 3389 | Attack vector |
| Event ID pattern | 4625 (failure) → no 4624 (success) | Indicates unsuccessful brute‑force |
| Failure reason code | 0xC000006D | Bad username or password (not lockout) |

**Note:** No file hashes, domain names, or registry keys were generated because the attack never executed code on the target.

---

## 7. MITRE ATT&CK Mapping

| Tactic | Technique | ID | Observed Behaviour |
|--------|-----------|-----|---------------------|
| Reconnaissance | Remote System Discovery | T1018 | Nmap scan for port 3389 |
| Credential Access | Brute Force | T1110 | Hydra password guessing |
| Credential Access | Password Spraying | T1110.003 | Single user, many passwords |
| Lateral Movement | Remote Services (RDP) | T1021.001 | Attempted logon via RDP |
| Impact | Account Lockout (if policy existed) | T1531 | Not observed – lab lacked lockout policy |

---

## 8. Containment & Eradication (Simulated)

### 8.1 Immediate Containment
- **Action:** Add firewall rule to block all traffic from `192.168.3.4` to `192.168.3.12`.
- **Command example (Windows Firewall):**
  ```powershell
  New-NetFirewallRule -DisplayName "Block Brute Force Source" -Direction Inbound -RemoteAddress 192.168.3.4 -Action Block
  ```
- **Result:** Attacker can no longer reach RDP or any other service on the target.

### 8.2 Eradication
- No malicious files, processes, or persistence mechanisms were found because the attack did not succeed.
- No need for password reset (account not compromised).

### 8.3 Lessons Learned for Containment
- In a real environment, automated response (e.g., Wazuh active response) could trigger this block instantly.
- Account lockout policy would have stopped the attack after ~5 failures, reducing noise.

---

## 9. Recommendations for Improvement

| Priority | Recommendation | Justification |
|----------|----------------|---------------|
| **High** | Implement account lockout policy (5 failures → lock 15 min) | Prevents brute‑force even before SIEM alerts |
| **High** | Restrict RDP source IPs to known admin workstations | Reduces attack surface drastically |
| **Medium** | Enable MFA for RDP (Duo / Microsoft Authenticator) | Makes brute‑force ineffective even with correct password |
| **Medium** | Deploy Sysmon on Windows for deeper process/network visibility | Helps detect post‑compromise activity |
| **Low** | Increase Wazuh rule threshold to 15 failures/60s | Reduce false positives (if observed in environment) |
| **Low** | Set up automated alert→ticket integration (TheHive, Jira) | Improves SOC workflow |

---

## 10. Root Cause Analysis

**Root cause:** RDP exposed on the Windows 11 host without:
- Source IP restriction
- Account lockout policy
- MFA

**Why the attack succeeded in failing?**  
The attacker was able to launch 12+ attempts in 60 seconds because:
- No lockout threshold prevented repeated attempts.
- No network filtering blocked the attacker IP.

**Why no compromise?**  
The dictionary did not contain the correct password for `Administrator`. If the password were weak, the attacker would have gained access.

**Final verdict:** The detection worked as designed, but preventive controls were missing. The incident is classified as a **successful detection** with **preventive gaps**.

---

## 11. Evidence Retention

| Evidence Type | Location / Reference | Retention Period |
|---------------|----------------------|------------------|
| Wazuh alert JSON | `/raw-results/wazuh-alert-5710.json` | Lab duration |
| Windows Event log export (evtx) | `/raw-results/security-log-brute-force.evtx` | Lab duration |
| Screenshots | `/screenshots/*.png` | Permanent (portfolio) |
| Hydra command output | `/raw-results/hydra-output.log` | Lab duration |
| MITRE mapping | This document | Permanent |

---

## 12. Incident Response Metrics (for SOC improvement)

| Metric | Value |
|--------|-------|
| Time to detect (TTD) | 30 seconds (from first failure to alert) |
| Time to acknowledge (TTA) | ~15 seconds (automated, analyst confirmed at 14:23:45) |
| Time to contain (TTC) | Simulated: 1 minute (manual firewall rule) |
| Number of false positives this month | 0 (lab environment) |
| Mean time to respond (MTTR) | Not applicable (no compromise) |

---

## 13. Conclusion

This incident was a **successful detection** of a simulated RDP brute‑force attack. The Wazuh SIEM rule triggered within 30 seconds of the first failure, demonstrating the value of simple correlation rules (10 failures/60 seconds). No compromise occurred because the password dictionary did not match.

The main gaps identified were the lack of preventive controls (account lockout, source IP restriction, MFA). These will be addressed in future lab iterations to reflect a more mature security posture.

The incident report serves as a template for documenting real‑world security events and proves the analyst's ability to:
- Detect automated attacks.
- Correlate multiple events.
- Recommend practical mitigations.
- Communicate findings in a structured, professional format.

---

## 14. Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| SOC Analyst (Investigator) | Hazem Mordy | (simulated) | 2026‑06‑02 |
| SOC Lead (Reviewer) | (simulated) | (simulated) | 2026‑06‑02 |

---

## 15. References

- [Wazuh Rule 5710](https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax.html)
- [Microsoft Event ID 4625](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4625)
- [MITRE ATT&CK T1110 – Brute Force](https://attack.mitre.org/techniques/T1110/)
- [SANS Incident Handling Process](https://www.sans.org/white-papers/33401/)

---

**End of Report – SOC‑IR‑2026‑001**

*Part of the SOC Monitoring Lab – June 2026*
