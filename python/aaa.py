import tkinter as tk
from tkinter import ttk
import time

# ===== Prefix system =====
PREFIXES = ["", "k", "m", "b", "t", "qa", "qi", "sx", "sp", "oc", "no", "dc",
            "udc", "ddc", "tdc", "qadc", "qidc", "sxdc", "spdc", "ocdc", "nodc"]

def format_number(n):
    if n < 1000: return str(int(n))
    exp = 0
    while n >= 1000 and exp < len(PREFIXES)-1:
        n /= 1000
        exp += 1
    return f"{n:.2f}{PREFIXES[exp]}".rstrip("0").rstrip(".")

def auto_resize_font(label, max_width, max_height):
    """Resize the font of a label so it fits within max_width and max_height"""
    text = label.cget("text")
    font_size = 20
    while font_size > 5:
        label.config(font=("Arial", font_size, "bold"))
        label.update_idletasks()
        if label.winfo_reqwidth() <= max_width and label.winfo_reqheight() <= max_height:
            break
        font_size -= 1

class ClickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Clicker Simulator")
        self.root.configure(bg="black")

        # ===== Game Variables =====
        self.clicks = 0.0
        self.rebirths = 0
        self.multiplier = 1

        self.manual_click_times = []  # timestamps of manual clicks
        self.auto_cps = 0.0           # CPS from autoclickers

        # autoclickers
        self.shop_items = [
            ["Basic AutoClicker", 5, 100],
            ["Advanced AutoClicker", 25, 400],
            ["Ultra AutoClicker", 80, 1200],
            ["Super AutoClicker", 275, 7500],
            ["Ultrasonic AutoClicker", 360, 12500],
            ["Hyper AutoClicker", 1000, 1_000_000],
            ["Quantum AutoClicker", 5000, 10_000_000],
            ["Singularity AutoClicker", 50_000, 100_000_000],
            ["Omega AutoClicker", 10**80, 10**100]
        ]
        self.owned = {item[0]: 0 for item in self.shop_items}

        # ===== Notebook =====
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # ===== Click Tab =====
        self.tab_click = tk.Frame(self.notebook, bg="black")
        self.notebook.add(self.tab_click, text="Click Farm")

        self.click_label = tk.Label(self.tab_click, text="Clicks: 0", font=("Arial", 20), fg="white", bg="black")
        self.click_label.pack(pady=10)

        self.auto_cps_label = tk.Label(self.tab_click, text="Auto CPS: 0", font=("Arial", 14), fg="cyan", bg="black")
        self.auto_cps_label.pack()
        self.manual_cps_label = tk.Label(self.tab_click, text="Manual CPS: 0", font=("Arial", 14), fg="lightgreen", bg="black")
        self.manual_cps_label.pack()

        # Full screen click area
        self.click_area = tk.Canvas(self.tab_click, bg="black", highlightthickness=0)
        self.click_area.pack(fill="both", expand=True)
        self.click_area.bind("<Button-1>", lambda e: self.manual_click())
        self.click_area.bind("<B1-Motion>", lambda e: self.manual_click())
        self.click_area.bind("<ButtonRelease-1>", lambda e: None)

        # ===== Shop Tab =====
        self.tab_shop = tk.Frame(self.notebook, bg="black")
        self.notebook.add(self.tab_shop, text="Shop")

        self.shop_canvas = tk.Canvas(self.tab_shop, bg="black", highlightthickness=0)
        self.shop_scrollbar = ttk.Scrollbar(self.tab_shop, orient="vertical", command=self.shop_canvas.yview)
        self.shop_scrollable_frame = tk.Frame(self.shop_canvas, bg="black")

        self.shop_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.shop_canvas.configure(
                scrollregion=self.shop_canvas.bbox("all")
            )
        )

        self.shop_canvas.create_window((0, 0), window=self.shop_scrollable_frame, anchor="nw")
        self.shop_canvas.configure(yscrollcommand=self.shop_scrollbar.set)

        self.shop_canvas.pack(side="left", fill="both", expand=True)
        self.shop_scrollbar.pack(side="right", fill="y")

        self.rebirth_button = tk.Button(self.shop_scrollable_frame, text="Rebirth (Cost: 1M)", font=("Arial", 12),
                                        bg="#444", fg="white", command=self.rebirth)
        self.rebirth_button.pack(pady=10, fill="x")

        self.update_shop()

        # Remove CPS table entirely

        self.last_time = time.time()
        self.update_game()

    def manual_click(self):
        self.clicks += 1 * self.multiplier
        self.manual_click_times.append(time.time())

    def buy_item(self, item):
        name, cps, cost = item
        if self.clicks >= cost:
            self.clicks -= cost
            self.owned[name] += 1
            self.auto_cps += cps
            item[2] = int(cost * 1.15)
            self.update_shop()

    def rebirth(self):
        if self.clicks >= 1_000_000:
            self.clicks = 0
            self.auto_cps = 0
            self.rebirths += 1
            self.multiplier *= 2
            for item in self.shop_items:
                self.owned[item[0]] = 0
            self.update_shop()

    def update_shop(self):
        for widget in self.shop_scrollable_frame.winfo_children():
            if widget != self.rebirth_button:
                widget.destroy()
        for item in self.shop_items:
            name, cps, cost = item
            text = f"{name} (+{format_number(cps)} cps)\nCost: {format_number(cost)} | Owned: {self.owned[name]}"
            btn = tk.Button(self.shop_scrollable_frame, text=text, font=("Arial", 12),
                            bg="#222", fg="white", relief="raised",
                            command=lambda i=item: self.buy_item(i))
            btn.pack(pady=5, fill="x")
            auto_resize_font(btn, max_width=300, max_height=60)

    def update_game(self):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        # Auto CPS adds clicks
        self.clicks += self.auto_cps * self.multiplier * dt

        # Manual CPS calculation (real-time)
        cutoff = now - 1
        self.manual_click_times = [t for t in self.manual_click_times if t > cutoff]
        manual_cps = len(self.manual_click_times)

        # Update labels
        self.click_label.config(text=f"Clicks: {format_number(self.clicks)}")
        self.auto_cps_label.config(text=f"Auto CPS: {format_number(self.auto_cps)}")
        self.manual_cps_label.config(text=f"Manual CPS: {format_number(manual_cps)}")

        self.root.after(100, self.update_game)

root = tk.Tk()
root.geometry("400x700")  # mobile-friendly default size
game = ClickerGame(root)
root.mainloop()