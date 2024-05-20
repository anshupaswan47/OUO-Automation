import subprocess
import time

def open_new_tab(tab_index):
    cmd = f'start cmd /k "python run.py & exit"'
    print(f"Opening tab {tab_index}")
    subprocess.run(cmd, shell=True)

def close_tab(tab_handle):
    cmd = f'taskkill /PID {tab_handle} /F'
    print(f"Closing tab with PID {tab_handle}")
    subprocess.run(cmd, shell=True)

def get_cmd_pids():
    result = subprocess.run("tasklist /FI \"IMAGENAME eq cmd.exe\"", shell=True, stdout=subprocess.PIPE)
    output = result.stdout.decode()
    lines = output.splitlines()
    pids = []
    for line in lines[3:]:  # Skip the header lines
        parts = line.split()
        if len(parts) >= 2:
            pids.append(parts[1])
    return pids

if __name__ == "__main__":
    while True:
        tab_handles = []

        # Open 6 tabs one by one
        for i in range(6):
            open_new_tab(i + 1)
            time.sleep(1)  # Small delay to ensure tabs open correctly

        print("All 6 tabs opened, waiting for 5 minutes...")
        time.sleep(300)  # Wait for 5 minutes

        # Get the PIDs of the open Command Prompt tabs
        tab_handles = get_cmd_pids()

        # Close the tabs one by one with a 1-second delay between each
        for handle in tab_handles:
            close_tab(handle)
            time.sleep(1)

        print("All tabs closed, waiting for 5 minutes before reopening...")
        time.sleep(300)  # Wait for 5 minutes before reopening tabs
