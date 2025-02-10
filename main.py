from application import NetworkScannerApp
import tkinter as tk


def main():
    root = tk.Tk()
    app = NetworkScannerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
