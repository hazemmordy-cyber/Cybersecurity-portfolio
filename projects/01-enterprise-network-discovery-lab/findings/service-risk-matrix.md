# Service Risk Matrix

## Assessment Summary

| Service | Port | Protocol | State | Risk Level | Risk Reason |
|---------|------|----------|-------|------------|-------------|
| msrpc | 135 | TCP | Filtered | Low | Blocked by firewall; no direct exposure |
| netbios-ssn | 139 | TCP | Filtered | Low | Legacy Windows service; blocked |
| microsoft-ds | 445 | TCP | Filtered | Low | SMB blocked; prevents lateral movement |
| ms-wbt-server | 3389 | TCP | Filtered | Low | RDP blocked; remote access protected |
| Various UDP | Top 100 | UDP | Open/Filtered | Low-Medium | UDP scanning inconclusive; potential exposure |

---

## Risk Level Definitions

| Level | Description |
|-------|-------------|
| Critical | Exploitable remotely; no authentication required; widespread impact |
| High | Easily exploitable; significant impact on confidentiality/integrity/availability |
| Medium | Requires specific conditions; limited impact or difficult exploitation |
| Low | Minimal risk; requires multiple additional vulnerabilities |
| Informational | No immediate risk; useful for situational awareness |

---

## Detailed Analysis

### 1. msrpc (135/tcp) — Risk: LOW

**Why it matters:**
- Used for remote procedure calls between Windows systems
- Can be exploited for enumeration and certain RCE vulnerabilities (e.g., EternalBlue variants)

**Why risk is LOW in this assessment:**
- Port is **filtered** (firewall blocking inbound connections)
- Not reachable from the analyst machine

**Enterprise impact:** Minimal — default Windows Firewall configuration blocks external access

---

### 2. netbios-ssn (139/tcp) — Risk: LOW

**Why it matters:**
- Legacy NetBIOS name service
- Often targeted for enumeration and SMB relay attacks

**Why risk is LOW in this assessment:**
- Firewall is filtering inbound traffic
- No response received during scanning

**Enterprise impact:** Legacy protocol exposure is prevented by current firewall rules

---

### 3. microsoft-ds (445/tcp) — Risk: LOW

**Why it matters:**
- Modern SMB protocol for file sharing and named pipes
- Historically targeted by major vulnerabilities (EternalBlue, WannaCry, NotPetya)

**Why risk is LOW in this assessment:**
- SMB ports are **filtered** — not accessible
- Cannot be exploited remotely with current configuration

**Enterprise impact:** Critical service properly protected by host-based firewall

---

### 4. ms-wbt-server (3389/tcp) — Risk: LOW

**Why it matters:**
- Remote Desktop Protocol (RDP)
- High-value target for remote access and brute force attacks

**Why risk is LOW in this assessment:**
- RDP port is **filtered** — no external access
- Cannot be reached for authentication attempts

**Enterprise impact:** Remote access properly restricted at host level

---

### 5. UDP Ports (Top 100) — Risk: LOW-MEDIUM

**Why it matters:**
- UDP services (DNS, NTP, SNMP, NetBIOS) can be exploited for amplification attacks
- UDP scanning results are often ambiguous (open|filtered)

**Why risk is LOW-MEDIUM in this assessment:**
- No response to UDP probes (typical firewall behavior)
- Cannot confirm if services are truly exposed
- Potential for UDP-based reconnaissance

**Enterprise impact:** Lower confidence in UDP exposure status; requires further investigation

---

## Risk Trend

| Category | Status | Trend |
|----------|--------|-------|
| TCP Service Exposure | ✅ Contained | Stable |
| UDP Service Exposure | ⚠️ Unknown | Investigate |
| Firewall Effectiveness | ✅ Strong | Maintain |
| Attack Surface Reduction | ✅ Successful | Complete |

---

## Remediation Priorities

| Priority | Action | Owner | Timeline |
|----------|--------|-------|----------|
| 1 | Maintain current Windows Firewall rules | IT Security | Ongoing |
| 2 | Investigate UDP response behavior | Network Team | 1 week |
| 3 | Enable firewall logging for detection | SOC | 2 weeks |
| 4 | Consider network segmentation | Network Architecture | 1 month |

---

## Summary Statement

The target system (Windows 11) demonstrates a **mature security baseline** with no exploitable services exposed to the internal network from the scanning perspective. All critical Windows services (SMB, RDP, RPC) are properly filtered by the host-based firewall. The only residual risk is the inconclusive UDP state, which requires further investigation but poses low immediate threat.

## Interpretation

The identified services represent potential entry points that should be reviewed as part of a defensive security strategy.

Risk ratings were assigned based on exposure level, common attacker interest, and potential misuse scenarios.
