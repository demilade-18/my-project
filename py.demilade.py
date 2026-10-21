import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

# ---------- ROOM DATA: LR 1 to LR 15 ----------
rooms_data = [
    {"id": "LR1",  "name": "LR 1",  "capacity": 45,  "occupied": False, "building": "Science Hall"},
    {"id": "LR2",  "name": "LR 2",  "capacity": 30,  "occupied": True,  "building": "Science Hall"},
    {"id": "LR3",  "name": "LR 3",  "capacity": 60,  "occupied": False, "building": "Science Hall"},
    {"id": "LR4",  "name": "LR 4",  "capacity": 25,  "occupied": True,  "building": "Humanities"},
    {"id": "LR5",  "name": "LR 5",  "capacity": 50,  "occupied": False, "building": "Humanities"},
    {"id": "LR6",  "name": "LR 6",  "capacity": 35,  "occupied": True,  "building": "Humanities"},
    {"id": "LR7",  "name": "LR 7",  "capacity": 120, "occupied": True,  "building": "Main Building"},
    {"id": "LR8",  "name": "LR 8",  "capacity": 80,  "occupied": False, "building": "Main Building"},
    {"id": "LR9",  "name": "LR 9",  "capacity": 90,  "occupied": True,  "building": "Main Building"},
    {"id": "LR10", "name": "LR 10", "capacity": 20,  "occupied": False, "building": "Library Annex"},
    {"id": "LR11", "name": "LR 11", "capacity": 22,  "occupied": True,  "building": "Library Annex"},
    {"id": "LR12", "name": "LR 12", "capacity": 18,  "occupied": False, "building": "Library Annex"},
    {"id": "LR13", "name": "LR 13", "capacity": 40,  "occupied": True,  "building": "Business School"},
    {"id": "LR14", "name": "LR 14", "capacity": 55,  "occupied": False, "building": "Business School"},
    {"id": "LR15", "name": "LR 15", "capacity": 38,  "occupied": False, "building": "Business School"},
]


class RoomTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trinity University · Room Tracker")
        self.root.configure(bg="#f0f4fa")
        self.root.geometry("1150x780")
        self.root.minsize(800, 600)

        # State
        self.current_filter = "all"  # "all", "empty", "occupied"

        # Colors
        self.COLOR_BG = "#f0f4fa"
        self.COLOR_CARD = "#ffffff"
        self.COLOR_PRIMARY = "#0a3b5b"
        self.COLOR_EMPTY = "#22c55e"
        self.COLOR_OCCUPIED = "#ef4444"
        self.COLOR_EMPTY_BG = "#f7fff9"
        self.COLOR_OCCUPIED_BG = "#fff8f8"
        self.COLOR_BORDER = "#e2edf7"
        self.COLOR_TEXT_DARK = "#0b2d47"
        self.COLOR_TEXT_MUTED = "#456f8e"

        # Fonts
        self.font_brand = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.font_sub = tkfont.Font(family="Segoe UI", size=10)
        self.font_room = tkfont.Font(family="Segoe UI", size=15, weight="bold")
        self.font_badge = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        self.font_small = tkfont.Font(family="Segoe UI", size=9)
        self.font_stat_num = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.font_stat_label = tkfont.Font(family="Segoe UI", size=9)
        self.font_filter = tkfont.Font(family="Segoe UI", size=10, weight="bold")

        # Build UI
        self._build_ui()
        self._refresh_all()

    # ------------------------------------------------------------------
    # UI CONSTRUCTION
    # ------------------------------------------------------------------
    def _build_ui(self):
        # Main container
        main = tk.Frame(self.root, bg=self.COLOR_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # ----- HEADER -----
        header = tk.Frame(main, bg=self.COLOR_BG)
        header.pack(fill="x", pady=(0, 15))

        brand = tk.Frame(header, bg=self.COLOR_BG)
        brand.pack(side="left")
        tk.Label(brand, text="🎓", font=("Segoe UI", 24), bg="#e1f0fa",
                 fg=self.COLOR_PRIMARY, padx=6, pady=2).pack(side="left", padx=(0, 10))
        tk.Label(brand, text="Trinity University", font=self.font_brand,
                 bg=self.COLOR_BG, fg=self.COLOR_TEXT_DARK).pack(side="left")
        tk.Label(brand, text="· room tracker", font=self.font_sub,
                 bg=self.COLOR_BG, fg="#5b7e9b").pack(side="left", padx=(6, 0))

        live = tk.Label(header, text="● LIVE • updated just now", font=self.font_badge,
                        bg="#dcfce7", fg="#166534", padx=14, pady=6)
        live.pack(side="right")

        # Divider
        tk.Frame(main, height=2, bg="#e6edf4").pack(fill="x", pady=(0, 15))

        # ----- STATS CARDS -----
        stats_frame = tk.Frame(main, bg=self.COLOR_BG)
        stats_frame.pack(fill="x", pady=(0, 20))

        self.stat_empty = self._create_stat_card(
            stats_frame, "🚪", "empty rooms", self.COLOR_EMPTY, "#f9fcff")
        self.stat_occupied = self._create_stat_card(
            stats_frame, "🚪", "occupied rooms", self.COLOR_OCCUPIED, "#f9fcff")
        self.stat_total = self._create_stat_card(
            stats_frame, "🏛", "total rooms", "#2563eb", "#f9fcff")

        self.stat_empty.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.stat_occupied.pack(side="left", expand=True, fill="x", padx=5)
        self.stat_total.pack(side="left", expand=True, fill="x", padx=(10, 0))

        # ----- FILTER BAR -----
        filter_frame = tk.Frame(main, bg=self.COLOR_BG)
        filter_frame.pack(fill="x", pady=(0, 15))

        tk.Label(filter_frame, text="🔍 filter:", font=self.font_small,
                 bg=self.COLOR_BG, fg="#5f7d9c").pack(side="left", padx=(0, 8))

        self.filter_buttons = {}
        for key, label in [("all", "All rooms"), ("empty", "Empty"), ("occupied", "Occupied")]:
            btn = tk.Button(
                filter_frame, text=label, font=self.font_filter,
                bg="white", fg="#1f3a57", relief="flat", bd=0,
                padx=16, pady=6, cursor="hand2",
                activebackground="#e8f0f9", activeforeground="#1f3a57",
                command=lambda k=key: self._set_filter(k)
            )
            btn.pack(side="left", padx=(0, 6))
            self.filter_buttons[key] = btn

        # ----- ROOM GRID (scrollable) -----
        grid_outer = tk.Frame(main, bg=self.COLOR_BG)
        grid_outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(grid_outer, bg=self.COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(grid_outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.room_frame = tk.Frame(canvas, bg=self.COLOR_BG)
        self.canvas_window = canvas.create_window(
            (0, 0), window=self.room_frame, anchor="nw")

        def _on_frame_config(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.room_frame.bind("<Configure>", _on_frame_config)

        def _on_canvas_config(event):
            canvas.itemconfig(self.canvas_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_config)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Linux
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        # ----- FOOTER -----
        footer = tk.Frame(main, bg=self.COLOR_BG)
        footer.pack(fill="x", pady=(15, 0))
        tk.Frame(footer, height=1, bg="#e0ecf6").pack(fill="x", pady=(0, 8))
        tk.Label(footer, text="📍 Main campus · LR 1 – LR 15   |   🕐 real-time occupancy   |   🔄 click filter to update",
                 font=self.font_small, bg=self.COLOR_BG, fg="#7a98b3").pack()

    def _create_stat_card(self, parent, icon, label, color, bg):
        card = tk.Frame(parent, bg=bg, bd=1, relief="solid",
                        highlightbackground="#e1eaf2", highlightthickness=1)
        inner = tk.Frame(card, bg=bg)
        inner.pack(padx=18, pady=12, fill="x")

        tk.Label(inner, text=icon, font=("Segoe UI", 18), bg=bg, fg=color).pack(side="left", padx=(0, 12))

        text_frame = tk.Frame(inner, bg=bg)
        text_frame.pack(side="left")
        num_label = tk.Label(text_frame, text="0", font=self.font_stat_num, bg=bg, fg=color)
        num_label.pack(anchor="w")
        tk.Label(text_frame, text=label, font=self.font_stat_label, bg=bg, fg="#4a627a").pack(anchor="w")

        card.num_label = num_label
        return card

    # ------------------------------------------------------------------
    # DATA / LOGIC
    # ------------------------------------------------------------------
    def _compute_stats(self):
        total = len(rooms_data)
        empty = sum(1 for r in rooms_data if not r["occupied"])
        occupied = sum(1 for r in rooms_data if r["occupied"])
        return total, empty, occupied

    def _update_stats(self):
        total, empty, occupied = self._compute_stats()
        self.stat_empty.num_label.config(text=str(empty))
        self.stat_occupied.num_label.config(text=str(occupied))
        self.stat_total.num_label.config(text=str(total))

    def _set_filter(self, key):
        if key == self.current_filter:
            return
        self.current_filter = key
        self._update_filter_buttons()
        self._render_rooms()

    def _update_filter_buttons(self):
        for key, btn in self.filter_buttons.items():
            if key == self.current_filter:
                btn.config(bg=self.COLOR_PRIMARY, fg="white", activebackground="#0e4a70", activeforeground="white")
            else:
                btn.config(bg="white", fg="#1f3a57", activebackground="#e8f0f9", activeforeground="#1f3a57")

    def _get_filtered_rooms(self):
        if self.current_filter == "empty":
            return [r for r in rooms_data if not r["occupied"]]
        elif self.current_filter == "occupied":
            return [r for r in rooms_data if r["occupied"]]
        return rooms_data

    # ------------------------------------------------------------------
    # RENDERING
    # ------------------------------------------------------------------
    def _refresh_all(self):
        self._update_stats()
        self._update_filter_buttons()
        self._render_rooms()

    def _render_rooms(self):
        # Clear existing
        for widget in self.room_frame.winfo_children():
            widget.destroy()

        filtered = self._get_filtered_rooms()

        if not filtered:
            tk.Label(
                self.room_frame,
                text=f"🔎 No {'empty' if self.current_filter == 'empty' else 'occupied'} rooms found.\nTry a different filter.",
                font=("Segoe UI", 12), bg="#f6fafe", fg="#3c5e7c",
                padx=40, pady=40, relief="solid", bd=1
            ).pack(fill="x", padx=5, pady=20)
            return

        # Grid layout: 3 columns responsive
        COLS = 3
        for i, room in enumerate(filtered):
            row = i // COLS
            col = i % COLS
            self._create_room_card(room, row, col)

        # Configure column weights
        for c in range(COLS):
            self.room_frame.grid_columnconfigure(c, weight=1, uniform="room")

    def _create_room_card(self, room, row, col):
        is_empty = not room["occupied"]
        border_color = self.COLOR_EMPTY if is_empty else self.COLOR_OCCUPIED
        bg_color = self.COLOR_EMPTY_BG if is_empty else self.COLOR_OCCUPIED_BG
        status_text = "EMPTY" if is_empty else "OCCUPIED"
        status_icon = "✅" if is_empty else "🔴"

        # Outer card frame (with left colored border)
        card_outer = tk.Frame(self.room_frame, bg=border_color)
        card_outer.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

        # Inner content
        card = tk.Frame(card_outer, bg=bg_color, bd=1, relief="solid",
                        highlightbackground=self.COLOR_BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=(5, 0))  # 5px left border effect

        content = tk.Frame(card, bg=bg_color)
        content.pack(fill="both", expand=True, padx=14, pady=12)

        # Header: room name + capacity
        header = tk.Frame(content, bg=bg_color)
        header.pack(fill="x", pady=(0, 6))

        tk.Label(header, text=room["name"], font=self.font_room,
                 bg=bg_color, fg=self.COLOR_TEXT_DARK).pack(side="left")

        cap_frame = tk.Frame(header, bg="#edf4fc", padx=8, pady=2)
        cap_frame.pack(side="right")
        tk.Label(cap_frame, text=f"👥 {room['capacity']}", font=self.font_small,
                 bg="#edf4fc", fg="#2b4c6b").pack()

        # Status badge
        badge_bg = "#e3f9e9" if is_empty else "#ffe6e6"
        badge_fg = "#0c6b2e" if is_empty else "#a51b1b"
        badge = tk.Frame(content, bg=badge_bg, padx=10, pady=3)
        badge.pack(anchor="w", pady=(0, 10))
        tk.Label(badge, text=f"{status_icon} {status_text}", font=self.font_badge,
                 bg=badge_bg, fg=badge_fg).pack()

        # Divider
        tk.Frame(content, height=1, bg="#d9e5f0").pack(fill="x", pady=(0, 8))

        # Details: building + id
        details = tk.Frame(content, bg=bg_color)
        details.pack(fill="x")
        tk.Label(details, text=f"🏢 {room['building']}", font=self.font_small,
                 bg=bg_color, fg=self.COLOR_TEXT_MUTED).pack(side="left")
        tk.Label(details, text=f"🆔 {room['id']}", font=self.font_small,
                 bg=bg_color, fg=self.COLOR_TEXT_MUTED).pack(side="right")


# ----------------------------------------------------------------------
# ENTRY POINT
# ----------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = RoomTrackerApp(root)
    root.mainloop()

 
