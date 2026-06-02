#!/usr/bin/env python3
"""
Security Port Auditor - A lightweight TCP port scanner for isolated lab environments.
"""

import socket
import json
import csv
import argparse
from datetime import datetime

# Default common TCP ports (Windows + Linux + general)
COMMON_PORTS = [
    21,    # FTP
    22,    # SSH
    23,    # Telnet
    25,    # SMTP
    53,    # DNS
    80,    # HTTP
    110,   # POP3
    135,   # RPC
    139,   # NetBIOS
    143,   # IMAP
    443,   # HTTPS
    445,   # SMB
    993,   # IMAPS
    995,   # POP3S
    1433,  # MSSQL
    3306,  # MySQL
    3389,  # RDP
    5432,  # PostgreSQL
    5900,  # VNC
    8080,  # HTTP-Alt
]

def scan_port(target, port, timeout=1.0):
    """
    Attempt a TCP connection to a single port.
    Returns dict with target, port, state, and optional service banner.
    """
    result = {
        "target": target,
        "port": port,
        "state": "closed",
        "service_banner": ""
    }
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            if sock.connect_ex((target, port)) == 0:
                result["state"] = "open"
                # Try simple banner grabbing
                try:
                    sock.settimeout(2.0)
                    banner = sock.recv(256).decode('utf-8', errors='ignore').strip()
                    result["service_banner"] = banner.replace('\n', ' ').replace('\r', '')
                except Exception:
                    pass  # No banner available
    except socket.gaierror:
        result["state"] = "invalid_target"
    except Exception:
        pass
    return result

def save_json(results, filename):
    """Save scan results as JSON."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

def save_csv(results, filename):
    """Save scan results as CSV."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["target", "port", "state", "service_banner"])
        writer.writeheader()
        writer.writerows(results)

def print_summary(results):
    """Print a human‑friendly summary to console."""
    open_ports = [r for r in results if r["state"] == "open"]
    print("\n" + "="*50)
    print(f"Scan completed for {results[0]['target']}")
    print(f"Total ports checked: {len(results)}")
    print(f"Open ports: {len(open_ports)}")
    if open_ports:
        print("Open ports details:")
        for r in open_ports:
            banner_preview = (r["service_banner"][:50] + "...") if len(r["service_banner"]) > 50 else r["service_banner"]
            print(f"  {r['port']}/tcp -> banner: {banner_preview if banner_preview else '(none)'}")
    else:
        print("No open ports discovered.")
    print("="*50)

def main():
    parser = argparse.ArgumentParser(
        description="Security Port Auditor – Lightweight TCP port scanner for lab environments.",
        epilog="Example: python port_auditor.py 192.168.3.12\n"
               "         python port_auditor.py 192.168.3.12 --ports 22,80,443"
    )
    parser.add_argument("target", help="Target IP address (e.g., 192.168.3.12)")
    parser.add_argument("--ports", help="Comma-separated port numbers (default: common ports list)", default="")
    parser.add_argument("--timeout", type=float, default=1.0, help="Socket timeout in seconds (default 1.0)")
    args = parser.parse_args()

    # Determine which ports to scan
    if args.ports:
        try:
            ports = [int(p.strip()) for p in args.ports.split(",") if p.strip().isdigit()]
        except ValueError:
            print("Error: --ports must be comma-separated numbers.")
            return
    else:
        ports = COMMON_PORTS

    print(f"Starting port scan on {args.target} with timeout {args.timeout}s")
    results = []
    for port in ports:
        res = scan_port(args.target, port, timeout=args.timeout)
        results.append(res)
        # Real-time feedback
        if res["state"] == "open":
            print(f"✓ {port}/tcp -> open")
        elif res["state"] == "closed":
            print(f"✗ {port}/tcp -> closed")
        else:
            print(f"! {port}/tcp -> {res['state']}")

    # Save outputs with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    import os
    os.makedirs("outputs", exist_ok=True)
    json_file = f"outputs/scan_{args.target}_{timestamp}.json"
    csv_file = f"outputs/scan_{args.target}_{timestamp}.csv"
    save_json(results, json_file)
    save_csv(results, csv_file)

    print_summary(results)
    print(f"JSON output saved to: {json_file}")
    print(f"CSV output saved to: {csv_file}")

if __name__ == "__main__":
    main()
