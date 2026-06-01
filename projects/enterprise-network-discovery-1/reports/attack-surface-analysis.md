# Attack Surface Analysis Report

## Executive Summary

This report documents the attack surface analysis performed on an internal enterprise network segment. The assessment identified active hosts, enumerated network services, and evaluated potential security exposure from an internal reconnaissance perspective.

**Assessment Date:** June 1, 2026  
**Analyst:** Hazem Mordy  
**Environment:** Isolated Virtual Network (VirtualBox)

---

## Scope

| Item | Details |
|------|---------|
| Target Network | 192.168.3.0/24 |
| Target Host | 192.168.3.12 (Windows 11) |
| Analyst Machine | 192.168.3.4 (Kali Linux) |
| Assessment Type | Internal Network Reconnaissance (Authorized) |

---

## Environment


cyber-lab (Internal Network)
│
├── Kali Linux — 192.168.3.4
└── Windows 11 — 192.168.3.12



**Network Configuration:**
- VirtualBox Internal Network
- No internet gateway
- Isolated from external networks

---

## Methodology

### Phase 1: Discovery
- Host identification via ARP scanning (`nmap -sn`)
- Connectivity testing (ICMP ping)

### Phase 2: Enumeration
- TCP port scan (`nmap -sV -O`)
- Targeted Windows port scan (135,139,445,3389)
- UDP top ports scan (`--top-ports 100`)

### Phase 3: Analysis
- Service exposure evaluation
- Firewall behavior analysis
- Risk categorization

---

## Discovered Assets

| Asset | IP Address | Status | Detection Method |
|-------|------------|--------|------------------|
| Windows 11 | 192.168.3.12 | Active | ARP reply |
| Kali Linux | 192.168.3.4 | Active | Known analyst machine |

---

## Service Enumeration Results

| Port | Service | State | Notes |
|------|---------|-------|-------|
| 135/tcp | msrpc | Filtered | Blocked by Windows Firewall |
| 139/tcp | netbios-ssn | Filtered | Blocked by Windows Firewall |
| 445/tcp | microsoft-ds | Filtered | Blocked by Windows Firewall |
| 3389/tcp | ms-wbt-server | Filtered | Blocked by Windows Firewall |
| All 1000 TCP ports | Various | Filtered | No response from target |
| Top 100 UDP ports | Various | Open/Filte red | No response from target |

---

## Security Observations

### Firewall Behavior
- **ICMP (ping):** Blocked
- **Inbound TCP:** All common ports filtered
- **Inbound UDP:** No response (open/filtered state)
- **ARP:** Allowed (required for network communication)

### Key Finding
The target system is running a **restrictive host-based firewall** (Windows Defender Firewall) that:
- Blocks all unsolicited inbound connections
- Drops ICMP echo requests
- Maintains ARP visibility for network functionality

---

## Risk Analysis

### Risk Matrix

| Finding | Impact | Likelihood | Risk Level | Justification |
|---------|--------|------------|------------|---------------|
| Host discoverable via ARP | Low | High | Low | ARP is fundamental to network operation |
| ICMP blocked | Low | Low | Low | Standard security configuration |
| All TCP ports filtered | Low | Low | Low | No external attack surface exposed |
| UDP ports open/filtered | Medium | Low | Low-Medium | UDP can be exploited but requires specialized techniques |

### Overall Risk Assessment: **LOW**

The target system demonstrates a strong security baseline with no exposed services from the scanning perspective.

---

## Recommendations

For enterprise environments with similar configurations:

1. **Maintain current firewall rules** — They are effectively reducing attack surface
2. **Implement network segmentation** — Isolate sensitive hosts even from internal scanning
3. **Enable firewall logging** — Detect and alert on reconnaissance attempts
4. **Regular rule reviews** — Ensure no unintended exceptions exist
5. **Deploy HIDS** — Host-based detection for internal monitoring

---

## Lessons Learned

1. **"No results" is a finding** — A filtered port scan indicates security controls are working
2. **ARP visibility is unavoidable** — Hosts must respond to ARP; this is why monitoring matters
3. **Documentation separates analysts from technicians** — Interpreting results is the core skill
4. **Enterprise context changes everything** — The same scan has different meanings in different environments

---

## References

- Nmap scan outputs: `/raw-results/`
- Screenshots: `/screenshots/`
- Network diagram: `/diagrams/network-architecture.png`

---

## Appendix: Commands Used

```bash
# Host discovery
sudo nmap -sn 192.168.3.0/24

# Service enumeration
sudo nmap -sV -O 192.168.3.12

# Targeted Windows port scan
sudo nmap -p 135,139,445,3389 -Pn 192.168.3.12

# UDP scan
sudo nmap -sU --top-ports 100 192.168.3.12
