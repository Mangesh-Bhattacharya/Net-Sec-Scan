import os
import socket
import time
from scapy.all import Ether, DHCP, sniff
import ipinfo
import requests


def scan_ports(host, ports, verbose=False):
    open_ports = []
    for port in ports:
        try:
            s = socket.socket()
            s.connect((host, port))
            status = "Open"
            if verbose:
                # Detailed info about the service could be added here
                service_info = get_service_info(port)
                open_ports.append((port, status, service_info))
            else:
                open_ports.append((port, status))
        except:
            open_ports.append((port, "Closed"))
        finally:
            s.close()

    result = "Scan Results:\n"
    for port, status, *service_info in open_ports:
        result += f"Port {port}: {status}\n"
        if verbose and service_info:
            result += f"Service Info: {service_info[0]}\n"

    return result


def get_service_info(port):
    # Simulate fetching CVE information (could use a real CVE API)
    service_info = {
        80: "HTTP - Common web server, CVE-2021-22940",
        443: "HTTPS - Secure HTTP, CVE-2020-0601",
        22: "SSH - Secure Shell, CVE-2018-15473",
        3306: "MySQL - Database service, CVE-2019-2890",
    }
    return service_info.get(port, "No specific service info available")


def geo_locate(geotarget):
    access_token = os.environ.get("IPINFO_ACCESS_TOKEN")
    if not access_token:
        raise RuntimeError(
            "Set the IPINFO_ACCESS_TOKEN environment variable to use geolocation "
            "(see README for setup instructions)."
        )
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(geotarget)

    result = f"Geolocation for IP {geotarget}:\n"
    for key, value in details.all.items():
        result += f"{key}: {value}\n"

    return result


def start_dhcp_sniffing(callback):
    sniff(prn=callback, filter='udp and (port 67 or port 68)')


def listen_dhcp_packets(callback):
    def print_packet(packet):
        target_mac, requested_ip, hostname, vendor_id = [None] * 4
        if packet.haslayer(Ether):
            target_mac = packet.getlayer(Ether).src
        dhcp_options = packet[DHCP].options
        for item in dhcp_options:
            try:
                label, value = item
            except ValueError:
                continue
            if label == "requested_addr":
                requested_ip = value
            elif label == "hostname":
                hostname = value.decode()
            elif label == "vendor_class_id":
                vendor_id = value.decode()

        if target_mac and vendor_id and hostname and requested_ip:
            time_now = time.strftime("[%Y-%m-%d  - %H:%M:%S]")
            result = f"{time_now}: {target_mac} - {hostname} / {vendor_id} requested {requested_ip}"
            callback(result)

    start_dhcp_sniffing(print_packet)
