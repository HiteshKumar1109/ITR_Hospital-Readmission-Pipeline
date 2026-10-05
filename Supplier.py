from tkinter import *
from tkinter import ttk, messagebox
import sqlite3 as sq
import os

class SupplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Supplier Management System")
        self.root.config(bg="#f4f6f8")
        self.root.focus_force()

        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        title = Label(self.root, text="Supplier Details", font=("Segoe UI", 20, "bold"), bg="#1f4e79", fg="white", pady=10)
        title.pack(fill=X)

        # left menu
        form_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        form_frame.place(x=20, y=80, width=400, height=380)

        Label(form_frame, text="Invoice No.", font=("Segoe UI", 12, "bold"), bg="white").place(x=20, y=30)
        Entry(form_frame, textvariable=self.var_sup_invoice, font=("Segoe UI", 12), bg="#f9f9f9", bd=2, relief=GROOVE).place(x=150, y=30, width=200)

        Label(form_frame, text="Supplier Name", font=("Segoe UI", 12, "bold"), bg="white").place(x=20, y=80)
        Entry(form_frame, textvariable=self.var_name, font=("Segoe UI", 12), bg="#f9f9f9", bd=2, relief=GROOVE).place(x=150, y=80, width=200)

        Label(form_frame, text="Contact No.", font=("Segoe UI", 12, "bold"), bg="white").place(x=20, y=130)
        Entry(form_frame, textvariable=self.var_contact, font=("Segoe UI", 12), bg="#f9f9f9", bd=2, relief=GROOVE).place(x=150, y=130, width=200)

        Label(form_frame, text="Description", font=("Segoe UI", 12, "bold"), bg="white").place(x=20, y=180)
        self.txt_desc = Text(form_frame, font=("Segoe UI", 11), bg="#f9f9f9", bd=2, relief=GROOVE)
        self.txt_desc.place(x=150, y=180, width=200, height=100)

        # Buttons
        btn_frame = Frame(form_frame, bg="white")
        btn_frame.place(x=15, y=310, width=370, height=40)

        Button(btn_frame, text="Add", command=self.add, font=("Segoe UI", 12, "bold"), bg="#1976d2", fg="white", bd=0, cursor="hand2").place(x=0, y=0, width=80, height=35)
        Button(btn_frame, text="Update", command=self.update, font=("Segoe UI", 12, "bold"), bg="#fb8c00", fg="white", bd=0, cursor="hand2").place(x=90, y=0, width=80, height=35)
        Button(btn_frame, text="Delete", command=self.delete, font=("Segoe UI", 12, "bold"), bg="#e53935", fg="white", bd=0, cursor="hand2").place(x=180, y=0, width=80, height=35)
        Button(btn_frame, text="Clear", command=self.clear, font=("Segoe UI", 12, "bold"), bg="#546e7a", fg="white", bd=0, cursor="hand2").place(x=270, y=0, width=80, height=35)

        # Right Table Frame
        table_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        table_frame.place(x=440, y=80, width=640, height=380)

        # Search
        self.var_search = StringVar()
        Label(table_frame, text="Search by Invoice No.", font=("Segoe UI", 12, "bold"), bg="white").place(x=10, y=10)
        Entry(table_frame, textvariable=self.var_search, font=("Segoe UI", 12), bg="#f9f9f9", bd=2, relief=GROOVE).place(x=190, y=10, width=200)
        Button(table_frame, text="Search", command=self.search, font=("Segoe UI", 11, "bold"), bg="#1976d2", fg="white", bd=0, cursor="hand2").place(x=400, y=10, width=100, height=30)
        Button(table_frame, text="Show All", command=self.show, font=("Segoe UI", 11, "bold"), bg="#43a047", fg="white", bd=0, cursor="hand2").place(x=510, y=10, width=100, height=30)

        # Treeview
        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)

        self.supplier_table = ttk.Treeview(table_frame, columns=("invoice", "name", "contact", "desc"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplier_table.xview)
        scrolly.config(command=self.supplier_table.yview)

        self.supplier_table.heading("invoice", text="Invoice No.")
        self.supplier_table.heading("name", text="Name")
        self.supplier_table.heading("contact", text="Contact")
        self.supplier_table.heading("desc", text="Description")
        self.supplier_table["show"] = "headings"

        self.supplier_table.column("invoice", width=90)
        self.supplier_table.column("name", width=100)
        self.supplier_table.column("contact", width=100)
        self.supplier_table.column("desc", width=200)
        self.supplier_table.pack(fill=BOTH, expand=1, pady=(50, 0))
        self.supplier_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    
    def add(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Invoice No. already assigned", parent=self.root)
                else:
                    cur.execute("INSERT INTO supplier (invoice, name, contact, desc) VALUES (?,?,?,?)", (
                        self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END)
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier added successfully", parent=self.root)
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
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()
            self.supplier_table.delete(*self.supplier_table.get_children())
            for row in rows:
                self.supplier_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.supplier_table.focus()
        content = (self.supplier_table.item(f))
        row = content['values']
        if row:
            self.var_sup_invoice.set(row[0])
            self.var_name.set(row[1])
            self.var_contact.set(row[2])
            self.txt_desc.delete('1.0', END)
            self.txt_desc.insert(END, row[3])

    def update(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    cur.execute("UPDATE supplier SET name=?, contact=?, desc=? WHERE invoice=?", (
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END),
                        self.var_sup_invoice.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier updated successfully", parent=self.root)
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
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Deleted", "Supplier deleted successfully", parent=self.root)
                        self.clear()
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.var_search.set("")
        self.show()

    def search(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search input required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_search.get(),))
                row = cur.fetchone()
                if row is not None:
                    self.supplier_table.delete(*self.supplier_table.get_children())
                    self.supplier_table.insert('', END, values=row)
                else:
                    messagebox.showinfo("Result", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = SupplierClass(root)
    root.mainloop()
