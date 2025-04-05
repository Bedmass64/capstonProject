import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class ToolTip:
    def __init__(self, widget, text='widget info'):
        self.waittime = 500
        self.wraplength = 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def showtip(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(
            self.tw,
            text=self.text,
            justify='left',
            background="#ffffe0",
            relief='solid',
            borderwidth=1,
            wraplength=self.wraplength
        )
        label.pack(ipadx=1)

    def hidetip(self):
        if self.tw:
            self.tw.destroy()
        self.tw = None

class EnhancedTradingStrategyGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trading Strategy Interface")
        self.geometry("1200x800")
        self.configure(bg="#2e2e2e")

        self.current_strategy = None
        self.current_currency = None
        self.current_timeframe = None

        self.setup_styles()
        self.create_menu_bar()
        self.create_widgets()
        self.create_status_bar()

    def setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Title.TLabel", font=("Helvetica", 26, "bold"),
                             foreground="#ffffff", background="#007acc")
        self.style.configure("Menu.TButton", font=("Helvetica", 12, "bold"),
                             foreground="#ffffff", background="#007acc", padding=10)
        self.style.map("Menu.TButton", background=[("active", "#005f99")])
        self.style.configure("TFrame", background="#2e2e2e")
        self.style.configure("TLabel", background="#2e2e2e", foreground="#ffffff", font=("Helvetica", 11))
        self.style.configure("TLabelframe", background="#2e2e2e", foreground="#ffffff", font=("Helvetica", 11, "bold"))
        self.style.configure("TLabelframe.Label", background="#2e2e2e", foreground="#ffffff")

    def create_menu_bar(self):
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menu_bar)

    def create_widgets(self):
        title_frame = ttk.Frame(self, style="TFrame")
        title_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        title_label = ttk.Label(title_frame, text="Trading Strategy Interface",
                                style="Title.TLabel", anchor="center")
        title_label.pack(fill=tk.X, ipady=10)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.menu_frame = ttk.Frame(self, style="TFrame", padding=10)
        self.menu_frame.grid(row=1, column=0, sticky="nsw", padx=10, pady=10)

        self.strategy_setup_frame = ttk.LabelFrame(self.menu_frame, text="Strategy Setup", style="TLabelframe", padding=10)
        self.strategy_setup_frame.pack(pady=5, fill=tk.X)
        
        self.strategy_options = ["Strategy 1", "Strategy 2", "Strategy 3"]
        self.strategy_combobox = ttk.Combobox(self.strategy_setup_frame, values=self.strategy_options,
                                              state="readonly", font=("Helvetica", 11))
        self.strategy_combobox.set("Select Strategy")
        self.strategy_combobox.pack(pady=5, fill=tk.X)
        ToolTip(self.strategy_combobox, "Select the trading strategy")
        
        self.currency_pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"]
        self.currency_pair_combobox = ttk.Combobox(self.strategy_setup_frame, values=self.currency_pairs,
                                                   state="readonly", font=("Helvetica", 11))
        self.currency_pair_combobox.set("Select Currency Pair")
        self.currency_pair_combobox.pack(pady=5, fill=tk.X)
        ToolTip(self.currency_pair_combobox, "Select the currency pair")

        self.time_frames = ["15M", "1H"]
        self.time_frame_combobox = ttk.Combobox(self.strategy_setup_frame, values=self.time_frames,
                                                state="readonly", font=("Helvetica", 11))
        self.time_frame_combobox.set("Select Time Frame")
        self.time_frame_combobox.pack(pady=5, fill=tk.X)
        ToolTip(self.time_frame_combobox, "Select the time frame")

        self.confirm_setup_button = ttk.Button(self.strategy_setup_frame, text="Confirm Setup", style="Menu.TButton", command=self.confirm_setup)
        self.confirm_setup_button.pack(pady=5, fill=tk.X)
        ToolTip(self.confirm_setup_button, "Confirm your selections")
        
        self.analysis_frame = ttk.Frame(self.menu_frame, style="TFrame")

        self.profit_button = ttk.Button(self.analysis_frame, text="Profit Factor", style="Menu.TButton", command=self.show_profit_factor)
        self.profit_button.pack(pady=5, fill=tk.X)
        ToolTip(self.profit_button, "Display the Profit Factor analysis image")

        self.statistics_button = ttk.Button(self.analysis_frame, text="Strategy Statistics", style="Menu.TButton", command=self.show_strategy_statistics)
        self.statistics_button.pack(pady=5, fill=tk.X)
        ToolTip(self.statistics_button, "Display the strategy statistics page")

        self.trade_frame = ttk.LabelFrame(self.menu_frame, text="Trade Examples", style="TLabelframe", padding=10)
        self.trade_options = ["Trade 1", "Trade 2", "Trade 3"]
        self.trade_combobox = ttk.Combobox(self.trade_frame, values=self.trade_options,
                                           state="readonly", font=("Helvetica", 11))
        self.trade_combobox.set("Select Trade")
        self.trade_combobox.pack(pady=5, fill=tk.X)
        ToolTip(self.trade_combobox, "Choose a trade example to display")
        self.trade_show_button = ttk.Button(self.trade_frame, text="Load Trade", style="Menu.TButton", command=self.show_selected_trade)
        self.trade_show_button.pack(pady=5, fill=tk.X)
        ToolTip(self.trade_show_button, "Display the image for the selected trade example")

        self.display_frame = ttk.Frame(self, style="TFrame", padding=10)
        self.display_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.display_frame.grid_rowconfigure(0, weight=1)
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_label = ttk.Label(self.display_frame, background="#ffffff", anchor="center")
        self.display_label.grid(row=0, column=0, sticky="nsew")
        
        self.display_label.config(text="Please complete strategy setup", font=("Helvetica", 16))

    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self, textvariable=self.status_var, anchor="w",
                               relief="sunken", font=("Helvetica", 10))
        status_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

    def load_image(self, filepath, size=(800, 600)):
        try:
            img = Image.open(filepath)
            img = img.resize(size, Image.ANTIALIAS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {filepath}: {e}")
            return None

    def load_dynamic_image(self, image_type, strategy, currency, timeframe, trade=None):
        """
        Construct the filename based on the selections.
        The currency pair is sanitized by replacing "/" with "-" to avoid folder issues.
        Expected file naming convention (for example):
          - Profit Factor: "Strategy 1_EUR-USD_1H_profit_factor.png"
          - Strategy Statistics: "Strategy 1_EUR-USD_1H_strategy_statistics.png"
          - Trade Example: "Strategy 1_EUR-USD_1H_trade_1.png" (if trade == "1")
        """
        safe_currency = currency.replace("/", "-")
        if trade is None:
            filename = f"{strategy}_{safe_currency}_{timeframe}_{image_type}.png"
        else:
            filename = f"{strategy}_{safe_currency}_{timeframe}_trade_{trade}.png"
        return self.load_image(filename, size=(800, 600))

    def confirm_setup(self):
        strategy = self.strategy_combobox.get()
        currency = self.currency_pair_combobox.get()
        timeframe = self.time_frame_combobox.get()
        if strategy == "Select Strategy" or currency == "Select Currency Pair" or timeframe == "Select Time Frame":
            messagebox.showwarning("Setup Incomplete", "Please select a strategy, currency pair, and time frame.")
            self.status_var.set("Setup incomplete: please make all selections.")
        else:
            self.current_strategy = strategy
            self.current_currency = currency
            self.current_timeframe = timeframe
            self.status_var.set(f"Setup confirmed: {strategy}, {currency}, {timeframe}")
            
            self.profit_factor_image = self.load_dynamic_image("profit_factor", strategy, currency, timeframe)
            self.strategy_statistics_image = self.load_dynamic_image("strategy_statistics", strategy, currency, timeframe)
            
            self.trade_images = {}
            for option in self.trade_options:
                trade_num = option.split()[1]
                self.trade_images[option] = self.load_dynamic_image("trade", strategy, currency, timeframe, trade=trade_num)
            
            self.analysis_frame.pack(pady=10, fill=tk.X)
            self.trade_frame.pack(pady=10, fill=tk.X)
            
            if self.profit_factor_image:
                self.display_label.config(image=self.profit_factor_image, text="")
            else:
                self.display_label.config(text="Profit Factor image not found", image="")

    def show_profit_factor(self):
        if hasattr(self, "profit_factor_image") and self.profit_factor_image:
            self.display_label.config(image=self.profit_factor_image, text="")
            self.status_var.set("Displaying Profit Factor")
        else:
            self.display_label.config(text="Profit Factor image not found", image="")
            self.status_var.set("Error: Profit Factor image not found")

    def show_strategy_statistics(self):
        if hasattr(self, "strategy_statistics_image") and self.strategy_statistics_image:
            self.display_label.config(image=self.strategy_statistics_image, text="")
            self.status_var.set("Displaying Strategy Statistics")
        else:
            self.display_label.config(text="Strategy Statistics image not found", image="")
            self.status_var.set("Error: Strategy Statistics image not found")

    def show_selected_trade(self):
        selected_trade = self.trade_combobox.get()
        if selected_trade in self.trade_images and self.trade_images[selected_trade]:
            self.display_label.config(image=self.trade_images[selected_trade], text="")
            self.status_var.set(f"Displaying {selected_trade}")
        else:
            self.display_label.config(text=f"{selected_trade} image not found", image="")
            self.status_var.set(f"Error: {selected_trade} image not found")
    
    def show_about(self):
        messagebox.showinfo("About", "Trading Strategy Interface\nVersion 2.0\nDeveloped by Your Name")

if __name__ == "__main__":
    app = EnhancedTradingStrategyGUI()
    app.mainloop()
