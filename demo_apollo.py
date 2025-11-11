#!/usr/bin/env python3
"""
Apollo Digitalis Virtualis - Demo Server
Quick start script for running both backend and serving the dashboard
"""

import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def print_banner():
    """Print startup banner"""
    banner = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║         🔮 APOLLO DIGITALIS VIRTUALIS 🔮                      ║
    ║                                                                ║
    ║         Interactive Dashboard with VR/AR Support               ║
    ║         Euystacio Holographic Chat Interface (CIC)             ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    
    Starting Apollo Dashboard...
    """
    print(banner)

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_cors
        import yaml
        print("✅ All Python dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\nInstalling dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
        print("✅ Dependencies installed")
        return True

def start_backend():
    """Start the Flask backend server"""
    print("\n🚀 Starting backend server on http://127.0.0.1:5000")
    os.environ['DEBUG'] = 'True'
    subprocess.run([sys.executable, "oi_server.py"])

def start_frontend():
    """Start a simple HTTP server for the frontend"""
    print("🌐 Starting frontend server on http://localhost:8080")
    time.sleep(2)  # Wait for backend to start
    subprocess.run([sys.executable, "-m", "http.server", "8080"])

def open_browser():
    """Open the dashboard in the default browser"""
    time.sleep(3)  # Wait for servers to start
    url = "http://localhost:8080/apollo-dashboard.html"
    print(f"\n🌍 Opening dashboard in browser: {url}")
    webbrowser.open(url)

def main():
    """Main entry point"""
    print_banner()
    
    if not check_dependencies():
        sys.exit(1)
    
    print("\n" + "="*70)
    print("APOLLO DASHBOARD - Quick Start")
    print("="*70)
    print("\n📋 Available URLs:")
    print("   Dashboard: http://localhost:8080/apollo-dashboard.html")
    print("   Backend API: http://127.0.0.1:5000/api/v1/health")
    print("\n💬 Try these commands in the Chat Interface:")
    print("   • Avvia analisi Terræ Nova")
    print("   • Status sistema")
    print("   • Modalità VR")
    print("\n🥽 VR Mode:")
    print("   Click 'Enter VR Mode' button (bottom left)")
    print("\n⌨️  Navigation:")
    print("   • Mouse Drag: Rotate camera")
    print("   • W/A/S/D: Move camera")
    print("\n🛑 To stop: Press Ctrl+C")
    print("="*70 + "\n")
    
    try:
        # Start backend in a separate thread
        backend_thread = Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # Open browser in a separate thread
        browser_thread = Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Start frontend in main thread
        start_frontend()
        
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Apollo Dashboard...")
        print("Goodbye, Seedbringer! 🔮")
        sys.exit(0)

if __name__ == "__main__":
    main()
