# main.py
import json
from phantomhunt.modules.discovery import discover_assets
from phantomhunt.modules.phase2 import phase2
from rich.console import Console

console = Console()


if __name__ == "__main__":
    console.print("[bold red]PhantomHunt[/] - Stealth Internal Threat Hunter\n")
    console.print(" [1] Silent Discovery")
    console.print(" [2] Priv Esc + Credential Dump")
    console.print(" [3] Domain Enum + Kerberoasting + Lateral")
    console.print(" [4] Generate Full Report")
    choice = input("\nChoose (1-4): ").strip()

    # Persistent variables (stay alive during one run)
    assets = None
    priv_findings = []
    wifi_count = 0
    browser_count = 0
    domain_attempted = False

    if choice == "1":
        console.print("[cyan]Phase 1: Silent Asset Discovery Starting...[/]\n")
        assets = discover_assets()
        print("DEBUG: assets =", assets)
        with open('assets.json', 'w') as f:
            json.dump(assets, f, indent=4)
        console.print("[green]Assets saved to assets.json for report.[/]")
        console.print(f"\n[bold green]Discovery Complete! Found {len(assets or {})} live hosts.[/]")
        console.print("[yellow]Assets saved for report.[/]")

    elif choice == "2":
        #phase2()
        # TODO: later collect real priv_findings, wifi_count, browser_count here

        phase2_data = phase2()  # call and capture return dict
        priv_findings = phase2_data["priv_findings"]
        wifi_count = phase2_data["wifi_count"]
        browser_count = phase2_data["browser_count"]
        console.print("[green]Phase 2 real data captured for report.[/]")


    elif choice == "3":
        # from phantomhunt.modules.phase3 import phase3
        # phase3()
        # domain_attempted = True
        from phantomhunt.modules.phase3 import phase3

        phase3()
        domain_attempted = True
        console.print("[green]Phase 3 data flagged for report.[/]")

    elif choice == "4":
         from phantomhunt.modules.report import generate_report
         try:
            with open('assets.json', 'r') as f:
                loaded_assets = json.load(f)
            console.print("[yellow]Loaded assets from assets.json[/]")
         except FileNotFoundError:
            loaded_assets = {}
            console.print("[red]No assets.json found - using empty data[/]")

         generate_report(
            assets=loaded_assets,
            # priv_findings=priv_findings or [...dummy...],
            # priv_findings=priv_findings or [
            #     {"name": "Print Spooler Running", "status": "Possible", "details": "PrintNightmare / JuicyPotato"},
            #     {"name": "Token Privileges", "status": "VULNERABLE", "details": "Juicy/Rotten Potato possible"}
            # ],
            priv_findings=priv_findings or [],
            wifi_count=wifi_count,
            browser_count=browser_count,
            domain_attempted=domain_attempted
        )
    else:
        console.print("[red]Invalid choice – exiting.[/]")
       # generate_report(
        #     assets=assets,
        #     priv_findings=priv_findings or [  # fallback dummy if none
        #         {"name": "Print Spooler Running", "status": "Possible", "details": "PrintNightmare / JuicyPotato"},
        #         {"name": "Token Privileges", "status": "VULNERABLE", "details": "Juicy/Rotten Potato possible"}
        #     ],
        #     wifi_count=wifi_count,
        #     browser_count=browser_count,
        #     domain_attempted=domain_attempted
        # )


