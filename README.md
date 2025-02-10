# Network Scanner App

A state-of-the-art, real-time **Network Scanner App** that provides functionalities like port scanning, geolocation lookup, and DHCP packet listening. It’s designed to help network administrators, security professionals, and enthusiasts analyze and troubleshoot networks easily.

## 📦 Features

- **Port Scanning**: Scan a range of ports on a given host and check which ports are open or closed.
- **Geolocation Lookup**: Retrieve geolocation data for any given IP address, including details such as location, city, and region.
- **DHCP Listener**: Listen for DHCP requests and capture details such as MAC addresses, requested IPs, and hostnames.

## 📂 Installation

### Prerequisites

Make sure you have Python 3.6 or higher installed on your machine. You will also need `pip` to install dependencies.

1. Clone the repository:
   ```bash
   git clone https://github.com/Mangesh-Bhattacharya/Net-Sec-Scan.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Net-Sec-Scan
   ```

3. Create a virtual environment (recommended):
   ```bash
   python -m venv env
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Geolocation API Key

To use the **geolocation lookup** feature, you will need to set up an API key from [ipinfo.io](https://ipinfo.io/).

1. Create an account on [ipinfo.io](https://ipinfo.io/).
2. Get your API access token from your account dashboard.
3. Store the token as an environment variable:

   On Windows:
   ```bash
   set IPINFO_ACCESS_TOKEN=your-secure-token
   ```
   On macOS/Linux:
   ```bash
   export IPINFO_ACCESS_TOKEN="your-secure-token"
   ```

## 🚀 Usage

### Starting the App

Run the application by executing:

```bash
python main.py
```

This will open a graphical interface with three options:
1. **Port Scan**: Scan a range of ports on a host.
2. **Geolocate IP**: Enter an IP address to retrieve geolocation details.
3. **DHCP Listener**: Listen for DHCP requests on the network.

### Port Scan

- Click on the "1- Port Scan" button.
- Input the host's IP address and port range (e.g., `22-80`).
- The app will display whether each port is open or closed.

### Geolocation

- Click on the "2- GEOLOCATE IP" button.
- Enter the IP address you want to geolocate.
- The app will fetch and display the geolocation details from **ipinfo.io**.

### DHCP Listener

- Click on the "3- DHCP Listener" button.
- The app will start listening for DHCP packets and show details such as MAC addresses, hostnames, and requested IP addresses.

## ⚙️ Dependencies

The app relies on the following Python packages:

- `scapy==2.4.6`
- `paramiko==3.5.1`
- `ipinfo==3.1.2`
- `tkinter` (Standard library)
- `threading` (Standard library)
- `socket` (Standard library)

## 🛡️ Security

Please read the [Security Policy](SECURITY.md) for important information about securing the app and ensuring safe usage.

## 💬 Contributing

Contributions are welcome! If you'd like to contribute to the project, feel free to fork the repository and submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add feature'`).
4. Push to your branch (`git push origin feature-branch`).
5. Create a new pull request.

Please ensure your code adheres to the existing coding standards and that all tests pass before submitting a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgements

- **Scapy**: For powerful network packet manipulation.
- **ipinfo.io**: For providing geolocation data.
- **Tkinter**: For the graphical user interface.
- **Paramiko**: For SSH connections (if needed).

## 📧 Contact

For any inquiries or if you find a security vulnerability, feel free to contact us at:

- Email: [mangesh@ameyacloud.com](mailto:mangesh@ameyacloud.com)
- GitHub Issues: [Network-Scanner-App Issues](https://github.com/Net-Sec-Scan/Network-Scanner-App/issues)
