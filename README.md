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
3. **Create & activate virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate    # Windows
   # source venv/bin/activate   # Linux/macOS
4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
5. **Install WeasyPrint native dependencies (Windows only)**

   Install MSYS2: https://www.msys2.org/
   
   Open MSYS2 MinGW 64-bit shell:

   ```bash
   pacman -Syu --noconfirm
   pacman -S mingw-w64-x86_64-pango --noconfirm```

 set WEASYPRINT_DLL_DIRECTORIES=C:\msys64\mingw64\bin
 pip install weasyprint

6. **Run the tool**

   ```bash
   python main.py
7. **Usage Demo**
   
   ```text
   PhantomHunt - Stealth Internal Threat Hunter
   
   [1] Silent Discovery
   [2] Priv Esc + Credential Dump
   [3] Domain Enum + Kerberoasting + Lateral
   [4] Generate Full Report
   
   Choose (1-4):
8. **Project Structure**

   ```text
   PhantomHunt/
   ├── main.py                 # CLI entry point + menu
   ├── requirements.txt
   ├── phantomhunt/
   │   ├── modules/
   │   │   ├── discovery.py    # Phase 1: Silent ARP discovery
   │   │   ├── phase2.py       # Phase 2: Priv esc + credential dump
   │   │   ├── phase3.py       # Phase 3: Domain + Kerberoast + lateral sim
   │   │   └── report.py       # Report generation (HTML + PDF)
   │   └── resources/
   │       └── report_template.html
   ├── reports/                # Generated reports + template
   ├── assets.json             # Saved discovery data (optional)
   └── venv/                   # Virtual environment (not committed)
8. **Future Improvements (Planned)**

   - Add JSON persistence for Phase 2 & Phase 3 findings
   - More privilege escalation checks (weak services, unquoted paths, UAC bypass, etc.)
   - Real Impacket integration for Kerberoasting & lateral movement (lab-only)
   - Add evasion techniques & C2 simulation
   - Docker support for easy lab deployment

9. **License**

    MIT License – see LICENSE file

10. **Author**

   Ravi (hawk1411)  
   Final Year Cybersecurity Project – 2025–2026

**Built with ❤️ for learning red-team techniques and threat hunting.**
**Star ⭐ if you find it useful!**


   







