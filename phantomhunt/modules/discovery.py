# phantomhunt/modules/discovery.py
import socket
import subprocess
import os
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp

from netaddr import IPNetwork
from rich.console import Console
from rich.table import Table
import logging

console = Console()
logging.basicConfig(level=logging.INFO)


def get_local_network():
    """Auto detect local subnet (e.g., 192.168.1.0/24)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except:
        ip = "192.168.1.100"
    finally:
        s.close()

    # Simple /24 assumption (works 99% in labs)
    network = ".".join(ip.split(".")[:-1]) + ".0/24"
    return network, ip


def arp_scan(network):
    """Super silent ARP scan - only sends to live hosts"""
    console.print("[bold blue]Running silent ARP discovery...[/]")
    request = ARP(pdst=network)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / request

    # answered, _ = scapy.all.srp(arp_request_broadcast, timeout=2, verbose=0)
    answered, _ = srp(arp_request_broadcast, timeout=2, verbose=0)
    hosts = []
    for sent, received in answered:
        hosts.append({'ip': received.psrc, 'mac': received.hwsrc})
    return hosts


def get_hostname(ip):
    """Try to resolve hostname silently"""
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unknown"


def discover_assets():
    network, local_ip = get_local_network()
    console.print(f"[bold]Local IP:[/] {local_ip}")
    console.print(f"[bold]Scanning network:[/] {network}\n")

    hosts = arp_scan(network)

    table = Table(title="Discovered Assets (Silent Mode)", show_header=True, header_style="bold magenta")
    table.add_column("IP Address")
    table.add_column("MAC Address")
    table.add_column("Hostname")
    table.add_column("Status")

    discovered = {}
    for host in hosts:
        ip = host['ip']
        mac = host['mac']
        hostname = get_hostname(ip)
        table.add_row(ip, mac, hostname, "[green]Alive[/]")
        discovered[ip] = {"mac": mac, "hostname": hostname, "status": "alive"}

    console.print(table)
    console.print(f"\n[bold yellow]Total live hosts found: {len(hosts)}[/]")

    return discovered


if __name__ == "__main__":
    discover_assets()