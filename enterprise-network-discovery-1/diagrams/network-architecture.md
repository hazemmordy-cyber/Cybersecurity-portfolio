# Network Architecture Diagram

## Enterprise Network Discovery Lab


┌─────────────────────────────────────────────────────────────┐
│ INTERNAL NETWORK │
│ cyber-lab │
│ 192.168.3.0/24 │
│ │
│ │
│ ┌──────────────┐ ┌──────────────┐ │
│ │ │ │ │ │
│ │ Kali │◄────────────►│ Windows │ │
│ │ Linux │ ARP │ 11 │ │
│ │ (Analyst) │ │ (Target) │ │
│ │ │ │ │ │
│ │ 192.168.3.4 │ │192.168.3.12 │ │
│ └──────┬───────┘ └──────┬───────┘ │
│ │ │ │
│ │ │ │
│ ▼ ▼ │
│ ┌──────────────┐ ┌──────────────┐ │
│ │ Nmap │ │ Firewall │ │
│ │ Scans │──────────────►│ (Blocking │ │
│ │ TCP/UDP │ Filtered │ ICMP + │ │
│ │ │ Ports │ Ports) │ │
│ └──────────────┘ └──────────────┘ │
│ │
└─────────────────────────────────────────────────────────────┘




## Traffic Flow Description

| Direction | Protocol | Result |
|-----------|----------|--------|
| Kali → Windows | ICMP (ping) | ❌ Blocked |
| Kali → Windows | ARP | ✅ Allowed |
| Kali → Windows | TCP (common ports) | ❌ Filtered |
| Kali → Windows | UDP (common ports) | ❌ Open/Filtered |

## Security Control Points

1. **Host-based Firewall (Windows Defender)** - Blocks inbound ICMP and port scans
2. **ARP Protocol** - Required for network communication, remains enabled
3. **Internal Network Isolation** - No internet access, controlled environment

## Enterprise Equivalent

This architecture mimics:
- Internal corporate network segment
- Endpoint with default firewall configuration
- Security analyst conducting authorized reconnaissance
