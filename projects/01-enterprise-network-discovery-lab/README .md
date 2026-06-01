# Enterprise Network Discovery & Attack Surface Analysis

## 1. Executive Summary
This project simulates an internal enterprise reconnaissance scenario where a security analyst identifies active systems, exposed services, and potential attack surfaces within a controlled virtual environment.

##  At a Glance

| Aspect | Summary |
|--------|---------|
| **What I did** | Internal network reconnaissance on isolated Windows 11 host |
| **What I found** | Restrictive firewall blocking all TCP/UDP ports; host discoverable via ARP |
| **Risk level** | LOW — no exposed attack surface from scanning perspective |
| **Key skill** | Interpreting filtered results as a security finding, not a failure |

**Key Finding:** The target system (Windows 11) is protected by a restrictive host-based firewall blocking all common TCP and UDP ports — a strong security baseline that still allows host discovery via ARP.

## 2. Environment Architecture
- VirtualBox isolated network (`cyber-lab`)
- Windows 11 endpoint system (Target)
- Kali Linux security analysis machine (Analyst)

cyber-lab (Internal Network)
│
├── Kali Linux — 192.168.3.4
└── Windows 11 — 192.168.3.12



## 3. Methodology (Security Workflow)

### Phase 1: Asset Discovery
- Host identification using ICMP scanning
- Network range validation via `ipconfig` and `ip addr`

### Phase 2: Service Enumeration
- Port scanning using Nmap (`-sV -O`)
- Service version detection
- OS fingerprinting
- Targeted scans for Windows-specific ports (135,139,445,3389)
- UDP scan (`--top-ports 100`)

### Phase 3: Attack Surface Mapping
- Identification of exposed services
- Initial risk categorization
- Exposure analysis from attacker perspective

## 4. Key Observations

| Finding | Details |
|---------|---------|
| Active Host | `192.168.3.12` confirmed alive via ARP |
| ICMP Behavior | Ping from Kali → Windows: **FAILED** |
| TCP Ports | All 1000 scanned ports: **filtered** |
| UDP Ports | All 100 scanned ports: **open|filtered** |
| Windows Ports | All filtered (135,139,445,3389) |

## 5. Security Interpretation (IMPORTANT)

The presence of a restrictive firewall blocking all incoming connections indicates a **strong security baseline**. However, from an enterprise perspective:

**Why this matters:**
- Host remains discoverable via ARP (unavoidable in internal networks)
- No attack surface exposed externally from scanning perspective
- Firewall is functioning as intended

**In real enterprise environments, such exposure would require:**
- Network segmentation to limit lateral movement
- Regular firewall rule reviews
- Continuous monitoring for unauthorized scanning attempts

##  Threat Perspective

From an attacker perspective, exposed network services provide initial visibility into the target environment. Even when ports are filtered, the following information can still be valuable:

- **Host discovery via ARP** confirms a live target exists
- **Firewall behavior** reveals that security controls are present (which itself is intelligence)
- **Filtered vs. closed ports** helps attackers understand the defensive posture

Service enumeration in this lab revealed:
- No directly accessible services
- Restrictive inbound filtering
- UDP ambiguity (open|filtered state)

**Attacker takeaway:** This target requires more sophisticated methods (social engineering, phishing, or supply chain) rather than direct network exploitation.

---

##  Defensive Perspective

From a defensive security standpoint, identifying exposed services helps security teams:

- **Reduce unnecessary exposure** — Verify why each service is running
- **Improve segmentation** — Isolate critical hosts even from internal scanning
- **Harden systems** — Apply principle of least privilege
- **Monitor critical services** — Alert on unauthorized access attempts

**Key defensive insight from this assessment:**

The Windows 11 host demonstrates a **strong security baseline** with all common ports filtered. However, ARP visibility is unavoidable in internal networks. This reinforces the need for:

1. **Network segmentation** — Even internal scanning should be limited
2. **Firewall logging** — Detect reconnaissance attempts
3. **Host-based monitoring** — Catch what network controls miss

Attack surface visibility is essential for proactive security operations — not to enable attacks, but to close gaps before they can be exploited.

## 6. Attack Surface Map

| Host | Port | Service | Risk Level | Notes |
|------|------|---------|------------|-------|
| 192.168.3.12 | 135 | msrpc | Low (filtered) | Blocked by Windows Firewall |
| 192.168.3.12 | 139 | netbios-ssn | Low (filtered) | Blocked by Windows Firewall |
| 192.168.3.12 | 445 | microsoft-ds | Low (filtered) | Blocked by Windows Firewall |
| 192.168.3.12 | 3389 | ms-wbt-server | Low (filtered) | Blocked by Windows Firewall |

## 7. Tools Used
- Nmap 7.95
- ICMP utilities (ping)
- VirtualBox Internal Networking

##  What This Project Proves

| Skill | Evidence |
|-------|----------|
| Network Reconnaissance | Host discovery via ARP, ICMP analysis |
| Service Enumeration | Nmap scans for TCP/UDP, port analysis |
| Firewall Behavior Analysis | Documented filtered states, ICMP blocking |
| Security Interpretation | Threat + Defensive perspectives written |
| Professional Documentation | Risk matrix, attack surface map, screenshots |
| Enterprise Mindset | Recommendations for segmentation, monitoring |

## 8. Lessons Learned
This exercise demonstrated how early-stage reconnaissance forms the foundation of both penetration testing and SOC-level visibility into network behavior. A "clean" scan result doesn't mean the host is absent — it means security controls are working.

## 9. Evidence
📸 Screenshots available in [`./screenshots/`](./screenshots/)
- `ipconfig-windows.png`
- `ping-fail-kali.png`
- `nmap-sn-sweep.png`
- `nmap-sV-O-results.png`

## 10. Future Improvements
- Add automated scanning scripts (Python)
- Expand network to multi-host enterprise simulation
- Introduce logging and monitoring layer
