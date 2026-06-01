# Enterprise Network Discovery & Attack Surface Analysis

## 1. Executive Summary
This project simulates an internal enterprise reconnaissance scenario where a security analyst identifies active systems, exposed services, and potential attack surfaces within a controlled virtual environment.

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
