import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, Scrollbar, scrolledtext
import socket
import ipinfo
import webbrowser
from threading import Thread
import time
import os
from scapy.all import sniff, DHCP, Ether

class NetworkScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Scanner App")
        self.root.geometry("500x550")

        self.verbose = False  # Verbose mode is disabled by default
        self.create_widgets()
        self.setup_logging()

        # Check whether a libpcap provider (Npcap/WinPcap) is available for sniffing
        self.pcap_available = self.check_pcap_provider()
        if not self.pcap_available:
            self.log("WARNING: No libpcap provider available — DHCP sniffing disabled. Install Npcap (https://nmap.org/npcap/) and enable 'WinPcap API-compatible mode' and re-run as Administrator to enable packet capture.")
            # disable DHCP button
            if hasattr(self, 'dhcp_listener_button'):
                try:
                    self.dhcp_listener_button.config(state=tk.DISABLED)
                except Exception:
                    pass

    def create_widgets(self):
        label = tk.Label(self.root, text="Select an action:")
        label.pack(pady=10)

        self.log_display = scrolledtext.ScrolledText(self.root, height=12)
        self.log_display.pack(pady=10)

        port_scan_button = tk.Button(
            self.root, text="1- Port Scan", command=self.port_scan)
        port_scan_button.pack(fill='x', padx=20, pady=2)

        geo_locate_button = tk.Button(
            self.root, text="2- GEOLOCATE IP", command=self.geo_locate)
        geo_locate_button.pack(fill='x', padx=20, pady=2)

        # create dhcp button as an attribute so it can be disabled later
        self.dhcp_listener_button = tk.Button(
            self.root, text="3- DHCP Listener", command=self.dhcp_listener)
        self.dhcp_listener_button.pack(fill='x', padx=20, pady=2)

        self.verbose_var = tk.BooleanVar()
        verbose_button = tk.Checkbutton(
            self.root, text="Verbose Mode", variable=self.verbose_var, command=self.toggle_verbose)
        verbose_button.pack(pady=10)

    def setup_logging(self):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        self.log_file = os.path.join("logs", "network_scan.log")

    def log(self, message):
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
        entry = f"{timestamp} {message}"
        with open(self.log_file, "a") as f:
            f.write(entry + "
")
        self.log_display.insert(tk.END, entry + "
")
        self.log_display.see(tk.END)

    def toggle_verbose(self):
        self.verbose = bool(self.verbose_var.get())

    def port_scan(self):
        host = simpledialog.askstring("Input", "Enter the host to scan:")

        port_selection_window = tk.Toplevel(self.root)
        port_selection_window.title("Select Ports")
        port_selection_window.geometry("300x400")
        port_selection_window.transient(self.root)

        port_list = [
            (20, "FTP Data"), (21, "FTP Control"), (22, "SSH"), (23, "Telnet"),
            (25, "SMTP"), (53, "DNS"), (80, "HTTP"), (110, "POP3"),
            (143, "IMAP"), (443, "HTTPS"), (3306, "MySQL"), (5432, "PostgreSQL"),
            (6379, "Redis"), (11211, "Memcached"), (27017, "MongoDB"), (3389, "RDP"),
            (8080, "HTTP-Alt"), (8443, "HTTPS-Alt")
        ]

        # listbox with multi-select and protocol names
        lb_frame = tk.Frame(port_selection_window)
        lb_frame.pack(fill='both', expand=True, padx=10, pady=10)

        scrollbar = Scrollbar(lb_frame)
        scrollbar.pack(side='right', fill='y')

        listbox = Listbox(lb_frame, selectmode='multiple', yscrollcommand=scrollbar.set)
        for port, name in port_list:
            listbox.insert(tk.END, f"{port} - {name}")
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=listbox.yview)

        custom_label = tk.Label(port_selection_window, text="Or enter ports/range (e.g. 22,80,443 or 1-1024):")
        custom_label.pack(padx=10, pady=(0,5))
        custom_entry = tk.Entry(port_selection_window)
        custom_entry.pack(fill='x', padx=10)

        def select_ports():
            selected = listbox.curselection()
            selected_ports = [port_list[i][0] for i in selected]
            custom = custom_entry.get().strip()
            if custom:
                try:
                    if '-' in custom:
                        s,e = map(int, custom.split('-'))
                        selected_ports.extend(list(range(s, e+1)))
                    else:
                        for p in custom.split(','):
                            selected_ports.append(int(p.strip()))
                except ValueError:
                    messagebox.showerror('Invalid input', 'Custom ports entry is invalid')
                    return

            if not selected_ports:
                messagebox.showwarning('No ports', 'No ports selected. Using common ports.')
                selected_ports = [22,80,443,3306]

            port_selection_window.destroy()
            self.log(f"Starting port scan on {host} for ports: {selected_ports}")
            # run scan in background
            Thread(target=self._run_port_scan, args=(host, selected_ports), daemon=True).start()

        submit_button = tk.Button(port_selection_window, text="Start Scan", command=select_ports)
        submit_button.pack(pady=8)

    def _run_port_scan(self, host, ports):
        result = self.scan_ports(host, ports)
        # show modal with results
        messagebox.showinfo("Scan Results", result)
        self.log(result)

    def scan_ports(self, host, ports):
        open_ports = []
        for port in ports:
            try:
                s = socket.socket()
                s.settimeout(1.0)
                s.connect((host, port))
                open_ports.append((port, "Open"))
                if self.verbose:
                    self.log(f"Port {port} is Open")
            except Exception:
                open_ports.append((port, "Closed"))
                if self.verbose:
                    self.log(f"Port {port} is Closed")
            finally:
                try:
                    s.close()
                except Exception:
                    pass

        result = "Scan Results:
"
        for port, status in open_ports:
            result += f"Port {port}: {status}
"

        return result

    def geo_locate(self):
        geotarget = simpledialog.askstring("Input", "What IP would you like to geolocate?")
        access_token = '58a0d309242449'
        handler = ipinfo.getHandler(access_token)
        try:
            details = handler.getDetails(geotarget)
        except Exception as e:
            self.log(f"IPInfo error: {e}")
            messagebox.showerror('Error', 'Failed to get geolocation data')
            return

        # some responses don't include loc — handle safely
        loc = getattr(details, 'loc', None)
        if loc:
            latitude, longitude = loc.split(',')
            result = f"Geolocation for IP {geotarget}:
"
            result += f"Location: {getattr(details, 'city', 'N/A')}, {getattr(details, 'region', 'N/A')}, {getattr(details, 'country', 'N/A')}
"
            result += f"Coordinates: {latitude}, {longitude}"
            webbrowser.open(f"https://www.google.com/maps?q={latitude},{longitude}")
        else:
            result = f"No location data available for IP {geotarget}."

        messagebox.showinfo("Geolocation Results", result)
        self.log(result)

    def dhcp_listener(self):
        if not self.pcap_available:
            messagebox.showerror('PCAP Missing', 'Npcap/WinPcap not found. DHCP listening is disabled. Install Npcap and re-run with administrator privileges.')
            return

        self.waiting_window = tk.Toplevel(self.root)
        self.waiting_window.title("DHCP Listener")
        label = tk.Label(self.waiting_window, text="Listening for DHCP requests...")
        label.pack(pady=10)

        def process_packet(packet):
            try:
                if packet.haslayer(DHCP):
                    mac = packet[Ether].src
                    options = packet[DHCP].options
                    requested_ip = next((item[1] for item in options if item[0] == "requested_addr"), "Unknown")
                    hostname = next((item[1].decode() for item in options if item[0] == "hostname"), "Unknown")
                    vendor_id = next((item[1].decode() for item in options if item[0] == "vendor_class_id"), "Unknown")
                    result = f"DHCP Request: {mac} - {hostname} / {vendor_id} requested {requested_ip}"
                    self.log(result)
            except Exception as e:
                self.log(f"Error processing packet: {e}")

        try:
            dhcp_thread = Thread(target=lambda: sniff(filter='udp and (port 67 or port 68)', prn=process_packet), daemon=True)
            dhcp_thread.start()
        except OSError as e:
            self.log(f"Failed to start sniffing: {e}")
            messagebox.showerror('Sniffing error', 'Failed to start packet capture. Ensure Npcap is installed and you have the required privileges.')

    def check_pcap_provider(self):
        # simple check: try to import pcapy or check scapy conf
        try:
            import pcapy
            return True
        except Exception:
            # pcapy not available — try reading scapy's conf
            try:
                from scapy.all import conf
                return getattr(conf, 'use_pcap', False)
            except Exception:
                return False


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkScannerApp(root)
    root.mainloop()
    root = tk.Tk()
    app = NetworkScannerApp(root)
    root.mainloop()