import tkinter as tk
from tkinter import simpledialog
import time
import threading
from pygame import mixer


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temporizador Pomodoro Extendido")
        self.root.geometry("350x400")
        self.root.attributes("-topmost", True)

        mixer.init()

        # SECCIÓN TASKS
        self.tasks = []

        self.tasks_frame = tk.Frame(root)
        self.tasks_frame.pack(fill="x", padx=10, pady=5)

        self.tasks_title = tk.Label(self.tasks_frame, text="Tasks", font=("Helvetica", 12, "bold"))
        self.tasks_title.pack(anchor="w")

        self.tasks_list_frame = tk.Frame(self.tasks_frame)
        self.tasks_list_frame.pack(fill="x")

        self.add_task_btn = tk.Button(
            self.tasks_frame, text="+ Agregar Task", command=self.add_task
        )
        self.add_task_btn.pack(pady=5)

        # SECCIÓN TEMPORIZADOR
        self.total_seconds = 25 * 60
        self.remaining_seconds = self.total_seconds
        self.running = False
        self.paused = False

        self.label = tk.Label(root, text=self.format_time(self.remaining_seconds),
                              font=("Helvetica", 30))
        self.label.pack(pady=15)

        controls = tk.Frame(root)
        controls.pack()

        self.start_btn = tk.Button(controls, text="Iniciar", command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=3)

        self.pause_btn = tk.Button(controls, text="Pausar", command=self.pause_timer)
        self.pause_btn.grid(row=0, column=1, padx=3)

        self.resume_btn = tk.Button(controls, text="Reanudar", command=self.resume_timer)
        self.resume_btn.grid(row=0, column=2, padx=3)

        self.reset_btn = tk.Button(controls, text="Reiniciar", command=self.reset_timer)
        self.reset_btn.grid(row=0, column=3, padx=3)

        self.edit_btn = tk.Button(root, text="Editar tiempo", command=self.edit_time)
        self.edit_btn.pack(pady=10)

    # FUNCIÓN TASKS
    def add_task(self):
        task_frame = tk.Frame(self.tasks_list_frame)
        task_frame.pack(fill="x", pady=2)

        var = tk.BooleanVar()

        checkbox = tk.Checkbutton(task_frame, variable=var)
        checkbox.pack(side=tk.LEFT)

        entry = tk.Entry(task_frame)
        entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        entry.focus()

        delete_btn = tk.Button(
            task_frame, text="❌", command=lambda: task_frame.destroy()
        )
        delete_btn.pack(side=tk.RIGHT)

        self.tasks.append((var, entry))

    # FUNCIÓN TEMPORIZADOR
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
        self.paused = True

    def resume_timer(self):
        self.paused = False

    def reset_timer(self):
        self.running = False
        self.paused = False
        self.remaining_seconds = self.total_seconds
        self.update_label()

    def edit_time(self):
        self.running = False
        minutes = simpledialog.askinteger(
            "Editar tiempo", "Ingrese minutos:", parent=self.root, minvalue=1
        )
        if minutes:
            self.total_seconds = minutes * 60
            self.remaining_seconds = self.total_seconds
            self.update_label()

    def update_label(self):
        self.label.config(text=self.format_time(self.remaining_seconds))

    def finish_timer(self):
        mixer.music.load("finish.mp3")
        mixer.music.play(-1)

        modal = tk.Toplevel(self.root)
        modal.title("Tiempo terminado")
        modal.geometry("250x120")
        modal.attributes("-topmost", True)
        modal.grab_set()

        tk.Label(modal, text="¡El temporizador ha finalizado!",
                 font=("Helvetica", 12)).pack(pady=15)

        tk.Button(modal, text="Aceptar",
                  command=lambda: self.stop_sound(modal)).pack(pady=10)

        modal.protocol("WM_DELETE_WINDOW", lambda: self.stop_sound(modal))
        self.running = False

    def stop_sound(self, modal):
        mixer.music.stop()
        modal.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
