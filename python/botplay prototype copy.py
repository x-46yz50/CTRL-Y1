import tkinter as tk
from tkinter import ttk
import pyautogui
import mss
import keyboard
import time
import threading
import numpy as np
import ctypes

# Otimização de DPI para Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

class LadderVisualizer:
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.overrideredirect(True)
        self.top.attributes("-topmost", True)
        self.top.attributes("-alpha", 0.6)
        self.top.attributes("-transparentcolor", "white")
        self.top.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        
        self.canvas = tk.Canvas(self.top, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

    def draw_ladder(self, coords, seg_height, num_segments, lane_width=10):
        self.canvas.delete("all")
        for direction, pos in coords.items():
            if pos:
                base_x, base_y = pos
                # Desenha a "escada"
                # Segmento 0 (Vermelho) = Receptor (Onde a nota bate)
                # Segmentos 1+ (Azul) = Scanner Vertical (O que vem depois)
                
                # Base
                self.canvas.create_rectangle(
                    base_x - lane_width, base_y, 
                    base_x + lane_width, base_y + seg_height, 
                    outline="#FF0000", width=2
                )
                
                # Degraus para cima
                for i in range(1, num_segments + 1):
                    y_pos = base_y - (i * seg_height)
                    self.canvas.create_rectangle(
                        base_x - lane_width, y_pos, 
                        base_x + lane_width, y_pos + seg_height, 
                        outline="#00FFFF", width=1
                    )

    def close(self):
        self.top.destroy()

class FNFSmartLadderBot:
    def __init__(self, root):
        self.root = root
        self.root.title("roFNF Bot - Ladder Logic (Scanner Vertical)")
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        self.running = False
        self.visualizer = None
        
        # Coordenadas exatas das suas imagens
        self.coordinates = {
            'left': (635, 890), 
            'down': (850, 890), 
            'up': (1070, 890), 
            'right': (1285, 890)
        }
        
        self.key_vars = {
            'left': tk.StringVar(value='d'),
            'down': tk.StringVar(value='f'),
            'up': tk.StringVar(value='j'),
            'right': tk.StringVar(value='k')
        }

        self.status_var = tk.StringVar(value="Status: Parado")
        self.debug_info = tk.StringVar(value="Debug: Inativo")
        
        self.setup_ui()

        try:
            keyboard.add_hotkey('f7', self.toggle_bot_state)
        except ImportError:
            pass

    def setup_ui(self):
        tk.Label(self.root, text="roFNF Bot - Lógica de Escada", font=("Segoe UI", 14, "bold")).pack(pady=5)
        
        # Sistema de Abas
        tab_control = ttk.Notebook(self.root)
        tab_main = ttk.Frame(tab_control)
        tab_ladder = ttk.Frame(tab_control)
        
        tab_control.add(tab_main, text='Principal')
        tab_control.add(tab_ladder, text='Configuração da Escada')
        tab_control.pack(expand=1, fill="both", padx=10, pady=5)

        # --- ABA PRINCIPAL ---
        btn_frame = tk.Frame(tab_main)
        btn_frame.pack(pady=10)
        self.start_btn = tk.Button(btn_frame, text="START (F7)", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), command=self.start_bot, width=15)
        self.start_btn.pack(side='left', padx=10)
        self.stop_btn = tk.Button(btn_frame, text="STOP (F7)", bg="#f44336", fg="white", font=("Arial", 12, "bold"), command=self.stop_bot, width=15, state='disabled')
        self.stop_btn.pack(side='left', padx=10)

        tk.Button(tab_main, text="👁 MOSTRAR ESCADA (VISUALIZADOR)", bg="#2196F3", fg="white", command=self.toggle_visualizer).pack(pady=5)

        # Teclas e Posições
        keys_frame = tk.LabelFrame(tab_main, text="Teclas e Posições", padx=5, pady=5)
        keys_frame.pack(fill="x", pady=5)
        for d in ['left', 'down', 'up', 'right']:
            r = tk.Frame(keys_frame)
            r.pack(fill='x', pady=2)
            tk.Label(r, text=f"{d.upper()}:", width=6, anchor='w').pack(side='left')
            tk.Entry(r, textvariable=self.key_vars[d], width=5).pack(side='left')
            tk.Button(r, text="Set Pos", command=lambda x=d: self.set_coordinate(x), width=8).pack(side='left', padx=5)
            tk.Label(r, text=str(self.coordinates[d]), fg="green").pack(side='left')

        # --- ABA ESCADA (Configuração Fina) ---
        
        # 1. Cores e Thresholds
        colors_frame = tk.LabelFrame(tab_ladder, text="1. Identificação de Cores (0-255)", padx=10, pady=5)
        colors_frame.pack(fill="x", pady=5)
        
        tk.Label(colors_frame, text="Brilho da NOTA (Cabeça Branca):").pack(anchor='w')
        self.note_thresh = tk.Scale(colors_frame, from_=0, to=255, orient='horizontal', length=350)
        self.note_thresh.set(230) # Você disse 255, deixamos 230 de margem
        self.note_thresh.pack(anchor='w')

        tk.Label(colors_frame, text="Brilho do OUTLINE/BORDA (Separação):").pack(anchor='w')
        self.outline_thresh = tk.Scale(colors_frame, from_=0, to=255, orient='horizontal', length=350)
        self.outline_thresh.set(180) # Você sugeriu 180-200
        self.outline_thresh.pack(anchor='w')

        tk.Label(colors_frame, text="Brilho da LONG NOTE (Corpo Cinza):").pack(anchor='w')
        self.ln_thresh = tk.Scale(colors_frame, from_=0, to=255, orient='horizontal', length=350)
        self.ln_thresh.set(100) # Você sugeriu 150, deixamos 100 pra pegar bem
        self.ln_thresh.pack(anchor='w')
        
        # 2. Geometria
        geo_frame = tk.LabelFrame(tab_ladder, text="2. Tamanho dos Identificadores", padx=10, pady=5)
        geo_frame.pack(fill="x", pady=5)

        tk.Label(geo_frame, text="Altura de cada bloco (Pixels):").pack(anchor='w')
        self.seg_height = tk.Scale(geo_frame, from_=1, to=50, orient='horizontal', length=350)
        self.seg_height.set(10) 
        self.seg_height.pack(anchor='w')

        tk.Label(geo_frame, text="Quantos blocos olhar pra cima?").pack(anchor='w')
        self.num_segs = tk.Scale(geo_frame, from_=1, to=15, orient='horizontal', length=350)
        self.num_segs.set(5) 
        self.num_segs.pack(anchor='w')

        # Debug Console na UI
        tk.Label(self.root, text="Valores em Tempo Real (Use para calibrar):", font=("Arial", 8, "bold")).pack(side='bottom', anchor='w')
        tk.Label(self.root, textvariable=self.debug_info, relief='sunken', anchor='w', bg="#222", fg="#0f0", font=("Consolas", 9)).pack(side='bottom', fill='x')

    def toggle_visualizer(self):
        if self.visualizer:
            self.visualizer.close()
            self.visualizer = None
        else:
            self.visualizer = LadderVisualizer(self.root)
            self.update_visualizer()

    def update_visualizer(self):
        if self.visualizer:
            self.visualizer.draw_ladder(
                self.coordinates, 
                self.seg_height.get(), 
                self.num_segs.get()
            )

    def set_coordinate(self, direction):
        def countdown():
            for i in range(3, 0, -1):
                self.status_var.set(f"Posicione em {direction}... {i}")
                time.sleep(1)
            x, y = pyautogui.position()
            self.coordinates[direction] = (x, y)
            self.root.after(0, self.update_visualizer)
        threading.Thread(target=countdown, daemon=True).start()

    def toggle_bot_state(self):
        if self.running:
            self.root.after(0, self.stop_bot)
        else:
            self.root.after(0, self.start_bot)

    def start_bot(self):
        if self.running: return 
        # Fecha visualizador para performance máxima
        if self.visualizer: self.visualizer.close(); self.visualizer = None
        
        self.running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_var.set("RODANDO... (Aperte F7 para Parar)")
        threading.Thread(target=self.bot_logic, daemon=True).start()

    def stop_bot(self):
        self.running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_var.set("Parado.")

    def bot_logic(self):
        # Lê configurações da UI
        h_seg = self.seg_height.get()     # Altura do bloco
        n_seg = self.num_segs.get()       # Quantos blocos pra cima
        
        th_note = self.note_thresh.get()      # ~230
        th_outline = self.outline_thresh.get()# ~180
        th_ln = self.ln_thresh.get()          # ~100

        keys = {d: self.key_vars[d].get() for d in ['left', 'down', 'up', 'right']}
        holding = {k: False for k in keys}

        # Calcula a área de captura total (Base + Escada pra cima)
        xs = [p[0] for p in self.coordinates.values()]
        ys = [p[1] for p in self.coordinates.values()]
        
        total_height = h_seg * (n_seg + 1)
        
        # O topo da captura é o Y da nota MENOS a altura da escada (pois Y cresce pra baixo)
        monitor = {
            "left": min(xs) - 10,
            "top": min(ys) - (h_seg * n_seg), 
            "width": (max(xs) - min(xs)) + 20,
            "height": total_height + 10
        }

        with mss.mss() as sct:
            while self.running:
                # Captura ultra rápida
                img = np.array(sct.grab(monitor))
                
                debug_text = ""

                for direction, (gx, gy) in self.coordinates.items():
                    rel_x = gx - monitor["left"]
                    
                    # O Y da base (Receptor) é relativo ao topo da imagem capturada
                    # Se capturamos a partir de (Y_nota - AlturaEscada), então o Y_nota na imagem é AlturaEscada
                    base_rel_y = (gy - monitor["top"])
                    
                    k = keys[direction]
                    should_hold = False
                    
                    # --- LÓGICA DE ESCADA ---
                    
                    # 1. Analisa a BASE (Onde bate a nota)
                    # Pega um quadrado 6x6 no centro da lane
                    roi_base = img[base_rel_y:base_rel_y+h_seg, rel_x-3:rel_x+3, 1] # Canal Verde
                    val_base = np.max(roi_base) if roi_base.size > 0 else 0

                    # 2. Analisa o TOPO DA ESCADA (O que vem depois)
                    # Olha o primeiro ou segundo degrau acima
                    y_up = base_rel_y - h_seg 
                    roi_up = img[y_up:y_up+h_seg, rel_x-3:rel_x+3, 1]
                    val_up = np.max(roi_up) if roi_up.size > 0 else 0

                    # DEBUG (Mostra o que o bot vê na Esquerda)
                    if direction == 'left':
                        debug_text = f"LEFT -> Base: {val_base} | Cima: {val_up}"

                    # --- TOMADA DE DECISÃO ---
                    
                    # CASO 1: Tem uma NOTA na base (Branco forte)
                    if val_base > th_note:
                        should_hold = True
                        
                        # Mas... se logo acima for ESCURO (Menor que Outline e LN), é fim de nota
                        # Ou se for a "Borda" (Entre LN e Nota)
                        
                        # Se Cima < LN Threshold -> É PRETO (Fim de nota) -> Solta logo
                        # Se Cima > Outline Threshold -> É OUTRA NOTA COLADA -> Solta pra apertar de novo
                        
                        # Lógica para STREAM (Bolinhas):
                        # Base = 255, Cima = 0 (Preto) ou 180 (Borda)
                        if val_up < th_ln: 
                            # Se em cima é preto, solta na próxima leitura
                            pass 
                        elif val_up < th_note and val_up > th_outline:
                            # Se em cima é a borda (180~200), solta para poder bater na próxima
                            # Aqui está o segredo: Se ver a borda, força soltar!
                            # Para garantir o "mash" rápido, podemos negar o should_hold momentaneamente se já estavamos segurando
                            if holding[direction]: should_hold = False

                    # CASO 2: Tem uma LONG NOTE na base (Cinza médio)
                    elif val_base > th_ln and val_base < th_note:
                        should_hold = True
                        # Continua segurando firme
                    
                    # APLICAÇÃO
                    if should_hold:
                        if not holding[direction]:
                            keyboard.press(k)
                            holding[direction] = True
                    else:
                        if holding[direction]:
                            keyboard.release(k)
                            holding[direction] = False

                # Atualiza debug na tela a cada 10 frames para não travar
                if int(time.time() * 20) % 2 == 0:
                    self.debug_info.set(debug_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = FNFSmartLadderBot(root)
    root.mainloop()