# if __name__ == "__main__":
#     console.print("[bold red]PhantomHunt[/] - Stealth Internal Threat Hunter\n")
#     console.print(" [1] Silent Discovery")
#     console.print(" [2] Priv Esc + Credential Dump")
#     console.print(" [3] Domain Enum + Kerberoasting + Lateral")
#     console.print(" [4] Generate Full Report")
#     choice = input("\nChoose (1-4): ").strip()
#
#     assets = None
#     priv_findings = []  # We'll collect from phase2
#     wifi_count = 0
#     browser_count = 0
#     domain_attempted = False
#
#     # if choice == "1":
#     #     console.print("[cyan]Phase 1: Silent Asset Discovery Starting...[/]\n")
#     #     assets = discover_assets()
#     #     console.print(
#     #         f"\n[bold green]Discovery Complete! Found {len(assets or {})} live hosts.[/]"
#     #     )
#     if choice == "1":
#         console.print("[cyan]Phase 1: Silent Asset Discovery Starting...[/]\n")
#         assets = discover_assets()  # this line already exists
#         console.print(f"\n[bold green]Discovery Complete! Found {len(assets or {})} live hosts.[/]")
#         # NEW: Save the assets for later report
#         console.print("[yellow]Assets saved for report generation.[/]")
#
#     elif choice == "2":
#         # Run phase2 but capture results (modify phase2 to return them)
#         # For now, just run it
#         phase2()
#         # In real: you'd return dict from phase2() and assign here
#
#     elif choice == "3":
#         from phantomhunt.modules.phase3 import phase3
#
#         phase3()
#         domain_attempted = True
#
#     elif choice == "4":
#         from phantomhunt.modules.report import generate_report
#
#         generate_report(
#             assets=assets,
#             priv_findings=[  # Example - expand with real data from phase2
#                 {
#                     "name": "Print Spooler Running",
#                     "status": "Possible",
#                     "details": "PrintNightmare / JuicyPotato",
#                 },
#                 {
#                     "name": "Token Privileges",
#                     "status": "VULNERABLE",
#                     "details": "Juicy/Rotten Potato possible",
#                 },
#             ],
#             wifi_count=0,  # Update after real dump
#             browser_count=0,
#             domain_attempted=domain_attempted,
#         )
#
#     else:
#         console.print("[red]Invalid choice – exiting.[/]")


# main.py
from phantomhunt.modules.discovery import discover_assets
from phantomhunt.modules.phase2 import phase2
from rich.console import Console
#

#
# if __name__ == "__main__":
#     console.print("[bold red]PhantomHunt[/] - Stealth Internal Threat Hunter\n")
#     console.print(" [1] Silent Discovery")
#     console.print(" [2] Priv Esc + Credential Dump")
#     console.print(" [3] Domain Enum + Kerberoasting + Lateral")
#     choice = input("\nChoose (1-3): ").strip()
#
#     if choice == "1":
#         console.print("[cyan]Phase 1: Silent Asset Discovery Starting...[/]\n")
#         assets = discover_assets()
#         console.print(f"\n[bold green]Discovery Complete! Found {len(assets)} live hosts.[/]")
#
#     elif choice == "2":
#         phase2()
#
#     elif choice == "3":
#         from phantomhunt.modules.phase3 import phase3
#         phase3()
#
#     else:
#         console.print("[red]Invalid choice – exiting.[/]")

# if __name__ == "__main__"://phase 2
#     console.print("[bold red]PhantomHunt[/] - Stealth Internal Threat Hunter\n")
#     console.print("[1] Silent Discovery   [2] Priv Esc + Credential Dump")
#     choice = input("\nChoose (1 or 2): ").strip()
#
#     if choice == "1":
#         console.print("[cyan]Phase 1: Silent Asset Discovery Starting...[/]\n")
#         assets = discover_assets()
#         console.print(f"\n[bold green]Discovery Complete! Found {len(assets)} live hosts.[/]")
#
#     elif choice == "2":
#         phase2()
#
#     else:
#         console.print("[red]Invalid choice – exiting.[/]")

# # main.py ---pahse1
# from phantomhunt.modules.discovery import discover_assets
# from rich.console import Console
#
# console = Console()
#
# if __name__ == "__main__":
#     console.print("[bold red]PhantomHunt[/] - Stealth Internal Network Discovery")
#     console.print("[cyan]Phase 1: Silent Asset Discovery Starting...[/]\n")
#     try:
#         assets = discover_assets()
#         console.print(f"\n[bold green]Discovery Complete! Found {len(assets)} live hosts.[/]")
#     except KeyboardInterrupt:
#         console.print("\n[yellow]Stopped by user.[/]")
#     except Exception as e:
#         console.print(f"[red]Error: {e}[/]")
