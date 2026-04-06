#!/usr/bin/env python3
import sys
import subprocess
import threading
import time
import os

def loading_animation(stop_event, message):
    chars = ["▖", "▘", "▝", "▗"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r[⏳] {message} {chars[i % len(chars)]} ")
        sys.stdout.flush()
        time.sleep(0.2)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
    sys.stdout.flush()

def install_system_dependencies():
    packages = ["python3-pip", "net-tools", "ssh", "dropbear", "stunnel4", "openvpn", "squid", "curl", "wget"]
    
    needs_install = False
    for pkg in packages:
        check = subprocess.run(["dpkg", "-s", pkg], capture_output=True)
        if check.returncode != 0:
            needs_install = True
            break
    
    try:
        import flask
    except ImportError:
        needs_install = True
    
    if needs_install:
        print("\n" + "="*50)
        print("[🚀] INITIALIZING VPS SETUP")
        print("="*50)
        try:
            stop_event = threading.Event()
            t = threading.Thread(target=loading_animation, args=(stop_event, "Updating system repositories..."))
            t.start()
            subprocess.run(["sudo", "apt-get", "update", "-y"], capture_output=True)
            stop_event.set()
            t.join()
            print("[✅] System repositories updated.")
            
            for pkg in packages:
                check = subprocess.run(["dpkg", "-s", pkg], capture_output=True)
                if check.returncode != 0:
                    stop_event = threading.Event()
                    t = threading.Thread(target=loading_animation, args=(stop_event, f"Installing {pkg}..."))
                    t.start()
                    subprocess.run(["sudo", "apt-get", "install", "-y", pkg], capture_output=True)
                    stop_event.set()
                    t.join()
                    print(f"[✅] {pkg} installed.")
            
            stop_event = threading.Event()
            t = threading.Thread(target=loading_animation, args=(stop_event, "Installing python requirements..."))
            t.start()
            subprocess.run(["sudo", "pip3", "install", "flask", "flask-login", "requests", "waitress", "werkzeug"], capture_output=True)
            stop_event.set()
            t.join()
            print("[✅] Python requirements installed.")
            
            print("\n" + "="*50)
            print("[🎉] SETUP COMPLETE! STARTING MAIN APP...")
            print("="*50 + "\n")
            
            # Run main.py after installation
            subprocess.Popen(["python3", "main.py"])
            print("[✅] main.py started successfully!")
            
        except Exception as e:
            print(f"\n[❌] Error during setup: {e}")
    else:
        print("\n[✅] All dependencies already installed!")
        print("[🚀] Starting main application...\n")
        
        # Run main.py without blocking
        try:
            subprocess.Popen(["python3", "main.py"])
            print("[✅] main.py started in background!")
            print("[ℹ️] Press Ctrl+C to exit installer (main.py will keep running)")
            
            # Keep installer alive briefly to show message
            time.sleep(2)
        except FileNotFoundError:
            print("[❌] main.py not found in current directory!")
        except Exception as e:
            print(f"[❌] Error running main.py: {e}")

if __name__ == "__main__":
    install_system_dependencies()