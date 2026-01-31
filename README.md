# PhantomHunt

**Stealth Internal Network Threat Hunter**  
A final-year cybersecurity project built in Python that performs silent asset discovery, privilege escalation checks, credential dumping, domain simulation, and generates professional MITRE ATT&CK-mapped reports.

**Demo GIF / Screenshot** (add one later when you have the report PDF open)  
![PhantomHunt Report Demo](reports/screenshot-report.png)  
*(Placeholder – replace with actual screenshot of your generated PDF/HTML report)*

## Features

- **Silent Asset Discovery** — Uses ARP scanning (no noisy Nmap/ICMP) to find live hosts on local network
- **Privilege Escalation Detection** — Checks common Windows LPE vectors (Print Spooler, AlwaysInstallElevated, SeImpersonate, etc.)
- **Credential Access** — Dumps saved Wi-Fi passwords and browser credentials (Chrome/Edge)
- **Domain & AD Simulation** — Basic domain enumeration + Kerberoasting/lateral movement placeholders (safe demo mode)
- **Beautiful Reports** — Generates HTML + PDF reports with MITRE ATT&CK tags, timelines, and risk summary
- **Stealth-focused** — Designed to be low-noise and educational (no real destructive actions by default)

## Tech Stack

- Python 3.10+
- Libraries: `rich`, `scapy`, `impacket`, `pywin32`, `jinja2`, `weasyprint`, `netaddr`, `pycryptodome`
- Runs on Windows (tested), partial Linux support possible

## Installation

1. **Prerequisites**  
   - Python 3.10+  
   - Npcap (for Scapy raw packets) → https://npcap.com/ (install with WinPcap compatibility checked)  
   - WeasyPrint dependencies → Install MSYS2 + Pango (see below)

2. **Clone the repo**
   ```bash
   git clone https://github.com/hawk1411/PhantomHunt.git
   cd PhantomHunt
3.Create & activate virtual environmentBashpython -m venv venv
```
venv\Scripts\activate    # Windows
# source venv/bin/activate   # Linux/macOS
```
