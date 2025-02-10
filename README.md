# Network Scanner App 🖥️🔍

A real-time **Network Scanner App** designed to provide powerful network analysis features like port scanning, geolocation lookup, and DHCP packet listening. Whether you are a **network administrator**, **security professional**, or **tech enthusiast**, this app helps you analyze and troubleshoot networks with ease.

## ✨ Features

- **Port Scanning** 🛠️  
  Scan any **IP address** for open ports, with both **default** and **custom port selections**.

- **Geolocation** 🌍  
  Get the **geographical location** of an IP address with detailed information like **city**, **country**, and **coordinates**.

- **DHCP Listener** 📡  
  Listen for **incoming DHCP requests** to monitor devices joining the network and capture important details like **MAC addresses** and **requested IPs**.

- **Verbose Mode** 🧐  
  Enable **verbose mode** to see **real-time scanning progress** in both the **GUI** and the **log file**.

- **Real-time Logging** 📜  
  Log scan results in a **detailed log file**, including **timestamps** and information about each port's status (open/closed).

- **Progress Bar** 📊  
  Track the **scanning progress** with an intuitive progress bar in the GUI, making it easy to monitor scan status in real time.

## 📦 Installation

### Prerequisites ⚙️

Make sure you have **Python 3.6** or higher installed on your machine. You will also need `pip` to install the necessary dependencies.

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Mangesh-Bhattacharya/Net-Sec-Scan.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd Net-Sec-Scan
   ```

3. **Create a virtual environment** (recommended):

   ```bash
   python -m venv env
   ```

4. **Activate the virtual environment**:
   - **On Windows**:

     ```bash
     .\env\Scripts\activate
     ```

   - **On macOS/Linux**:

     ```bash
     source env/bin/activate
     ```

5. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### Geolocation API Key 🌍

To use the **geolocation lookup** feature, you need an **API key** from [ipinfo.io](https://ipinfo.io/).

1. **Create an account** on [ipinfo.io](https://ipinfo.io/).
2. **Get your API access token** from your account dashboard.
3. **Store the token as an environment variable**:
   - **On Windows**:

     ```bash
     set IPINFO_ACCESS_TOKEN=your-secure-token
     ```

   - **On macOS/Linux**:

     ```bash
     export IPINFO_ACCESS_TOKEN="your-secure-token"
     ```

## 🚀 Usage

### Starting the App 💻

To run the application, simply execute the following:

```bash
python main.py
```

This will open a graphical interface with three primary options:

1. **Port Scan** 🛠️: Scan a range of ports on a host.
2. **Geolocate IP** 🌍: Enter an IP address to retrieve geolocation details.
3. **DHCP Listener** 📡: Listen for DHCP requests on the network.

### Port Scan 🛠️

1. Click on the **"1- Port Scan"** button.
2. Input the **host's IP address** and **port range** (e.g., `22-80`).
3. The app will display whether each port is **open** or **closed**.

### Geolocation 🌍

1. Click on the **"2- GEOLOCATE IP"** button.
2. Enter the **IP address** you want to geolocate.
3. The app will fetch and display the geolocation details from **ipinfo.io**.

### DHCP Listener 📡

1. Click on the **"3- DHCP Listener"** button.
2. The app will start listening for **DHCP packets** and show details such as **MAC addresses**, **hostnames**, and **requested IP addresses**.

## ⚙️ Dependencies

The app relies on the following Python packages:

- `scapy==2.4.6` 🔧: For powerful network packet manipulation.
- `paramiko==3.5.1` 🔑: For SSH connections (if needed).
- `ipinfo==3.1.2` 🌍: For geolocation data.
- `tkinter` 🖱️: For the graphical user interface (GUI).
- `threading` ⏳: For running background tasks like listening for DHCP packets.
- `socket` 📡: For network-related tasks.

## 🛡️ Security

Please review the [Security Policy](SECURITY.md) for essential information about securing the app and ensuring safe usage.

## 💬 Contributing

We welcome contributions to improve this project! To contribute:

1. **Fork the repository**.
2. Create a **new branch** (`git checkout -b feature-branch`).
3. **Commit your changes** (`git commit -am 'Add feature'`).
4. Push your changes to your branch (`git push origin feature-branch`).
5. Create a **pull request**.

Please ensure that your code adheres to the existing coding standards and passes all tests before submitting a pull request.

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

## 🤝 Acknowledgements

- **Scapy**: For providing powerful network packet manipulation capabilities.
- **ipinfo.io**: For offering excellent geolocation data.
- **Tkinter**: For providing the GUI framework.
- **Paramiko**: For enabling SSH functionality if needed.

## 📧 Contact

For any inquiries, suggestions, or if you find a security vulnerability, please reach out:

- **Email**: [mangesh@ameyacloud.com](mailto:mangesh@ameyacloud.com)
- **GitHub Issues**: [Network-Scanner-App Issues](https://github.com/Net-Sec-Scan/Network-Scanner-App/issues)

---

Thank you for checking out the **Network Scanner App**! Happy scanning! 🔍

```

### Key Changes:

1. **Features Section Updated**: Added new features, including verbose mode, real-time logging, and a progress bar.
2. **Enhanced Detail for Features**: Each feature is now more descriptive with appropriate emojis for better visual appeal.
3. **Industry Tone with Emoticons**: The emoticons make the README engaging, yet it maintains a professional feel.
