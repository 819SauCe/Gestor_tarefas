import tkinter as tk

frames = [
    """
     #
     ##
     ####
    ##00##
    ##0000##
    ##000000##
    ##0000##
     ##00##
     ####
     ##
     #
    """,
    """
     #
     ##
     ****
    **00**
    **0000**
    **000000**
    **0000**
     **00**
     ****
     ##
     #
    """,
    """
     #
     ##
     $$$$
    $$00$$
    $$0000$$
    $$000000$$
    $$0000$$
     $$00$$
     $$$$
     ##
     #
    """,
    """
     #
     ##
     &&&&
    &&00&&
    &&0000&&
    &&000000&&
    &&0000&&
     &&00&&
     &&&&
     ##
     #
    """,
    """
     #
     ##
     ####
    ##00##
    ##0000##
    ##000000##
    ##0000##
     ##00##
     ####
     ##
     #
    """
]

class DiamondAnimationApp(tk.Toplevel):
    def __init__(self, master, on_complete):
        super().__init__(master)

        self.title("Loading. . .")
        self.geometry("400x400")
        self.configure(bg="#0a0a23")
        self.attributes('-alpha', 0.9)
        
        self.label = tk.Label(self, font=("Courier", 10), bg="#0a0a23", fg="white", justify=tk.CENTER)
        self.label.pack(expand=True, fill=tk.BOTH)

        self.frame_index = 0
        self.progress = 0
        self.max_progress = 100
        self.on_complete = on_complete  # Função que será chamada quando o loading terminar
        self.update_animation()

    def update_animation(self):
        self.label.config(text=f"{frames[self.frame_index]}\nLoading... {self.progress}%")
        
        self.frame_index = (self.frame_index + 1) % len(frames)
        
        if self.progress < self.max_progress:
            self.progress += 5  # Atualiza a porcentagem conforme necessário
            self.after(200, self.update_animation)
        else:
            self.on_complete()  # Chama a função ao finalizar o loading
            self.destroy()  # Fecha a janela de loading

def show_loading(master, on_complete):
    loading_window = DiamondAnimationApp(master, on_complete)
    return loading_window
