import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, Scrollbar
import socket
import ipinfo
import webbrowser
from threading import Thread
import time


class NetworkScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Scanner App")
        self.root.geometry("400x400")

        self.verbose = False  # Verbose mode is disabled by default

        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self.root, text="Select an action:")
        label.pack(pady=10)

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

    def toggle_verbose(self):
        # Toggle the verbose flag when the checkbox is checked or unchecked
        self.verbose = not self.verbose

    def port_scan(self):
        host = simpledialog.askstring("Input", "Enter the host to scan:")

        # Predefined common ports for scanning
        common_ports = [
            20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 8080, 3306, 5432, 6379, 11211, 27017, 3389, 8081
        ]

        port_range = simpledialog.askstring(
            "Input", "Enter a port number or range (e.g., 80-443, 22, 8080):")

        selected_ports = []
        if port_range:
            try:
                if '-' in port_range:  # If range is specified, like 80-443
                    start_port, end_port = map(int, port_range.split('-'))
                    selected_ports = [p for p in range(
                        start_port, end_port + 1)]
                else:
                    # If individual ports are selected, split by commas
                    selected_ports = [int(p.strip())for p in port_range.split(',')]
            except ValueError as e:
                messagebox.showerror(
                    "Invalid Input", f"Invalid port range or numbers: {str(e)}")
                return

        # Show list of predefined common ports if no valid input was provided
        if not selected_ports:
            selected_ports = common_ports

        result = self.scan_ports(host, selected_ports)
        messagebox.showinfo("Scan Results", result)

    def scan_ports(self, host, ports):
        open_ports = []

        if self.verbose:
            print(f"Scanning ports for host: {host}")
            print(f"Ports to scan: {ports}")

        for port in ports:
            try:
                s = socket.socket()
                s.connect((host, port))
                open_ports.append((port, "Open"))
                if self.verbose:
                    print(f"Port {port} is Open")
            except:
                open_ports.append((port, "Closed"))
                if self.verbose:
                    print(f"Port {port} is Closed")
            finally:
                s.close()

        result = "Scan Results:\n"
        for port, status in open_ports:
            result += f"Port {port}: {status}\n"

        return result

    def geo_locate(self):
        geotarget = simpledialog.askstring(
            "Input", "What IP would you like to geolocate?")

        # Get geolocation details
        access_token = '58a0d309242449'  # Replace with your access token
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails(geotarget)

        # Extract latitude and longitude
        latitude = details.loc.split(',')[0]
        longitude = details.loc.split(',')[1]

        # Display result
        result = f"Geolocation for IP {geotarget}:\n"
        result += f"Location: {details.city}, {details.region}, {details.country}\n"
        result += f"Coordinates: {latitude}, {longitude}"

        messagebox.showinfo("Geolocation Results", result)

        if self.verbose:
            print(f"Geolocating IP: {geotarget}")
            print(f"Latitude: {latitude}, Longitude: {longitude}")

        # Open Google Maps with the coordinates
        google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
        webbrowser.open(google_maps_url)

    def dhcp_listener(self):
        self.waiting_window = tk.Toplevel(self.root)
        self.waiting_window.title("Please wait...")
        label = tk.Label(self.waiting_window, text="Listening for DHCP requests. Please wait...")
        label.pack(pady=10)

        def show_dhcp_result(result):
            if self.verbose:
                print("DHCP request detected:", result)
            self.waiting_window.destroy()
            messagebox.showinfo("DHCP Listener Results", result)

        # This method would use the listener function you've defined elsewhere (e.g., listen_dhcp_packets)
        listen_dhcp_packets(show_dhcp_result)


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkScannerApp(root)
    root.mainloop()
