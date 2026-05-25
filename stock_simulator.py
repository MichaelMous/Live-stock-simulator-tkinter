import tkinter as tk
from tkinter import messagebox
import random

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Stock Simulator")
        self.root.geometry("650x550")
        
        self.balance = 10000.0
        self.stocks = {"AAPL": 150.0, "TSLA": 200.0, "GOOG": 2800.0, "AMZN": 3400.0, "BTC": 45000.0}
        self.portfolio = {name: 0 for name in self.stocks}
        self.history = []

        self.setup_ui()
        self.update_display()
        
        self.auto_refresh()

    def setup_ui(self):
        self.lbl_balance = tk.Label(self.root, text="", font=('Arial', 11, 'bold'), fg="blue")
        self.lbl_balance.pack(pady=10)

        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        market_frame = tk.Frame(main_frame)
        market_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        tk.Label(market_frame, text="Αγορά (Τιμές ανανεώνονται LIVE)", fg="green").pack()
        self.lst_stocks = tk.Listbox(market_frame, height=10, exportselection=False, font=('Courier', 10))
        self.lst_stocks.pack(fill=tk.BOTH, expand=True)

        port_frame = tk.Frame(main_frame)
        port_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        tk.Label(port_frame, text="Το Portfolio μου", fg="brown").pack()
        self.lst_portfolio = tk.Listbox(port_frame, height=10, exportselection=False, font=('Courier', 10))
        self.lst_portfolio.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Αγορά (1)", command=self.buy_stock, bg="#d4edda", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Πώληση (1)", command=self.sell_stock, bg="#f8d7da", width=15).pack(side=tk.LEFT, padx=5)

        tk.Label(self.root, text="Ιστορικό Συναλλαγών").pack()
        self.lst_history = tk.Listbox(self.root, height=5, bg="#f9f9f9", font=('Arial', 9))
        self.lst_history.pack(padx=10, pady=5, fill=tk.X)

    def auto_refresh(self):
        for stock in self.stocks:
            change = random.uniform(-0.03, 0.03) 
            self.stocks[stock] *= (1 + change)
        
        self.update_display()
        self.root.after(3000, self.auto_refresh)

    def buy_stock(self):
        selection = self.lst_stocks.curselection()
        if not selection: return
        
        stock_name = list(self.stocks.keys())[selection[0]]
        price = self.stocks[stock_name]

        if self.balance >= price:
            self.balance -= price
            self.portfolio[stock_name] += 1
            self.history.insert(0, f"ΑΓΟΡΑ: 1 {stock_name} @ {price:.2f}€")
            self.update_display()
        else:
            messagebox.showwarning("Πρόβλημα", "Ανεπαρκές υπόλοιπο!")

    def sell_stock(self):
        selection = self.lst_portfolio.curselection()
        if not selection: return
        
        stock_name = list(self.portfolio.keys())[selection[0]]
        price = self.stocks[stock_name]

        if self.portfolio[stock_name] > 0:
            self.balance += price
            self.portfolio[stock_name] -= 1
            self.history.insert(0, f"ΠΩΛΗΣΗ: 1 {stock_name} @ {price:.2f}€")
            self.update_display()
        else:
            messagebox.showwarning("Πρόβλημα", "Δεν έχετε μετοχές προς πώληση!")

    def update_display(self):
        m_idx = self.lst_stocks.curselection()
        p_idx = self.lst_portfolio.curselection()

        self.lst_stocks.delete(0, tk.END)
        for name, price in self.stocks.items():
            self.lst_stocks.insert(tk.END, f"{name:8} | {price:>10.2f}€")
        if m_idx: self.lst_stocks.selection_set(m_idx)

        self.lst_portfolio.delete(0, tk.END)
        total_val = 0
        for name, qty in self.portfolio.items():
            val = qty * self.stocks[name]
            total_val += val
            self.lst_portfolio.insert(tk.END, f"{name:8} | {qty} τεμ. ({val:>8.2f}€)")
        if p_idx: self.lst_portfolio.selection_set(p_idx)

        self.lbl_balance.config(text=f"Μετρητά: {self.balance:.2f}€ | Αξία Portfolio: {total_val:.2f}€")
        
        self.lst_history.delete(0, tk.END)
        for entry in self.history[:10]: 
            self.lst_history.insert(tk.END, entry)

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()