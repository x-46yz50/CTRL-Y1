import tkinter as tk
import pyautogui
import mss
import keyboard
import time
import threading
import numpy as np
import ctypes

# Otimização para Windows (High DPI)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

class HitboxVisualizer:
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.overrideredirect(True)
        self.top.attributes("-topmost", True)
        self.top.attributes("-alpha", 0.6)
        self.top.attributes("-transparentcolor", "white")
        self.top.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        
        self.canvas = tk.Canvas(self.top, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

    def update_rects(self, coords, width, height):
        self.canvas.delete("all")
        for direction, pos in coords.items():
            if pos:
                x, y = pos
                # Desenha a caixa. O '-20' no Y serve para centralizar melhor no receptor
                self.canvas.create_rectangle(
                    x - width//2, y - 5, 
                    x + width//2, y + height - 5, 
                    outline="red", width=2
                )
    
    def close(self):
        self.top.destroy()

class FNFOptimizedBot:
    def __init__(self, root):
        self.root = root
        self.root.title("roFNF Bot - Fast Stream Edition")
        self.root.geometry("550x675")
        self.root.resizable(False, True)

        self.running = False
        self.visualizer = None
        
        # --- COORDENADAS DO SEU PRINT (ARREDONDADAS PARA SEGURANÇA) ---
        # Left: 634, Down: 852, Up: 1071, Right: 1284
        # Y (Altura) padronizado para 890~896 base
        self.coordinates = {
            'left': (635, 905), 
            'down': (850, 905), 
            'up': (1070, 905), 
            'right': (1285, 905)
        }
        
        self.key_vars = {
            'left': tk.StringVar(value='d'),
            'down': tk.StringVar(value='f'),
            'up': tk.StringVar(value='j'),
            'right': tk.StringVar(value='k')
        }

        self.status_var = tk.StringVar(value="Status: Parado (F7 Start/Stop)")
        self.create_widgets()

        try:
            keyboard.add_hotkey('f7', self.toggle_bot_state)
        except ImportError:
            pass

    def create_widgets(self):
        tk.Label(self.root, text="roFNF Bot - Velocidade & Outline", font=("Segoe UI", 14, "bold")).pack(pady=10)
        
        instr = tk.LabelFrame(self.root, text="Ajustes para Notas Rápidas", padx=5, pady=5)
        instr.pack(fill="x", padx=10)
        tk.Label(instr, text="1. Se errar notas rápidas: DIMINUA o Delay de Soltura.\n2. Se errar Long Notes: AUMENTE o Delay de Soltura.\n3. O 'Threshold' deve ser baixo (40-60) para pegar a borda cinza.", justify="left", fg="#444").pack()

        btn_vis = tk.Button(self.root, text="👁 MOSTRAR HITBOX (VISUALIZAR)", bg="#2196F3", fg="white", font=("Arial", 9, "bold"), command=self.toggle_visualizer)
        btn_vis.pack(pady=5)

        # Coordenadas
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        self.coord_labels = {}
        for d in ['left', 'down', 'up', 'right']:
            row = tk.Frame(frame)
            row.pack(fill='x', pady=2)
            tk.Label(row, text=f"{d.upper()}:", width=6, anchor='w', font=("Consolas", 10, "bold")).pack(side='left')
            tk.Entry(row, textvariable=self.key_vars[d], width=4).pack(side='left', padx=5)
            tk.Button(row, text="Set", command=lambda x=d: self.set_coordinate(x), width=6).pack(side='left')
            
            # Mostra a coordenada atual
            pos_text = str(self.coordinates[d])
            self.coord_labels[d] = tk.Label(row, text=pos_text, width=14, fg="green")
            self.coord_labels[d].pack(side='left')

        # Configurações Críticas
        settings = tk.LabelFrame(self.root, text="Sintonia Fina", padx=10, pady=10)
        settings.pack(pady=10, fill="x", padx=10)

        # 1. Delay de Soltura
        tk.Label(settings, text="Delay de Soltura (Coyote Time) - ms:", fg="blue", font=("Arial", 9, "bold")).pack(anchor='w')
        self.release_delay_slider = tk.Scale(settings, from_=0, to=100, orient='horizontal', length=400, resolution=5)
        self.release_delay_slider.set(20) # 20ms é melhor para notas rápidas
        self.release_delay_slider.pack(anchor='w')
        tk.Label(settings, text="Menor = Mais rápido | Maior = Melhora Long Note", fg="gray", font=("Arial", 8)).pack(anchor='w', pady=(0, 5))

        # 2. Altura Hitbox
        tk.Label(settings, text="Altura da Hitbox (Vertical):").pack(anchor='w')
        self.height_slider = tk.Scale(settings, from_=10, to=1500, orient='horizontal', length=400)
        self.height_slider.set(50) # Aumentei para 40 para não perder notas rápidas
        self.height_slider.pack(anchor='w')
        
        # 3. Sensibilidade
        tk.Label(settings, text="Sensibilidade (Detectar Cinza/Branco):").pack(anchor='w')
        self.threshold_slider = tk.Scale(settings, from_=5, to=200, orient='horizontal', length=400)
        self.threshold_slider.set(50) # Valor médio para pegar o outline cinza
        self.threshold_slider.pack(anchor='w')

        # Botões
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        self.start_btn = tk.Button(btn_frame, text="START (F7)", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), command=self.start_bot, width=12)
        self.start_btn.pack(side='left', padx=10)
        self.stop_btn = tk.Button(btn_frame, text="STOP (F7)", bg="#f44336", fg="white", font=("Arial", 11, "bold"), command=self.stop_bot, width=12, state='disabled')
        self.stop_btn.pack(side='left', padx=10)
        
        tk.Label(self.root, textvariable=self.status_var, relief='sunken', anchor='w').pack(side='bottom', fill='x')

    def toggle_visualizer(self):
        if self.visualizer:
            self.visualizer.close()
            self.visualizer = None
        else:
            self.visualizer = HitboxVisualizer(self.root)
            self.visualizer.update_rects(self.coordinates, 8, self.height_slider.get())

    def set_coordinate(self, direction):
        def countdown():
            for i in range(3, 0, -1):
                self.status_var.set(f"Posicione em {direction}... {i}")
                time.sleep(1)
            x, y = pyautogui.position()
            self.coordinates[direction] = (x, y)
            self.root.after(0, lambda: self.coord_labels[direction].config(text=str((x,y)), fg="green"))
            if self.visualizer:
                self.root.after(0, lambda: self.visualizer.update_rects(self.coordinates, 8, self.height_slider.get()))

        threading.Thread(target=countdown, daemon=True).start()

    def toggle_bot_state(self):
        if self.running:
            self.root.after(0, self.stop_bot)
        else:
            self.root.after(0, self.start_bot)

    def start_bot(self):
        if self.running: return 
        if self.visualizer: self.visualizer.close(); self.visualizer = None 
        
        self.running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_var.set("RODANDO! (F7 para parar)")
        threading.Thread(target=self.bot_logic, daemon=True).start()

    def stop_bot(self):
        self.running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_var.set("Parado.")

    def bot_logic(self):
        threshold = self.threshold_slider.get()
        hitbox_h = self.height_slider.get()
        release_delay_ms = self.release_delay_slider.get()
        release_delay_sec = release_delay_ms / 1000.0
        
        keys = {d: self.key_vars[d].get() for d in ['left', 'down', 'up', 'right']}
        holding = {k: False for k in keys}
        last_seen = {d: 0.0 for d in keys} 

        # Bounding Box Otimizado
        xs = [p[0] for p in self.coordinates.values()]
        ys = [p[1] for p in self.coordinates.values()]
        hitbox_w = 20 # Estreito para precisão
        
        # Ajuste de offset vertical leve para pegar a nota chegando
        offset_y = -5 

        monitor = {
            "left": min(xs) - hitbox_w,
            "top": min(ys) + offset_y,
            "width": (max(xs) - min(xs)) + hitbox_w * 2,
            "height": hitbox_h + 10
        }

        with mss.mss() as sct:
            while self.running:
                # Loop ultra-rápido sem sleep
                sct_img = sct.grab(monitor)
                img = np.array(sct_img)
                current_time = time.time()

                for direction, (gx, gy) in self.coordinates.items():
                    rel_x = gx - monitor["left"]
                    
                    # Recorte da Hitbox Vertical
                    # Pega apenas o Canal Verde (índice 1), pois o cinza/branco reflete bem nele
                    roi = img[0:hitbox_h, rel_x-3:rel_x+3, 1] 

                    max_val = np.max(roi) if roi.size > 0 else 0
                    k = keys[direction]

                    # Detectou nota (Branco ou Cinza acima do threshold)
                    if max_val > threshold:
                        last_seen[direction] = current_time
                        
                        if not holding[direction]:
                            keyboard.press(k)
                            holding[direction] = True
                    else:
                        # Nota sumiu (Preto)
                        if holding[direction]:
                            # Só solta se passou o tempo do Delay
                            if (current_time - last_seen[direction]) > release_delay_sec:
                                keyboard.release(k)
                                holding[direction] = False

if __name__ == "__main__":
    root = tk.Tk()
    app = FNFOptimizedBot(root)
    root.mainloop()