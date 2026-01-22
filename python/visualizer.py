import tkinter as tk
import sounddevice as sd
import numpy as np

class AudioVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Overlay Visualizer")
        
        # --- CONFIGURAÇÃO VISUAL ---
        self.WIDTH = 600
        self.HEIGHT = 1000
        self.BAR_COUNT = 40     # Quantidade de barras
        self.BAR_WIDTH = (self.WIDTH / self.BAR_COUNT)
        
        # Cores e Estilo
        self.BG_COLOR = 'black'        # Cor que ficará invisível
        self.BAR_COLOR = "#ffffff"     # Ciano Neon (Mude para o Hex que quiser)
        
        # Truque de transparência na barra:
        # Use 'gray12', 'gray25', 'gray50', 'gray75' ou '' (vazio) para sólido.
        # Isso cria um efeito de "rede" que deixa ver através da barra.
        self.BAR_STIPPLE = '' 

        # --- CONFIGURAÇÃO DE ÁUDIO/SENSIBILIDADE ---
        self.REFRESH_RATE = 1         # Atualização em ms
        self.SENSITIVITY = 0.1         # Aumente se o som estiver muito baixo
        self.MIN_FREQ_INDEX = 5        # PULA as 5 primeiras frequências (Corrige o problema da esquerda travada)
        self.MAX_FREQ_INDEX = 60       # Foca nas frequências que importam (evita o vazio na direita)

        # --- AUDIO SETUP ---
        self.RATE = 44100
        self.CHUNK = 2048              # Aumentei o Chunk para melhor resolução de graves
        
        try:
            self.stream = sd.InputStream(
                channels=1,
                samplerate=self.RATE,
                blocksize=self.CHUNK,
                dtype='float32'
            )
            self.stream.start()
        except Exception as e:
            print(f"Erro no áudio: {e}")
            self.root.destroy()
            return

        # --- JANELA (OVERLAY) ---
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", self.BG_COLOR)
        
        # Posicionamento
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_pos = (screen_width // 2) - (self.WIDTH // 2)
        y_pos = screen_height - self.HEIGHT - 60
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x_pos}+{y_pos}")

        # --- CANVAS ---
        self.canvas = tk.Canvas(self.root, width=self.WIDTH, height=self.HEIGHT, 
                                bg=self.BG_COLOR, highlightthickness=0)
        self.canvas.pack()

        self.bars = []
        for i in range(self.BAR_COUNT):
            x0 = i * self.BAR_WIDTH
            y0 = self.HEIGHT
            x1 = x0 + self.BAR_WIDTH - 4 # -4 para dar um espacinho entre barras
            y1 = self.HEIGHT
            # O parâmetro stipple cria a semi-transparência
            bar = self.canvas.create_rectangle(x0, y0, x1, y1, 
                                               fill=self.BAR_COLOR, 
                                               outline="",
                                               stipple=self.BAR_STIPPLE) 
            self.bars.append(bar)

        # --- ARRASTAR JANELA ---
        self.offset_x = 0
        self.offset_y = 0
        self.canvas.bind('<Button-1>', self.click_window)
        self.canvas.bind('<B1-Motion>', self.drag_window)
        
        self.update_visualizer()

    def click_window(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def drag_window(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    def update_visualizer(self):
        try:
            # Ler dados
            data, overflow = self.stream.read(self.CHUNK)
            data = data.flatten()
            
            # FFT
            data_fft = np.fft.fft(data)
            frequencies = np.abs(data_fft[:self.CHUNK // 2])
            
            # --- CORREÇÃO DO "TALO NA ESQUERDA" ---
            # Cortamos o array para ignorar o início (ruído DC) e o fim (agudos inaudíveis)
            # Isso dá um "Zoom" na parte da música que interessa
            relevant_freqs = frequencies[self.MIN_FREQ_INDEX : self.MIN_FREQ_INDEX + (self.BAR_COUNT * 4)]
            
            # Se não tiver dados suficientes após o corte, preencher com zeros
            if len(relevant_freqs) < self.BAR_COUNT:
                relevant_freqs = np.pad(relevant_freqs, (0, self.BAR_COUNT - len(relevant_freqs)))

            step = len(relevant_freqs) // self.BAR_COUNT
            if step < 1: step = 1

            for i in range(self.BAR_COUNT):
                start = i * step
                end = (i + 1) * step
                
                if end > len(relevant_freqs):
                    end = len(relevant_freqs)
                
                if end > start:
                    val = np.mean(relevant_freqs[start:end])
                else:
                    val = 0
                
                # --- EQUALIZAÇÃO VISUAL ---
                # Graves têm muita energia, agudos têm pouca.
                # Multiplicamos o valor por 'i' (índice) para aumentar a sensibilidade
                # nas barras da direita (agudos), senão elas nunca sobem.
                equalizer_boost = 1 + (i / self.BAR_COUNT) * 3 
                
                final_height = val * self.HEIGHT * self.SENSITIVITY * equalizer_boost
                
                # Trava a altura máxima
                bar_height = min(self.HEIGHT, final_height)
                
                # Animação
                x0 = i * self.BAR_WIDTH
                y0 = self.HEIGHT - bar_height
                x1 = x0 + self.BAR_WIDTH - 4
                y1 = self.HEIGHT
                
                self.canvas.coords(self.bars[i], x0, y0, x1, y1)
                
        except Exception:
            pass

        self.root.after(self.REFRESH_RATE, self.update_visualizer)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioVisualizer(root)
    root.mainloop()