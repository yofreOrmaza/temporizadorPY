import tkinter as tk
from tkinter import simpledialog
import time
import threading
from pygame import mixer  # para reproducir el sonido

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temporizador Pomodoro Extendido")
        self.root.geometry("300x200")
        self.root.attributes("-topmost", True)  # siempre encima

        # Inicializar mixer
        mixer.init()

        # Variables
        self.total_seconds = 25 * 60  # por defecto 25 min
        self.remaining_seconds = self.total_seconds
        self.running = False
        self.paused = False

        # Widgets
        self.label = tk.Label(root, text=self.format_time(self.remaining_seconds), font=("Helvetica", 30))
        self.label.pack(pady=20)

        self.start_btn = tk.Button(root, text="Iniciar", command=self.start_timer)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = tk.Button(root, text="Pausar", command=self.pause_timer)
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.resume_btn = tk.Button(root, text="Reanudar", command=self.resume_timer)
        self.resume_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(root, text="Reiniciar", command=self.reset_timer)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        self.edit_btn = tk.Button(root, text="Editar tiempo", command=self.edit_time)
        self.edit_btn.pack(side=tk.BOTTOM, pady=10)

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        if days > 0:
            return f"{days}d {hours:02}:{mins:02}:{secs:02}"
        elif hours > 0:
            return f"{hours:02}:{mins:02}:{secs:02}"
        else:
            return f"{mins:02}:{secs:02}"

    def start_timer(self):
        if not self.running:
            self.running = True
            self.paused = False
            threading.Thread(target=self.run_timer, daemon=True).start()

    def run_timer(self):
        while self.remaining_seconds > 0 and self.running:
            if not self.paused:
                time.sleep(1)
                self.remaining_seconds -= 1
                self.update_label()
        if self.remaining_seconds <= 0 and self.running:
            self.finish_timer()

    def pause_timer(self):
        if self.running:
            self.paused = True

    def resume_timer(self):
        if self.running and self.paused:
            self.paused = False

    def reset_timer(self):
        self.running = False
        self.paused = False
        self.remaining_seconds = self.total_seconds
        self.update_label()

    def edit_time(self):
        self.running = False
        self.paused = False
        minutes = simpledialog.askinteger("Editar tiempo", "Ingrese minutos:", parent=self.root, minvalue=1)
        if minutes:
            self.total_seconds = minutes * 60
            self.remaining_seconds = self.total_seconds
            self.update_label()

    def update_label(self):
        self.label.config(text=self.format_time(self.remaining_seconds))

    def finish_timer(self):
        mixer.music.load("finish.mp3")
        mixer.music.play(-1)  # loop infinito hasta que se cierre el modal

        # Crear ventana modal personalizada
        modal = tk.Toplevel(self.root)
        modal.title("Tiempo terminado")
        modal.geometry("250x120")
        modal.attributes("-topmost", True)
        modal.grab_set()  # hace la ventana modal

        msg = tk.Label(modal, text="¡El temporizador ha finalizado!", font=("Helvetica", 12))
        msg.pack(pady=15)

        btn = tk.Button(modal, text="Aceptar", command=lambda: self.stop_sound(modal))
        btn.pack(pady=10)

        # Si el usuario cierra con la X
        modal.protocol("WM_DELETE_WINDOW", lambda: self.stop_sound(modal))

        self.running = False

    def stop_sound(self, modal):
        mixer.music.stop()
        modal.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()