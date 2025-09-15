import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import socket
import ipinfo
import webbrowser
from threading import Thread
import os
from datetime import datetime
from scapy.all import sniff, DHCP, Ether
from net_scan import scan_ports  # Import the scan_ports function from net_scan.py
from tkinter import ttk


class NetworkScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Scanner App")
        self.root.geometry("600x600")

        self.verbose = False  # Verbose mode is disabled by default
        self.create_widgets()
        self.setup_logging()

    def create_widgets(self):
        label = tk.Label(self.root, text="Select an action:")
        label.pack(pady=10)

        self.log_display = scrolledtext.ScrolledText(self.root, height=10)
        self.log_display.pack(pady=10)

        port_scan_button = tk.Button(
            self.root, text="1- Port Scan", command=self.port_scan)
        port_scan_button.pack()

        geo_locate_button = tk.Button(
            self.root, text="2- GEOLOCATE IP", command=self.geo_locate)
        geo_locate_button.pack()

        dhcp_listener_button = tk.Button(
            self.root, text="3- DHCP Listener", command=self.dhcp_listener)
        dhcp_listener_button.pack()

        verbose_button = tk.Checkbutton(
            self.root, text="Verbose Mode", command=self.toggle_verbose)
        verbose_button.pack(pady=10)

        # Progress bar for scanning
        self.progress_bar = ttk.Progressbar(
            self.root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

    def setup_logging(self):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        self.log_file = os.path.join("logs", "network_scan.log")

    def log(self, message):
        with open(self.log_file, "a") as f:
            f.write(message + "\n")
        self.log_display.insert(tk.END, message + "\n")
        self.log_display.see(tk.END)

    def toggle_verbose(self):
        self.verbose = not self.verbose

    def port_scan(self):
        host = simpledialog.askstring("Input", "Enter the host to scan:")

        port_selection_window = tk.Toplevel(self.root)
        port_selection_window.title("Select Ports")

        port_list = [
            (20, "FTP Data"), (21, "FTP Control"), (22, "SSH"), (23, "Telnet"),
            (25, "SMTP"), (53, "DNS"), (80, "HTTP"), (110, "POP3"),
            (143, "IMAP"), (443, "HTTPS"), (3306, "MySQL"), (5432, "PostgreSQL"),
            (6379, "Redis"), (11211, "Memcached"), (27017, "MongoDB"), (3389, "RDP"),
            (21, "FTP"), (22, "SSH"), (25, "SMTP"), (53, "DNS"), (80, "HTTP"),
            (443, "HTTPS"), (8080, "HTTP Alt"), (3306, "MySQL"), (5432, "PostgreSQL")
        ]

        selected_ports = []
        all_ports_selected = tk.BooleanVar()

        def select_ports():
            if all_ports_selected.get():
                selected_ports.extend(range(1, 65536))  # Select all ports
            else:
                for i in range(len(port_list)):
                    if port_checkboxes[i].get():
                        selected_ports.append(port_list[i][0])
            port_selection_window.destroy()
            self.start_scan_thread(host, selected_ports)

        port_checkboxes = []
        select_all_checkbox = tk.Checkbutton(port_selection_window,
                                             text="Select All Ports (1-65535)", variable=all_ports_selected)
        select_all_checkbox.pack(anchor='w')

        for port, name in port_list:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(port_selection_window,
                                 text=f"{port} - {name}", variable=var)
            chk.pack(anchor='w')
            port_checkboxes.append(var)

        submit_button = tk.Button(
            port_selection_window, text="Start Scan", command=select_ports)
        submit_button.pack()

    def start_scan_thread(self, host, selected_ports):
        # Reset progress bar
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = len(selected_ports)

        # Start the scan thread
        scan_thread = Thread(target=self.run_scan, args=(host, selected_ports))
        scan_thread.start()

    def run_scan(self, host, selected_ports):
        # Log the start time
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log(f"Scan started at {start_time}")
        self.log(f"Scanning host: {host}")
        self.update_gui(f"Scan started at {start_time}")

        open_ports = []
        for i, port in enumerate(selected_ports):
            try:
                s = socket.socket()
                s.connect((host, port))
                open_ports.append((port, "Open"))
                if self.verbose:
                    verbose_message = f"Scanning port {port}... Open"
                    self.log(verbose_message)
                    # Show verbose message in GUI
                    self.update_gui(verbose_message)
            except Exception as e:
                open_ports.append((port, "Closed"))
                if self.verbose:
                    verbose_message = f"Scanning port {port}... Closed"
                    self.log(verbose_message)
                    # Show verbose message in GUI
                    self.update_gui(verbose_message)
            finally:
                s.close()

            # Update progress bar
            self.progress_bar['value'] = i + 1
            self.root.update_idletasks()  # Update the UI

        # Log the end time
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log(f"Scan ended at {end_time}")
        self.update_gui(f"Scan ended at {end_time}")

        # Show the results
        result = "Scan Results:\n"
        for port, status in open_ports:
            result += f"Port {port}: {status}\n"

        messagebox.showinfo("Scan Results", result)
        self.log(result)

    def update_gui(self, message):
        self.log_display.insert(tk.END, message + "\n")
        self.log_display.see(tk.END)

    def geo_locate(self):
        geotarget = simpledialog.askstring(
            "Input", "What IP would you like to geolocate?")
        access_token = '58a0d309242449'
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails(geotarget)

        if hasattr(details, 'loc') and details.loc:
            latitude, longitude = details.loc.split(',')
            result = f"Geolocation for IP {geotarget}:\n"
            result += f"Location: {details.city}, {details.region}, {details.country}\n"
            result += f"Coordinates: {latitude}, {longitude}"
            webbrowser.open(
                f"https://www.google.com/maps?q={latitude},{longitude}")
        else:
            result = f"No location data available for IP {geotarget}."

        messagebox.showinfo("Geolocation Results", result)
        self.log(result)

    def dhcp_listener(self):
        self.waiting_window = tk.Toplevel(self.root)
        self.waiting_window.title("DHCP Listener")
        label = tk.Label(self.waiting_window, text="Listening for DHCP requests...")
        label.pack(pady=10)

        def process_packet(packet):
            if packet.haslayer(DHCP):
                mac = packet[Ether].src
                options = packet[DHCP].options
                requested_ip = next(
                    (item[1] for item in options if item[0] == "requested_addr"), "Unknown")
                hostname = next(
                    (item[1].decode() for item in options if item[0] == "hostname"), "Unknown")
                vendor_id = next(
                    (item[1].decode() for item in options if item[0] == "vendor_class_id"), "Unknown")
                result = f"DHCP Request: {mac} - {hostname} / {vendor_id} requested {requested_ip}"
                self.log(result)

        dhcp_thread = Thread(target=lambda: sniff(
            filter='udp and (port 67 or port 68)', prn=process_packet))
        dhcp_thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkScannerApp(root)
    root.mainloop()
