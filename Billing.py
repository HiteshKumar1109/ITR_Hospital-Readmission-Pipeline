from tkinter import *
from tkinter import ttk, messagebox
import sqlite3 as sq
import time
import os

class BillingClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1300x700+25+20")
        self.root.title("Billing & Invoicing System")
        self.root.config(bg="#f4f6f8")
        self.root.focus_force()

        # Variables
        self.var_search_txt = StringVar()
        self.var_cust_name = StringVar()
        self.var_cust_contact = StringVar()
        
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()
        self.var_pid = None

        self.cart_list = [] # Stores dictionary of cart items
        
        # Title
        title = Label(self.root, text="Billing & Invoicing System", font=("Segoe UI", 22, "bold"), bg="#2C3E50", fg="white", pady=10)
        title.pack(fill=X)

        # Main Layout
        # Left Panel (Products)
        left_frame = LabelFrame(self.root, text="Products", font=("Segoe UI", 12, "bold"), bg="white", bd=2, relief=RIDGE)
        left_frame.place(x=10, y=70, width=420, height=610)

        # Search Products
        lbl_search = Label(left_frame, text="Search (Name):", font=("Segoe UI", 11, "bold"), bg="white")
        lbl_search.place(x=10, y=10)
        txt_search = Entry(left_frame, textvariable=self.var_search_txt, font=("Segoe UI", 11), bg="#f9f9f9", bd=2, relief=GROOVE)
        txt_search.place(x=130, y=10, width=160)
        txt_search.bind("<KeyRelease>", self.search_product)

        btn_show_all = Button(left_frame, text="Show All", command=self.show_products, font=("Segoe UI", 10, "bold"), bg="#546e7a", fg="white", cursor="hand2", bd=0)
        btn_show_all.place(x=300, y=10, width=90, height=28)

        # Treeview for Products
        table_frame = Frame(left_frame, bg="white", bd=1, relief=RIDGE)
        table_frame.place(x=10, y=50, width=390, height=360)

        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(table_frame, columns=("pid", "name", "price", "qty", "status"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="ID")
        self.product_table.heading("name", text="Product Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Stock")
        self.product_table.heading("status", text="Status")
        self.product_table["show"] = "headings"

        self.product_table.column("pid", width=40)
        self.product_table.column("name", width=140)
        self.product_table.column("price", width=70)
        self.product_table.column("qty", width=60)
        self.product_table.column("status", width=70)
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_selected_product)

        # Selected Product Form
        form_frame = Frame(left_frame, bg="white")
        form_frame.place(x=10, y=420, width=390, height=160)

        Label(form_frame, text="Product Name", font=("Segoe UI", 11, "bold"), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        Entry(form_frame, textvariable=self.var_pname, font=("Segoe UI", 11), bg="#f5f5f5", state="readonly", width=20).grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="Price", font=("Segoe UI", 11, "bold"), bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        Entry(form_frame, textvariable=self.var_price, font=("Segoe UI", 11), bg="#f5f5f5", state="readonly", width=20).grid(row=1, column=1, padx=5, pady=5)

        Label(form_frame, text="Stock Available", font=("Segoe UI", 11, "bold"), bg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        Entry(form_frame, textvariable=self.var_stock, font=("Segoe UI", 11), bg="#f5f5f5", state="readonly", width=20).grid(row=2, column=1, padx=5, pady=5)

        Label(form_frame, text="Quantity to Buy", font=("Segoe UI", 11, "bold"), bg="white").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        Entry(form_frame, textvariable=self.var_qty, font=("Segoe UI", 11), bg="#fffde7", bd=2, relief=GROOVE, width=20).grid(row=3, column=1, padx=5, pady=5)

        btn_add_cart = Button(form_frame, text="Add to Cart", command=self.add_to_cart, font=("Segoe UI", 11, "bold"), bg="#1976d2", fg="white", cursor="hand2", bd=0)
        btn_add_cart.place(x=275, y=110, width=105, height=35)


        # Middle Panel (Cart & Customer Info)
        middle_frame = Frame(self.root, bg="#f4f6f8")
        middle_frame.place(x=440, y=70, width=440, height=610)

        # Customer Frame
        cust_frame = LabelFrame(middle_frame, text="Customer Details", font=("Segoe UI", 11, "bold"), bg="white", bd=2, relief=RIDGE)
        cust_frame.pack(fill=X, pady=(0, 10))
        cust_frame.config(height=90)
        cust_frame.pack_propagate(False)

        Label(cust_frame, text="Name:", font=("Segoe UI", 10, "bold"), bg="white").place(x=10, y=10)
        Entry(cust_frame, textvariable=self.var_cust_name, font=("Segoe UI", 10), bg="#f9f9f9", bd=2, relief=GROOVE).place(x=70, y=8, width=130)

        Label(cust_frame, text="Contact:", font=("Segoe UI", 10, "bold"), bg="white").place(x=215, y=10)
        Entry(cust_frame, textvariable=self.var_cust_contact, font=("Segoe UI", 10), bg="#f9f9f9", bd=2, relief=GROOVE).place(x=280, y=8, width=130)

        # Cart Table Frame
        cart_table_frame = LabelFrame(middle_frame, text="Shopping Cart", font=("Segoe UI", 11, "bold"), bg="white", bd=2, relief=RIDGE)
        cart_table_frame.pack(fill=BOTH, expand=1)

        scrolly_c = Scrollbar(cart_table_frame, orient=VERTICAL)
        scrollx_c = Scrollbar(cart_table_frame, orient=HORIZONTAL)

        self.cart_table = ttk.Treeview(cart_table_frame, columns=("pid", "name", "price", "qty", "total"), xscrollcommand=scrollx_c.set, yscrollcommand=scrolly_c.set)
        scrollx_c.pack(side=BOTTOM, fill=X)
        scrolly_c.pack(side=RIGHT, fill=Y)
        scrollx_c.config(command=self.cart_table.xview)
        scrolly_c.config(command=self.cart_table.yview)

        self.cart_table.heading("pid", text="ID")
        self.cart_table.heading("name", text="Product Name")
        self.cart_table.heading("price", text="Price")
        self.cart_table.heading("qty", text="Qty")
        self.cart_table.heading("total", text="Total")
        self.cart_table["show"] = "headings"

        self.cart_table.column("pid", width=40)
        self.cart_table.column("name", width=150)
        self.cart_table.column("price", width=70)
        self.cart_table.column("qty", width=50)
        self.cart_table.column("total", width=80)
        self.cart_table.pack(fill=BOTH, expand=1)

        # Cart Calculations and Actions
        calc_frame = Frame(middle_frame, bg="white", bd=2, relief=RIDGE)
        calc_frame.pack(fill=X, pady=10)

        self.lbl_subtotal = Label(calc_frame, text="Sub Total: 0.00", font=("Segoe UI", 11, "bold"), bg="white", fg="#333")
        self.lbl_subtotal.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.lbl_tax = Label(calc_frame, text="Tax (5%): 0.00", font=("Segoe UI", 11, "bold"), bg="white", fg="#333")
        self.lbl_tax.grid(row=0, column=1, padx=20, pady=5, sticky="w")

        self.lbl_netpay = Label(calc_frame, text="Net Pay: 0.00", font=("Segoe UI", 13, "bold"), bg="white", fg="#27ae60")
        self.lbl_netpay.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        # Cart Buttons
        cart_btn_frame = Frame(middle_frame, bg="#f4f6f8", height=45)
        cart_btn_frame.pack(fill=X, pady=5)

        Button(cart_btn_frame, text="Remove Selected", command=self.remove_from_cart, font=("Segoe UI", 10, "bold"), bg="#e53935", fg="white", cursor="hand2", bd=0).place(x=0, y=0, width=135, height=35)
        Button(cart_btn_frame, text="Clear Cart", command=self.clear_cart, font=("Segoe UI", 10, "bold"), bg="#546e7a", fg="white", cursor="hand2", bd=0).place(x=145, y=0, width=100, height=35)
        Button(cart_btn_frame, text="Generate Bill", command=self.generate_bill, font=("Segoe UI", 11, "bold"), bg="#2e7d32", fg="white", cursor="hand2", bd=0).place(x=255, y=0, width=175, height=35)


        # Right Panel (Invoice Preview)
        right_frame = LabelFrame(self.root, text="Invoice Preview", font=("Segoe UI", 12, "bold"), bg="white", bd=2, relief=RIDGE)
        right_frame.place(x=890, y=70, width=400, height=610)

        # Invoice Text Widget
        self.txt_invoice = Text(right_frame, font=("Courier New", 10), bg="#fafafa", bd=1, relief=SUNKEN)
        self.txt_invoice.pack(fill=BOTH, expand=1, padx=10, pady=10)

        # Actions at startup
        self.show_products()
        self.clear_all()

    # ----------------------------------------------------
    # Database Operations
    # ----------------------------------------------------
    def show_products(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            cur.execute("SELECT pid, name, price, qty, status FROM product")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Database Error", f"Failed to load products:\n{str(ex)}", parent=self.root)
            print(f"Database Error: {str(ex)}")
        finally:
            con.close()

    def search_product(self, ev):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            query = "SELECT pid, name, price, qty, status FROM product WHERE name LIKE ?"
            cur.execute(query, ('%' + self.var_search_txt.get() + '%',))
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Database Error", f"Failed to search products:\n{str(ex)}", parent=self.root)
            print(f"Database Error: {str(ex)}")
        finally:
            con.close()

    def get_selected_product(self, ev):
        f = self.product_table.focus()
        content = self.product_table.item(f)
        row = content['values']
        if row:
            self.var_pid = row[0]
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.var_stock.set(row[3])
            self.var_qty.set("1")

    # ----------------------------------------------------
    # Cart Operations
    # ----------------------------------------------------
    def add_to_cart(self):
        if self.var_pid is None:
            messagebox.showerror("Error", "Please select a product from the list", parent=self.root)
            return
        if self.var_qty.get() == "":
            messagebox.showerror("Error", "Please enter quantity", parent=self.root)
            return

        try:
            qty_val = int(self.var_qty.get())
            if qty_val <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0", parent=self.root)
                return
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a valid integer", parent=self.root)
            return

        status = self.product_table.item(self.product_table.focus())['values'][4]
        if status != "Active":
            messagebox.showerror("Error", "Selected product is currently Inactive", parent=self.root)
            return

        stock = int(self.var_stock.get())
        if qty_val > stock:
            messagebox.showerror("Error", f"Insufficient Stock! Only {stock} items available.", parent=self.root)
            return

        # Check if already in cart
        for item in self.cart_list:
            if item['pid'] == self.var_pid:
                # Update quantity
                if item['qty'] + qty_val > stock:
                    messagebox.showerror("Error", f"Cannot add. Total in cart ({item['qty'] + qty_val}) exceeds stock ({stock})", parent=self.root)
                    return
                item['qty'] += qty_val
                item['total'] = item['qty'] * item['price']
                self.update_cart_display()
                self.calculate_bill()
                return

        # Add new item
        self.cart_list.append({
            'pid': self.var_pid,
            'name': self.var_pname.get(),
            'price': float(self.var_price.get()),
            'qty': qty_val,
            'total': qty_val * float(self.var_price.get())
        })
        self.update_cart_display()
        self.calculate_bill()

    def remove_from_cart(self):
        f = self.cart_table.focus()
        content = self.cart_table.item(f)
        row = content['values']
        if not row:
            messagebox.showerror("Error", "Please select an item from the cart to remove", parent=self.root)
            return
        pid = row[0]
        self.cart_list = [item for item in self.cart_list if item['pid'] != pid]
        self.update_cart_display()
        self.calculate_bill()

    def update_cart_display(self):
        self.cart_table.delete(*self.cart_table.get_children())
        for item in self.cart_list:
            self.cart_table.insert('', END, values=(item['pid'], item['name'], item['price'], item['qty'], item['total']))

    def calculate_bill(self):
        subtotal = sum(item['total'] for item in self.cart_list)
        tax = subtotal * 0.05
        netpay = subtotal + tax
        self.lbl_subtotal.config(text=f"Sub Total: {subtotal:.2f}")
        self.lbl_tax.config(text=f"Tax (5%): {tax:.2f}")
        self.lbl_netpay.config(text=f"Net Pay: {netpay:.2f}")

    def clear_cart(self):
        self.cart_list.clear()
        self.update_cart_display()
        self.calculate_bill()

    def clear_all(self):
        self.var_cust_name.set("")
        self.var_cust_contact.set("")
        self.var_search_txt.set("")
        self.var_pid = None
        self.var_pname.set("")
        self.var_price.set("")
        self.var_stock.set("")
        self.var_qty.set("")
        self.txt_invoice.delete('1.0', END)
        self.clear_cart()
        self.show_products()

    # ----------------------------------------------------
    # Generate Invoice & Save to DB
    # ----------------------------------------------------
    def generate_bill(self):
        if not self.cart_list:
            messagebox.showerror("Error", "Shopping Cart is empty", parent=self.root)
            return
        if self.var_cust_name.get() == "" or self.var_cust_contact.get() == "":
            messagebox.showerror("Error", "Customer details are required", parent=self.root)
            return

        invoice_no = "INV-" + time.strftime("%Y%m%d%H%M%S")
        bill_date = time.strftime("%Y-%m-%d")
        bill_time = time.strftime("%I:%M %p")
        
        # Calculate totals
        subtotal = sum(item['total'] for item in self.cart_list)
        tax = subtotal * 0.05
        netpay = subtotal + tax

        # Use absolute database path
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            # 1. Insert Billing Record FIRST (with customer details)
            cur.execute("""
                INSERT INTO billing (invoice, customer_name, customer_contact, bill_date, bill_time, subtotal, tax, total_amount, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                invoice_no,
                self.var_cust_name.get(),
                self.var_cust_contact.get(),
                bill_date,
                bill_time,
                subtotal,
                tax,
                netpay,
                "Completed"
            ))
            
            # 2. Deduct Stock and Insert Sales Records
            for item in self.cart_list:
                # Get current stock
                cur.execute("SELECT qty FROM product WHERE pid=?", (item['pid'],))
                result = cur.fetchone()
                if result is None:
                    raise Exception(f"Product with ID {item['pid']} not found in database")
                
                current_stock = int(result[0])
                new_stock = current_stock - item['qty']
                
                if new_stock < 0:
                    raise Exception(f"Insufficient stock for product {item['name']}")
                
                # Update stock
                cur.execute("UPDATE product SET qty=? WHERE pid=?", (str(new_stock), item['pid']))
                
                # Insert Sale Record
                cur.execute("INSERT INTO sales (invoice, date, product_name, price, qty, total) VALUES (?, ?, ?, ?, ?, ?)", (
                    invoice_no,
                    bill_date,
                    item['name'],
                    item['price'],
                    item['qty'],
                    item['total']
                ))
            con.commit()

            # Create bill folder if not exists
            if not os.path.exists("bill"):
                os.makedirs("bill")

            # 3. Write Text Invoice File
            bill_content = self.generate_invoice_string(invoice_no, bill_date, bill_time)
            with open(f"bill/{invoice_no}.txt", "w") as f:
                f.write(bill_content)

            self.txt_invoice.delete('1.0', END)
            self.txt_invoice.insert(END, bill_content)

            messagebox.showinfo("Success", f"Invoice {invoice_no} generated and saved to database successfully!", parent=self.root)
            # Clear inputs and cart, but keep invoice preview text
            self.var_cust_name.set("")
            self.var_cust_contact.set("")
            self.var_search_txt.set("")
            self.var_pid = None
            self.var_pname.set("")
            self.var_price.set("")
            self.var_stock.set("")
            self.var_qty.set("")
            self.clear_cart()
            self.show_products()
            
        except Exception as ex:
            con.rollback()
            messagebox.showerror("Database Error", f"Failed to save billing record:\n{str(ex)}", parent=self.root)
            print(f"Database Error: {str(ex)}")  # Print to console for debugging
        finally:
            con.close()

    def generate_invoice_string(self, invoice_no, date, time_str):
        subtotal = sum(item['total'] for item in self.cart_list)
        tax = subtotal * 0.05
        netpay = subtotal + tax

        invoice = "="*44 + "\n"
        invoice += "         INVENTORY MANAGEMENT SYSTEM         \n"
        invoice += "              SALES INVOICE                  \n"
        invoice += "="*44 + "\n"
        invoice += f" Invoice No: {invoice_no}\n"
        invoice += f" Date: {date}               Time: {time_str}\n"
        invoice += f" Customer Name: {self.var_cust_name.get()}\n"
        invoice += f" Customer Contact: {self.var_cust_contact.get()}\n"
        invoice += "="*44 + "\n"
        invoice += " Product Name        Qty    Price    Total\n"
        invoice += "="*44 + "\n"

        for item in self.cart_list:
            name_part = item['name'][:18]
            invoice += f" {name_part:<19} {item['qty']:<6} {item['price']:<8.2f} {item['total']:<8.2f}\n"

        invoice += "="*44 + "\n"
        invoice += f" Sub Total:                          {subtotal:>8.2f}\n"
        invoice += f" Tax (5%):                           {tax:>8.2f}\n"
        invoice += f" Net Pay:                            {netpay:>8.2f}\n"
        invoice += "="*44 + "\n"
        invoice += "       Thank you for shopping with us!       \n"
        invoice += "="*44 + "\n"
        return invoice

if __name__ == "__main__":
    root = Tk()
    obj = BillingClass(root)
    root.mainloop()
