import socket
import time
from scapy.all import Ether, DHCP, sniff
import ipinfo


def scan_ports(host, ports):
    open_ports = []
    for port in ports:
        try:
            s = socket.socket()
            s.connect((host, port))
        except:
            open_ports.append((port, "Closed"))
        else:
            open_ports.append((port, "Open"))
        finally:
            s.close()

    result = "Scan Results:\n"
    for port, status in open_ports:
        result += f"Port {port}: {status}\n"

    return result


def geo_locate(geotarget):
    access_token = '58a0d309242449'
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
