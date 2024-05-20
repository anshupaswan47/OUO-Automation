import subprocess
import time
import psutil

def open_new_tab(tab_index):
    cmd = f'start cmd /k "python run.py & exit"'
    print(f"Opening tab {tab_index}")
    subprocess.Popen(cmd, shell=True)

def close_tab(pid):
    try:
        proc = psutil.Process(pid)
        proc.terminate()  # Terminate the process
        proc.wait(timeout=5)  # Wait for the process to terminate
        print(f"Closed tab with PID {pid}")
    except psutil.NoSuchProcess:
        print(f"No such process: {pid}")
    except psutil.TimeoutExpired:
        print(f"Timeout expired for PID {pid}, force killing")
        proc.kill()  # Force kill if it didn't terminate

def get_new_cmd_pids(existing_pids):
    current_pids = set(p.pid for p in psutil.process_iter(attrs=['pid', 'name']) if p.info['name'] == 'cmd.exe')
    new_pids = current_pids - existing_pids
    return list(new_pids)

if __name__ == "__main__":
    while True:
        initial_pids = set(p.pid for p in psutil.process_iter(attrs=['pid', 'name']) if p.info['name'] == 'cmd.exe')

        # Open 6 tabs one by one
        for i in range(6):
            open_new_tab(i + 1)
            time.sleep(1)  # Small delay to ensure tabs open correctly

        print("All 6 tabs opened, waiting for 5 minutes...")
        time.sleep(300)  # Wait for 5 minutes

        # Get the PIDs of the new Command Prompt tabs
        new_pids = get_new_cmd_pids(initial_pids)

        # Close the tabs one by one with a 1-second delay between each
        for pid in new_pids:
            close_tab(pid)
            time.sleep(1)

        print("All tabs closed, waiting for 5 minutes before reopening...")
        time.sleep(300)  # Wait for 5 minutes before reopening tabs
