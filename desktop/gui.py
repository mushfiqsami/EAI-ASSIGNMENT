"""
Tkinter desktop client for the TechConnect EAI Demo API.
Run me with:  python desktop/gui.py   (after you start backend/app.py)

Requires: requests  (already in requirements.txt)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests, json, re

API = "http://localhost:5000"          # <— change only if backend port / host differ
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)

class App(tk.Tk):
    def __init__(self):
        super().__init__()             # fixed: one leading, two trailing underscores
        self.title("TechConnect EAI – Desktop Client")
        self.geometry("520x460")

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=6, pady=6)

        # ─────────────────── tab 1: Create Order ───────────────────
        tab_create = ttk.Frame(nb)
        nb.add(tab_create, text="Create Order")

        ttk.Label(tab_create, text="Customer Name").grid(row=0, column=0, sticky="w")
        self.ent_name = ttk.Entry(tab_create, width=40)
        self.ent_name.grid(row=0, column=1, padx=4, pady=4)

        ttk.Label(tab_create, text="Total (MYR)").grid(row=1, column=0, sticky="w")
        self.ent_total = ttk.Entry(tab_create, width=15)
        self.ent_total.grid(row=1, column=1, padx=4, pady=4, sticky="w")

        ttk.Button(tab_create, text="Submit", command=self.create_order)\
           .grid(row=2, column=1, sticky="e", pady=6)

        self.txt_new = scrolledtext.ScrolledText(tab_create, height=12)
        self.txt_new.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(0,4))
        tab_create.rowconfigure(3, weight=1)

        # ─────────────────── tab 2: Pay / Status ───────────────────
        tab_pay = ttk.Frame(nb)
        nb.add(tab_pay, text="Payment / Status")

        ttk.Label(tab_pay, text="Order ID").grid(row=0, column=0, sticky="w")
        self.ent_oid = ttk.Entry(tab_pay, width=45)
        self.ent_oid.grid(row=0, column=1, padx=4, pady=4)

        ttk.Button(tab_pay, text="Make Payment", command=self.make_payment)\
           .grid(row=1, column=1, sticky="e", pady=6)
        ttk.Button(tab_pay, text="Check Status", command=self.check_status)\
           .grid(row=1, column=0, sticky="w", padx=4)

        self.txt_pay = scrolledtext.ScrolledText(tab_pay, height=12)
        self.txt_pay.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0,4))
        tab_pay.rowconfigure(2, weight=1)

    # ───────────────────────── helpers ────────────────────────────
    def _show_json(self, widget: scrolledtext.ScrolledText, data: dict):
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, json.dumps(data, indent=2))

    def _error(self, err):
        messagebox.showerror("Error", str(err))

    # ───────────────────── API calls ───────────────────────────────
    def create_order(self):
        name  = self.ent_name.get().strip()
        total = self.ent_total.get().strip()

        if not name or not total:
            messagebox.showwarning("Missing data", "Please fill Customer Name and Total.")
            return
        try:
            payload = {"customer": name,
                       "total": float(total),
                       "currency": "MYR"}
        except ValueError:
            messagebox.showwarning("Invalid total", "Total (MYR) must be a number.")
            return

        try:
            print("[GUI] POST /api/orders", payload)
            r = requests.post(f"{API}/api/orders", json=payload, timeout=5)
            r.raise_for_status()
            data = r.json()
            self._show_json(self.txt_new, data)

            # prep the Payment tab
            self.ent_oid.delete(0, tk.END)
            self.ent_oid.insert(0, data["orderId"])
        except Exception as e:
            self._error(e)

    def make_payment(self):
        order_id = self.ent_oid.get().strip()
        if not order_id:
            messagebox.showwarning("Missing", "Enter order ID")
            return
        try:
            # Fetch the order so we know the correct amount
            ord_res = requests.get(API + f"/api/orders/{order_id}", timeout=5)
            ord_res.raise_for_status()
            order = ord_res.json()
            amount = order["total"]

            pay_payload = {
                "orderId": order_id,
                "amount": amount,
                "method": "card"
            }
            print("[GUI] POST /api/payments", pay_payload)
            pay_res = requests.post(API + "/api/payments",
                                    json=pay_payload,
                                    timeout=5)
            pay_res.raise_for_status()

            self.txt_pay.delete("1.0", tk.END)
            self.txt_pay.insert(tk.END, json.dumps(pay_res.json(), indent=2))
        except Exception as err:
            messagebox.showerror("Error", str(err))



    def check_status(self):
        oid = self.ent_oid.get().strip()
        if not UUID_RE.match(oid):
            messagebox.showwarning("Order ID", "Paste a valid orderId from the first tab.")
            return
        try:
            print("[GUI] GET /api/orders/" + oid)
            r = requests.get(f"{API}/api/orders/{oid}", timeout=5)
            r.raise_for_status()
            self._show_json(self.txt_pay, r.json())
        except Exception as e:
            self._error(e)


if __name__ == "__main__":
    App().mainloop()
