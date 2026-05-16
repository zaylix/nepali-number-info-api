import os
import subprocess
import time
from datetime import datetime

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode(), error.decode()

def update_database():
    print(f"[{datetime.now()}] Starting database update...")
    
    # Run the data processing script to refresh database.json
    # In a real scenario, this might fetch new data from an external source
    # For now, we'll just re-run the process_data.py which adds more fake data
    output, error = run_command("python3 /home/ubuntu/process_data.py")
    if error:
        print(f"Error running process_data.py: {error}")
        return

    # Git operations
    run_command("git add database.json")
    run_command(f'git commit -m "Auto-update database: {datetime.now()}"')
    output, error = run_command("git push origin main")
    
    if error and "Everything up-to-date" not in error:
        print(f"Error pushing to GitHub: {error}")
    else:
        print(f"[{datetime.now()}] Database updated and pushed to GitHub successfully.")

if __name__ == "__main__":
    # This script can be run as a cron job or a background process
    # For GitHub Actions, we'll use a workflow file instead
    update_database()
