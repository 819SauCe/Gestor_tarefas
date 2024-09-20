import psutil

def list_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        try:
            cpu_usage = proc.cpu_percent(interval=0.1)
            mem_info = proc.memory_info()
            memory_usage = mem_info.rss
            if proc.status() not in (psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD) and proc.pid is not None:
                processes.append([proc.info['pid'], proc.info['name'], proc.info['status'], cpu_usage, memory_usage])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return sorted(processes, key=lambda p: (-p[3], p[4]))


def terminate_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        print(f"Processo {pid} finalizado com sucesso.")
    except psutil.NoSuchProcess:
        print(f"Processo {pid} não encontrado.")
    except psutil.AccessDenied:
        print(f"Acesso negado ao tentar finalizar o processo {pid}.")
