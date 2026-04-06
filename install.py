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
    packages = ["python3-pip", "net-tools", "ssh", "dropbear", "stunnel4", "openvpn", "squid", "curl", "wget", "tmux"]
    
    # Display header
    print("\n" + "="*60)
    print("   🚀 EVT SSH PANEL INSTALLER 🚀")
    print("="*60)
    print("   Welcome to EVT SSH Panel Installation")
    print("   This script will setup all dependencies")
    print("   and run the main panel in tmux session")
    print("="*60 + "\n")
    
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
        print("[🚀] EVT SSH PANEL - INITIALIZING SETUP")
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
            print("[🎉] EVT SSH PANEL SETUP COMPLETE!")
            print("="*50 + "\n")
            
            # Create tmux session and run main.py
            run_in_tmux()
            
        except Exception as e:
            print(f"\n[❌] Error during setup: {e}")
    else:
        print("\n[✅] All dependencies already installed!")
        print("[🚀] EVT SSH Panel is ready to start...\n")
        
        # Create tmux session and run main.py
        run_in_tmux()

def run_in_tmux():
    """Create tmux session and run main.py inside it"""
    print("\n" + "="*50)
    print("📌 EVT SSH PANEL - TMUX SETUP")
    print("="*50)
    
    try:
        # Kill existing session if exists
        subprocess.run(["tmux", "kill-session", "-t", "evtauto"], capture_output=True)
        
        # Create new tmux session
        subprocess.run(["tmux", "new-session", "-d", "-s", "evtauto"], check=True)
        print("[✅] Tmux session 'evtauto' created")
        
        # Send command to run python3 main.py in the session
        subprocess.run(["tmux", "send-keys", "-t", "evtauto", "cd $(pwd)", "C-m"], check=True)
        subprocess.run(["tmux", "send-keys", "-t", "evtauto", "python3 main.py", "C-m"], check=True)
        
        print("[✅] EVT SSH Panel is running inside tmux session 'evtauto'")
        print("\n" + "="*60)
        print("🎉 EVT SSH PANEL IS NOW RUNNING! 🎉")
        print("="*60)
        print("\n[📌] TO VIEW THE PANEL:")
        print("    tmux attach -t evtauto")
        print("\n[📌] TO DETACH FROM SESSION:")
        print("    Press Ctrl+B then D")
        print("\n[📌] TO STOP THE PANEL:")
        print("    tmux kill-session -t evtauto")
        print("\n[📌] TO RESTART THE PANEL:")
        print("    python3 install.py")
        print("="*60 + "\n")
        
    except subprocess.CalledProcessError as e:
        print(f"[❌] Failed to create tmux session: {e}")
    except FileNotFoundError:
        print("[❌] tmux is not installed! Please install tmux first.")
        print("[💡] Run: sudo apt-get install tmux -y")

if __name__ == "__main__":
    install_system_dependencies()