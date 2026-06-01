# Enterprise Network Discovery & Attack Surface Mapping

## Executive Summary

This project simulates the reconnaissance phase of an internal enterprise security assessment. The objective was to identify active hosts, enumerate services, and analyze exposed attack surfaces within a controlled, isolated virtual environment.

**Key Finding:** The target system (Windows 11) is protected by a restrictive host-based firewall blocking all common TCP and UDP ports — a strong security baseline that still allows host discovery via ARP.

---

## Environment Architecture

| Component | Details |
|-----------|---------|
| Analyst Machine | Kali Linux (VirtualBox) |
| Target System | Windows 11 (VirtualBox) |
| Network Type | VirtualBox Internal Network (`cyber-lab`) |
| Network Range | 192.168.3.0/24 |




cyber-lab (Internal Network)
│
├── Kali Linux — 192.168.3.4
└── Windows 11 — 192.168.3.12




---

## Methodology

### Phase 1: Network Discovery
- Identified IP addresses via `ipconfig` (Windows) and `ip addr` (Kali)
- Tested connectivity using ICMP (ping)

### Phase 2: Host Sweeping
- Used `nmap -sn` to discover live hosts without relying on ICMP

### Phase 3: Service Enumeration
- Performed TCP port scan: `nmap -sV -O`
- Targeted specific Windows ports: `-p 135,139,445,3389 -Pn`
- UDP scan: `nmap -sU --top-ports 100`

### Phase 4: Attack Surface Analysis
- Interpreted results in enterprise security context
- Assessed risk levels and mitigation thinking

---

## Key Findings

| Finding | Details |
|---------|---------|
| Active Host | `192.168.3.12` confirmed alive via ARP |
| ICMP Behavior | Ping from Kali → Windows: **FAILED** |
| TCP Ports | All 1000 scanned ports: **filtered** |
| UDP Ports | All 100 scanned ports: **open\|filtered** |
| Windows Ports (135,139,445,3389) | All **filtered** |
| OS Fingerprint | Inconclusive due to firewall |

### Attack Surface Map

| Host | Port | Service | Risk Level | Notes |
|------|------|---------|------------|-------|
| 192.168.3.12 | 135 | msrpc | Low (filtered) | Blocked by Windows Firewall |
| 192.168.3.12 | 139 | netbios-ssn | Low (filtered) | Blocked by Windows Firewall |
| 192.168.3.12 | 445 | microsoft-ds | Low (filtered) | Blocked by Windows Firewall |
| 192.168.3.12 | 3389 | ms-wbt-server | Low (filtered) | Blocked by Windows Firewall |

---

## Security Interpretation

**What does this mean in real enterprise context?**

1. **Restrictive firewall is a security control** — Not a vulnerability. The target is configured to block inbound connections by default.

2. **ARP exposure is unavoidable** — In internal networks, hosts must respond to ARP to communicate. This is why network segmentation and monitoring are critical.

3. **"No results" is a finding** — Understanding when ports are *filtered* vs. *closed* vs. *open* is essential for accurate threat assessment.

4. **Enterprise relevance** — Many internal servers have similar configurations. The security question is not "can I hack it?" but "is this configuration appropriate for the system's role?"

---

## Risk Assessment

| Risk Area | Level | Justification |
|-----------|-------|---------------|
| External Attack Surface | Low | No exposed ports from scanning perspective |
| Internal Visibility | Medium | Host discoverable via ARP (by design) |
| Misconfiguration Risk | Low | Firewall behaving as expected |

---

## Mitigation Thinking (For Enterprise)

If an organization wants to reduce risk further:
- Implement network segmentation (isolate sensitive hosts)
- Enable advanced firewall logging to detect scanning attempts
- Use host-based intrusion detection (HIDS) for internal monitoring
- Regular review of firewall rules for operational exceptions

---

## Lessons Learned

- Firewalls can block ICMP but still allow ARP — understanding network layers matters
- A "clean" scan result doesn't mean the host is absent; it means controls are working
- Documentation and interpretation separate a technician from an analyst

---

## Evidence

📸 Screenshots available in [`./screenshots/`](./screenshots/)

1. `ipconfig-windows.png` — Windows IP configuration
2. `ping-fail-kali.png` — Failed ping from Kali to Windows
3. `nmap-sn-sweep.png` — Network sweep showing live host via ARP
4. `nmap-sV-O-results.png` — Service enumeration showing filtered ports

---

## Tools Used

- Nmap 7.95
- Ping (ICMP)
- VirtualBox 7.x (Internal Networking)
- Windows 11 (Target)
- Kali Linux (Analysis)

---

## Conclusion

This lab demonstrates that effective security assessments require more than running tools. The ability to interpret filtered results, document findings professionally, and translate technical observations into business-relevant risk language is what defines a security analyst.

The target system exhibited a strong security baseline (restrictive firewall). From an enterprise perspective, this configuration reduces external attack surface while maintaining internal network functionality — a balanced approach when combined with monitoring and segmentation.