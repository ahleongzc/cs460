import psutil
import time

# Replace with your PID
pid = 68715
process = psutil.Process(pid)

try:
    while True:
        # Get memory usage in MB
        memory_info = process.memory_info()
        memory_usage = memory_info.rss / (1024 ** 2)  # Convert to MB

        # Get CPU usage for the process
        cpu_usage = process.cpu_percent(interval=1)  # Overall CPU usage
        
        # Get per-core CPU usage for the system
        per_core_cpu_usage = psutil.cpu_percent(interval=1, percpu=True)

        print(f"Process Memory usage: {memory_usage:.2f} MB")
        print(f"Process CPU usage (all cores): {cpu_usage}%")
        
        # Print per-core CPU usage
        print("Per-core CPU usage:")
        for i, usage in enumerate(per_core_cpu_usage):
            print(f"Core {i}: {usage}%")

        time.sleep(1)  # Adjust sleep time to monitor at desired intervals

except psutil.NoSuchProcess:
    print("Process ended or does not exist anymore.")
