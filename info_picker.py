import psutil

def get_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    mem_usage = psutil.virtual_memory().percent
    hd_usage = psutil.disk_usage('/').percent
    return cpu_usage, mem_usage, hd_usage
