import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests, json

API = "http://localhost:5000"


class App(tk.Tk):
    def __init__(self):
        super().__init__()

       
        self.title("TechConnect EAI – Desktop Client")
        self.geometry("600x520")          
        self.minsize(550, 400)            

        
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=5, pady=5)

        
        frm_new = ttk.Frame(nb)
        nb.add(frm_new, text="Create Order")

        ttk.Label(frm_new, text="Customer Name").grid(row=0, column=0, sticky="w")
        self.ent_name = ttk.Entry(frm_new, width=40)
        self.ent_name.grid(row=0, column=1, pady=4, sticky="ew")

        ttk.Label(frm_new, text="Total (MYR)").grid(row=1, column=0, sticky="w")
        self.ent_total = ttk.Entry(frm_new, width=20)
        self.ent_total.grid(row=1, column=1, pady=4, sticky="w")

        ttk.Button(frm_new, text="Submit", command=self.create_order)\
           .grid(row=2, column=1, sticky="e", pady=8)

        self.txt_new = scrolledtext.ScrolledText(frm_new, height=12)
        self.txt_new.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(0, 4))

        
        frm_new.columnconfigure(1, weight=1)
        frm_new.rowconfigure(3, weight=1)

     
        frm_pay = ttk.Frame(nb)
        nb.add(frm_pay, text="Payment / Status")

        ttk.Label(frm_pay, text="Order ID").grid(row=0, column=0, sticky="w")
        self.ent_oid = ttk.Entry(frm_pay, width=42)
        self.ent_oid.grid(row=0, column=1, pady=4, sticky="ew")

        btn_frame = ttk.Frame(frm_pay)
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        ttk.Button(btn_frame, text="Make Payment", command=self.make_payment)\
           .pack(side="right", padx=(4, 0))
        ttk.Button(btn_frame, text="Check Status", command=self.check_status)\
           .pack(side="right")

        self.txt_pay = scrolledtext.ScrolledText(frm_pay, height=12)
        self.txt_pay.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(4, 0))

        frm_pay.columnconfigure(1, weight=1)
        frm_pay.rowconfigure(2, weight=1)


    def create_order(self):
        name = self.ent_name.get().strip()
        total = self.ent_total.get().strip()
        if not name or not total:
            messagebox.showwarning("Missing", "Enter name and total.")
            return
        try:
            payload = {"customer": name, "total": float(total), "currency": "MYR"}
            res = requests.post(API + "/api/orders", json=payload, timeout=5)
            res.raise_for_status()
            data = res.json()
            self.txt_new.delete("1.0", tk.END)
            self.txt_new.insert(tk.END, json.dumps(data, indent=2))
            
            self.ent_oid.delete(0, tk.END)
            self.ent_oid.insert(0, data["orderId"])
        except Exception as err:
            messagebox.showerror("Error", str(err))

    def make_payment(self):
        oid = self.ent_oid.get().strip()
        if not oid:
            messagebox.showwarning("Missing", "Enter order ID")
            return
        try:
            
            order = requests.get(f"{API}/api/orders/{oid}", timeout=5).json()
            pay_payload = {
                "orderId": oid,
                "amount": order["total"],
                "method": "card"
            }
            res = requests.post(f"{API}/api/payments", json=pay_payload, timeout=5)
            res.raise_for_status()
            self.txt_pay.delete("1.0", tk.END)
            self.txt_pay.insert(tk.END, json.dumps(res.json(), indent=2))
        except Exception as err:
            messagebox.showerror("Error", str(err))

    def check_status(self):
        oid = self.ent_oid.get().strip()
        if not oid:
            messagebox.showwarning("Missing", "Enter order ID")
            return
        try:
            res = requests.get(f"{API}/api/orders/{oid}", timeout=5)
            res.raise_for_status()
            self.txt_pay.delete("1.0", tk.END)
            self.txt_pay.insert(tk.END, json.dumps(res.json(), indent=2))
        except Exception as err:
            messagebox.showerror("Error", str(err))


if __name__ == "__main__":
    App().mainloop()
