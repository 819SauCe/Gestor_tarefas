import tkinter as tk
import tkinter.ttk as ttk
import psutil
import GPUtil
from process_utils import list_processes, terminate_process
import threading
from loading import show_loading
import info_picker
import os

def finalizar_selecionado():
    selected = apps.curselection()
    if selected:
        selected_process = apps.get(selected)
        print(f"Selecionado: {selected_process}")  # Debug
        try:
            pid = int(selected_process.split("|")[0].strip())
            terminate_process(pid)
            threading.Thread(target=update_listbox).start()
        except (IndexError, ValueError) as e:
            print(f"Erro: {e}")

def update_listbox():
    try:
        processes = list_processes()
        root.after(0, lambda: update_listbox_ui(processes))
    except Exception as e:
        print(f"Erro: {e}")

def update_listbox_ui(processes):
    apps.delete(0, tk.END)
    for pid, name, status, cpu_usage, memory_usage in processes:
        apps.insert(tk.END, f"{pid:<6} | {name:<30} | {status:<10} | CPU: {cpu_usage:>5}% | Memória: {memory_usage / (1024 * 1024):>6.2f} MB")

def draw_bar(usage, length=30):
    filled_len = int(length * usage // 100)
    return '▓' * filled_len + '░' * (length - filled_len)

def update_usage():
    try:
        cpu_usage, mem_usage, _ = info_picker.get_usage()
        cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        cpu_bar.config(text=draw_bar(cpu_usage))
        mem_label.config(text=f"Memory Usage: {mem_usage}%")
        mem_bar.config(text=draw_bar(mem_usage))
        hd_usage = psutil.disk_usage('/').percent
        hd_label.config(text=f"HD Usage: {hd_usage}%")
        hd_bar.config(text=draw_bar(hd_usage))
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def update_cpu_info():
    try:
        cpu_usage = psutil.cpu_percent()
        cpu_freq = psutil.cpu_freq().current
        core_count = psutil.cpu_count(logical=True)
        physical_cores = psutil.cpu_count(logical=False)
        cpu_temp = psutil.sensors_temperatures().get('coretemp', [{}])[0].get('current', 'N/A')
        
        temp_label.config(text=f"CPU Temp: {cpu_temp}°C")
        cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        cpu_bar.config(text=draw_bar(cpu_usage))
        freq_label.config(text=f"CPU Frequency: {cpu_freq:.2f} MHz")
        core_label.config(text=f"Logical cores: {core_count} | Physical cores: {physical_cores}")
        uptime = int(psutil.boot_time())
        uptime_label.config(text=f"System Uptime: {uptime}")
        
        root.after(1000, update_cpu_info)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

root = tk.Tk()
root.title("Assignment task")
root.geometry("700x500")
root.configure(bg='#0a0a23')
root.resizable(False, False)
root.withdraw()
root.attributes('-alpha', 0.9)

icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
icon_image = tk.PhotoImage(file=icon_path)
root.iconphoto(True, icon_image)

loading = show_loading(root, root.deiconify)
tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

tab1 = tk.Frame(tabs, bg='#0a0a23')
tabs.add(tab1, text='Open App')
apps = tk.Listbox(tab1, width=100, height=24, background='#0b0021', foreground='white', borderwidth=0, font=('Courier', 10))
apps.pack(pady=20)
update_listbox()

style = ttk.Style()
style.theme_create('Cloud', settings={
    ".": {"configure": {"background": '#0a0a23'}},
    "TNotebook": {"configure": {"background": '#0a0a23', "borderwidth": 0}},
    "TNotebook.Tab": {
        "configure": {"background": '#0a0a23', "foreground": 'white'},
        "map": {"background": [("selected", '#0a0a23')], "foreground": [("selected", 'white')]}
    }
})
style.theme_use('Cloud')

botao_finalizar = tk.Button(root, text="Finalizar Processo", borderwidth=2, command=finalizar_selecionado, background='black', foreground='white')
botao_finalizar.pack(padx=10)
botao_finalizar.place(x=580, y=460)

tab_cpu = tk.Frame(tabs, bg='#0a0a23')
tabs.add(tab_cpu, text="CPU")

def add_cpu_info(label_text):
    frame = tk.Frame(tab_cpu, bg='#0a0a23')
    frame.pack(padx=10, pady=10, anchor="w")
    label = tk.Label(frame, text=label_text, bg='#0a0a23', fg='white', font=("Courier", 12))
    label.pack(side="left")
    bar = tk.Label(frame, text=draw_bar(0), bg='#0a0a23', fg='white', font=("Courier", 12))
    bar.pack(side="right")
    return label, bar

cpu_label, cpu_bar = add_cpu_info("CPU Usage: 0%")
freq_label, _ = add_cpu_info("CPU Frequency: 0.00 MHz")
core_label, _ = add_cpu_info("Logical cores: 0 | Physical cores: 0")
uptime_label, _ = add_cpu_info("System Uptime: 0")
temp_label, _ = add_cpu_info("CPU Temp: N/A")

def update_gpu_temp():
    try:
        gpus = GPUtil.getGPUs()
        gpu_temp = gpus[0].temperature if gpus else 'N/A'
        gpu_temp_label.config(text=f"GPU Temp: {gpu_temp}°C")
        gpu_temp_bar.config(text=draw_bar(gpu_temp))
    except Exception:
        gpu_temp_label.config(text="GPU Temp: N/A")
    root.after(1000, update_gpu_temp)

tab_gpu = tk.Frame(tabs, bg='#0a0a23')
tabs.add(tab_gpu, text="GPU")

gpu_label = tk.Label(tab_gpu, text="GPU Usage:", bg='#0a0a23', fg='white', font=("Courier", 12))
gpu_label.pack(padx=10, pady=10)
gpu_bar = tk.Label(tab_gpu, text=draw_bar(0), bg='#0a0a23', fg='white', font=("Courier", 12))
gpu_bar.pack(padx=10, pady=10)
gpu_temp_label = tk.Label(tab_gpu, text="GPU Temp: N/A", bg='#0a0a23', fg='white', font=("Courier", 12))
gpu_temp_label.pack(padx=10, pady=10)
gpu_temp_bar = tk.Label(tab_gpu, text=draw_bar(0), bg='#0a0a23', fg='white', font=("Courier", 12))
gpu_temp_bar.pack(padx=10, pady=10)

tab_memory = tk.Frame(tabs, bg='#0a0a23')
tabs.add(tab_memory, text="Memory")

mem_label = tk.Label(tab_memory, text="Memory Usage:", bg='#0a0a23', fg='white', font=("Courier", 12))
mem_label.pack(padx=10, pady=10)
mem_bar = tk.Label(tab_memory, text=draw_bar(0), bg='#0a0a23', fg='white', font=("Courier", 12))
mem_bar.pack(padx=10, pady=10)
hd_label = tk.Label(tab_memory, text="HD Usage: 0%", bg='#0a0a23', fg='white', font=("Courier", 12))
hd_label.pack(padx=10, pady=10)
hd_bar = tk.Label(tab_memory, text=draw_bar(0), bg='#0a0a23', fg='white', font=("Courier", 12))
hd_bar.pack(padx=10, pady=10)

update_usage()
update_cpu_info()
update_gpu_temp()

def toggle_botao(event):
    current_tab = tabs.index(tabs.select())
    botao_finalizar.place(x=580, y=460) if current_tab == 0 else botao_finalizar.place_forget()

root.deiconify()
tabs.bind("<<NotebookTabChanged>>", toggle_botao)
root.mainloop()
