# phantomhunt/modules/report.py
import datetime
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import socket
from rich.console import Console

console = Console()

def generate_report(assets=None, priv_findings=None, wifi_count=0, browser_count=0, domain_attempted=False):
    """Generate HTML + PDF report"""
    print("DEBUG in report.py: assets =", assets)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    local_ip = socket.gethostbyname(socket.gethostname())
    network = ".".join(local_ip.split(".")[:-1]) + ".0/24"  # simple guess

    # Default empty if not provided
    assets = assets or {}
    priv_findings = priv_findings or []

    # Add MITRE mappings (expand later)
    for finding in priv_findings:
        if "Print Spooler" in finding.get("name", ""):
            finding["mitre"] = "T1547.012 / T1068 (Exploitation for Privilege Escalation)"
        elif "Token Privileges" in finding.get("name", ""):
            finding["mitre"] = "T1134.001 (Access Token Manipulation)"
        else:
            finding["mitre"] = "T1068"

    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', '..', 'reports')))
    template = env.get_template('report_template.html')

    html_content = template.render(
        timestamp=timestamp,
        local_ip=local_ip,
        network=network,
        assets=assets,
        priv_findings=priv_findings,
        wifi_count=wifi_count,
        browser_count=browser_count,
        domain_attempted=domain_attempted
    )

    # Save HTML
    html_path = "reports/phantomhunt_report.html"
    os.makedirs("reports", exist_ok=True)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Generate PDF
    pdf_path = "reports/phantomhunt_report.pdf"
    HTML(string=html_content).write_pdf(pdf_path)

    console.print(f"[bold green]Report generated![/]")
    console.print(f"HTML: {os.path.abspath(html_path)}")
    console.print(f"PDF:  {os.path.abspath(pdf_path)}")