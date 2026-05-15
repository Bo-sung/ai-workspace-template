import os
import time
import subprocess
import platform
from datetime import datetime, timedelta

# 8 hours = 28800 seconds
TIMEOUT_SECONDS = 8 * 60 * 60

# File touched by the orchestrator (via SSH) to signal activity
ACTIVE_FILE = os.path.expanduser("~/.ai_worker_active")

def check_and_shutdown():
    print(f"[{datetime.now()}] AI Worker Auto-Shutdown Service Started.")
    print(f"Monitoring activity file: {ACTIVE_FILE}")
    print(f"Timeout set to: 8 hours.")

    while True:
        try:
            # If the file doesn't exist, create it to start the timer
            if not os.path.exists(ACTIVE_FILE):
                with open(ACTIVE_FILE, 'w') as f:
                    f.write("Initialized")
            
            # Get last modified time
            mtime = os.path.getmtime(ACTIVE_FILE)
            last_active = datetime.fromtimestamp(mtime)
            time_since_active = datetime.now() - last_active
            
            if time_since_active.total_seconds() > TIMEOUT_SECONDS:
                print(f"[{datetime.now()}] No activity for 8 hours. Initiating shutdown...")
                
                os_name = platform.system()
                if os_name == "Windows":
                    # Uses PowerShell to trigger Sleep (절전 모드) instead of Shutdown
                    subprocess.run(["powershell", "-Command", "Add-Type -Assembly System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false)"])
                elif os_name == "Darwin": # macOS
                    # Uses AppleScript to shutdown gracefully without requiring sudo password
                    subprocess.run(["osascript", "-e", 'tell app "System Events" to shut down'])
                else: # Linux
                    subprocess.run(["sudo", "shutdown", "-h", "now"])
                    
                break
                
        except Exception as e:
            print(f"Error checking activity: {e}")
            
        # Check every 10 minutes
        time.sleep(600)

if __name__ == "__main__":
    check_and_shutdown()
