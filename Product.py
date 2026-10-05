from tkinter import *
from tkinter import ttk, messagebox
import sqlite3 as sq
import os

class ProductClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Product Management System")
        self.root.config(bg="#f4f6f8")
        self.root.focus_force()

        # Variables
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.fetch_cat_sup()

        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.var_pid = StringVar()

        # Title
        title = Label(self.root, text="Product Details", font=("Segoe UI", 20, "bold"), bg="#1f4e79", fg="white", pady=10)
        title.pack(fill=X)

        # Left Form Frame
        form_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        form_frame.place(x=20, y=80, width=450, height=380)

        Label(form_frame, text="Category", font=("Segoe UI", 12, "bold"), bg="white").place(x=20, y=30)
        self.cmb_cat = ttk.Combobox(form_frame, textvariable=self.var_cat, values=self.cat_list, state='readonly', justify=CENTER, font=("Segoe UI", 12))
        self.cmb_cat.place(x=150, y=30, width=200)
        self.cmb_cat.set("Select")

        Label(form_frame, text="Supplier", font=("Segoe UI", 12, "bold"), bg="white").place(x=20, y=80)
        self.cmb_sup = ttk.Combobox(form_frame, textvariable=self.var_sup, values=self.sup_list, state='readonly', justify=CENTER, font=("Segoe UI", 12))
        self.cmb_sup.place(x=150, y=80, width=200)
        self.cmb_sup.set("Select")

        Label(form_frame, text="Product Name", font=("Segoe UI", 12, "bold"), bg="white").place(x=20, y=130)
        Entry(form_frame, textvariable=self.var_name, font=("Segoe UI", 12), bg="#f9f9f9", bd=2, relief=GROOVE).place(x=150, y=130, width=200)

        Label(form_frame, text="Price", font=("Segoe UI", 12, "bold"), bg="white").place(x=20, y=180)
        Entry(form_frame, textvariable=self.var_price, font=("Segoe UI", 12), bg="#f9f9f9", bd=2, relief=GROOVE).place(x=150, y=180, width=200)

        Label(form_frame, text="Quantity", font=("Segoe UI", 12, "bold"), bg="white").place(x=20, y=230)
        Entry(form_frame, textvariable=self.var_qty, font=("Segoe UI", 12), bg="#f9f9f9", bd=2, relief=GROOVE).place(x=150, y=230, width=200)

        Label(form_frame, text="Status", font=("Segoe UI", 12, "bold"), bg="white").place(x=20, y=280)
        self.cmb_status = ttk.Combobox(form_frame, textvariable=self.var_status, values=("Active", "Inactive"), state='readonly', justify=CENTER, font=("Segoe UI", 12))
        self.cmb_status.place(x=150, y=280, width=200)
        self.cmb_status.set("Active")

        # Buttons
        btn_frame = Frame(form_frame, bg="white")
        btn_frame.place(x=15, y=330, width=420, height=40)

        Button(btn_frame, text="Add", command=self.add, font=("Segoe UI", 12, "bold"), bg="#1976d2", fg="white", bd=0, cursor="hand2").place(x=0, y=0, width=100, height=35)
        Button(btn_frame, text="Update", command=self.update, font=("Segoe UI", 12, "bold"), bg="#fb8c00", fg="white", bd=0, cursor="hand2").place(x=110, y=0, width=100, height=35)
        Button(btn_frame, text="Delete", command=self.delete, font=("Segoe UI", 12, "bold"), bg="#e53935", fg="white", bd=0, cursor="hand2").place(x=220, y=0, width=100, height=35)
        Button(btn_frame, text="Clear", command=self.clear, font=("Segoe UI", 12, "bold"), bg="#546e7a", fg="white", bd=0, cursor="hand2").place(x=330, y=0, width=70, height=35)

        # Right Table Frame
        table_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        table_frame.place(x=490, y=80, width=590, height=380)

        # Search
        self.var_search_cat = StringVar()
        self.var_search_txt = StringVar()
        Label(table_frame, text="Search Product", font=("Segoe UI", 12, "bold"), bg="white").place(x=10, y=10)
        self.cmb_search = ttk.Combobox(table_frame, textvariable=self.var_search_cat, values=("Category", "Supplier", "Name"), state='readonly', justify=CENTER, font=("Segoe UI", 11))
        self.cmb_search.place(x=150, y=10, width=120)
        self.cmb_search.set("Select")

        Entry(table_frame, textvariable=self.var_search_txt, font=("Segoe UI", 11), bg="#f9f9f9", bd=2, relief=GROOVE).place(x=280, y=10, width=120)
        Button(table_frame, text="Search", command=self.search, font=("Segoe UI", 11, "bold"), bg="#1976d2", fg="white", bd=0, cursor="hand2").place(x=410, y=10, width=80, height=28)
        Button(table_frame, text="Show All", command=self.show, font=("Segoe UI", 11, "bold"), bg="#43a047", fg="white", bd=0, cursor="hand2").place(x=500, y=10, width=80, height=28)

        # Treeview
        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(table_frame, columns=("pid", "Category", "Supplier", "name", "price", "qty", "status"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="P ID")
        self.product_table.heading("Category", text="Category")
        self.product_table.heading("Supplier", text="Supplier")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Quantity")
        self.product_table.heading("status", text="Status")
        self.product_table["show"] = "headings"

        self.product_table.column("pid", width=50)
        self.product_table.column("Category", width=100)
        self.product_table.column("Supplier", width=100)
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=80)
        self.product_table.column("qty", width=80)
        self.product_table.column("status", width=80)
        self.product_table.pack(fill=BOTH, expand=1, pady=(50, 0))
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    #----------------------------------------------------------------------------------
    def fetch_cat_sup(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM category")
            rows_cat = cur.fetchall()
            self.cat_list.append("Select")
            for i in rows_cat:
                self.cat_list.append(i[0])

            cur.execute("SELECT name FROM supplier")
            rows_sup = cur.fetchall()
            self.sup_list.append("Select")
            for i in rows_sup:
                self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def add(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_sup.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("INSERT INTO product (Category, Supplier, name, price, qty, status) VALUES (?,?,?,?,?,?)", (
                    self.var_cat.get(),
                    self.var_sup.get(),
                    self.var_name.get(),
                    self.var_price.get(),
                    self.var_qty.get(),
                    self.var_status.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Product added successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.product_table.focus()
        content = (self.product_table.item(f))
        row = content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_cat.set(row[1])
            self.var_sup.set(row[2])
            self.var_name.set(row[3])
            self.var_price.set(row[4])
            self.var_qty.set(row[5])
            self.var_status.set(row[6])

    def update(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select product from list", parent=self.root)
            else:
                cur.execute("UPDATE product SET Category=?, Supplier=?, name=?, price=?, qty=?, status=? WHERE pid=?", (
                    self.var_cat.get(),
                    self.var_sup.get(),
                    self.var_name.get(),
                    self.var_price.get(),
                    self.var_qty.get(),
                    self.var_status.get(),
                    self.var_pid.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Product updated successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select product from list", parent=self.root)
            else:
                op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                if op:
                    cur.execute("DELETE FROM product WHERE pid=?", (self.var_pid.get(),))
                    con.commit()
                    messagebox.showinfo("Deleted", "Product deleted successfully", parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_search_txt.set("")
        self.var_search_cat.set("Select")
        self.show()

    def search(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            if self.var_search_cat.get() == "Select":
                messagebox.showerror("Error", "Select search option", parent=self.root)
            elif self.var_search_txt.get() == "":
                messagebox.showerror("Error", "Search input required", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE "+self.var_search_cat.get()+" LIKE ?", ('%' + self.var_search_txt.get() + '%',))
                rows = cur.fetchall()
                if len(rows) > 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showinfo("Result", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = ProductClass(root)
    root.mainloop()
