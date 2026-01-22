import tkinter as tk
from tkinter import ttk
import threading
import time
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key, Listener, KeyCode

class AutoClickerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Autoclicker")
        self.root.geometry("400x450")
        self.root.resizable(False, False)

        # Controllers
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.running = False
        self.thread = None

        # --- UI LAYOUT ---
        
        # 1. Mouse Settings
        mouse_frame = ttk.LabelFrame(root, text="Mouse Settings", padding=10)
        mouse_frame.pack(fill="x", padx=10, pady=5)

        self.mouse_var = tk.BooleanVar()
        ttk.Checkbutton(mouse_frame, text="Enable Mouse Click (Left Button)", variable=self.mouse_var).pack(anchor="w")

        # 2. Keyboard Settings
        kb_frame = ttk.LabelFrame(root, text="Keyboard Settings", padding=10)
        kb_frame.pack(fill="x", padx=10, pady=5)

        self.kb_var = tk.BooleanVar()
        ttk.Checkbutton(kb_frame, text="Enable Keyboard Spam", variable=self.kb_var).pack(anchor="w")
        
        ttk.Label(kb_frame, text="Keys to press (separate by comma):").pack(anchor="w", pady=(5,0))
        ttk.Label(kb_frame, text="Examples: 'a' or 'a,b' or 'ctrl+c'", font=("Arial", 8, "italic"), foreground="gray").pack(anchor="w")
        
        self.keys_entry = ttk.Entry(kb_frame)
        self.keys_entry.insert(0, "1,2,3,4")
        self.keys_entry.pack(fill="x", pady=5)

        # 3. Speed Settings
        speed_frame = ttk.LabelFrame(root, text="Speed / Delay", padding=10)
        speed_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(speed_frame, text="Delay between clicks (seconds):").pack(side="left")
        self.delay_var = tk.DoubleVar(value=0.01)
        ttk.Entry(speed_frame, textvariable=self.delay_var, width=10).pack(side="right")

        # 4. Status & Instructions
        control_frame = ttk.Frame(root, padding=10)
        control_frame.pack(fill="x", pady=10)

        self.status_label = ttk.Label(control_frame, text="STATUS: STOPPED", foreground="red", font=("Arial", 12, "bold"))
        self.status_label.pack()

        ttk.Label(control_frame, text="Press F6 to Start/Stop").pack(pady=5)
        
        # Start the hotkey listener in background
        self.listener = Listener(on_press=self.on_key_press)
        self.listener.start()

    def on_key_press(self, key):
        # Toggle with F6
        if key == Key.f6:
            if self.running:
                self.stop_clicker()
            else:
                self.start_clicker()

    def start_clicker(self):
        if not self.running:
            self.running = True
            self.status_label.config(text="STATUS: RUNNING", foreground="green")
            # Run the loop in a separate thread so UI doesn't freeze
            self.thread = threading.Thread(target=self.run_loop)
            self.thread.daemon = True
            self.thread.start()

    def stop_clicker(self):
        self.running = False
        self.status_label.config(text="STATUS: STOPPED", foreground="red")

    def parse_key_string(self, key_str):
        """Helper to parse 'ctrl+c' or 'enter' or 'a'"""
        key_str = key_str.strip().lower()
        
        # Handle combinations (e.g., ctrl+c)
        if '+' in key_str:
            mods, char = key_str.rsplit('+', 1)
            # This is a basic implementation for single modifiers
            if 'ctrl' in mods: return (Key.ctrl, char)
            if 'alt' in mods: return (Key.alt, char)
            if 'shift' in mods: return (Key.shift, char)
        
        # Handle special keys
        special_keys = {
            'enter': Key.enter, 'space': Key.space, 'tab': Key.tab, 
            'esc': Key.esc, 'backspace': Key.backspace, 'shift': Key.shift
        }
        if key_str in special_keys:
            return (None, special_keys[key_str])
            
        # Default character
        return (None, key_str)

    def run_loop(self):
        # Read settings once before starting loop to avoid UI threading conflicts
        do_mouse = self.mouse_var.get()
        do_kb = self.kb_var.get()
        delay = self.delay_var.get()
        
        # Parse keys
        raw_keys = self.keys_entry.get().split(',')
        parsed_keys = [self.parse_key_string(k) for k in raw_keys]

        while self.running:
            # 1. Mouse Action
            if do_mouse:
                self.mouse.click(Button.left)

            # 2. Keyboard Action
            if do_kb:
                for mod, key in parsed_keys:
                    if mod:
                        # Handle Combination (hold mod, press key)
                        with self.keyboard.pressed(mod):
                            self.keyboard.press(key)
                            self.keyboard.release(key)
                    else:
                        # Normal Key
                        self.keyboard.press(key)
                        self.keyboard.release(key)

            # 3. Wait
            time.sleep(delay)

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerUI(root)
    root.mainloop()