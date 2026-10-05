from tkinter import *
from tkinter import ttk, messagebox
import sqlite3 as sq
import os

class CategoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Category Management System")
        self.root.config(bg="#f4f6f8")
        self.root.focus_force()

        # Variables
        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        # Title
        title = Label(self.root, text="Category Details", font=("Segoe UI", 20, "bold"), bg="#1f4e79", fg="white", pady=10)
        title.pack(fill=X)

        # Form
        Label(self.root, text="Enter Category Name", font=("Segoe UI", 12, "bold"), bg="#f4f6f8").place(x=50, y=100)
        Entry(self.root, textvariable=self.var_name, font=("Segoe UI", 12), bg="#fffde7", bd=2, relief=GROOVE).place(x=50, y=140, width=300, height=35)

        Button(self.root, text="Add", command=self.add, font=("Segoe UI", 12, "bold"), bg="#1976d2", fg="white", bd=0, cursor="hand2").place(x=50, y=190, width=140, height=35)
        Button(self.root, text="Delete", command=self.delete, font=("Segoe UI", 12, "bold"), bg="#e53935", fg="white", bd=0, cursor="hand2").place(x=210, y=190, width=140, height=35)

        # Category Table
        cat_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        cat_frame.place(x=500, y=100, width=550, height=350)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.category_table = ttk.Treeview(cat_frame, columns=("cid", "name"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.category_table.xview)
        scrolly.config(command=self.category_table.yview)

        self.category_table.heading("cid", text="Category ID")
        self.category_table.heading("name", text="Name")
        self.category_table["show"] = "headings"

        self.category_table.column("cid", width=100)
        self.category_table.column("name", width=200)
        self.category_table.pack(fill=BOTH, expand=1)
        self.category_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    #-------------------------------------------
    def add(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name is required", parent=self.root)
            else:
                cur.execute("INSERT INTO category (name) VALUES (?)", (self.var_name.get(),))
                con.commit()
                messagebox.showinfo("Success", "Category added successfully", parent=self.root)
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
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()
            self.category_table.delete(*self.category_table.get_children())
            for row in rows:
                self.category_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.category_table.focus()
        content = (self.category_table.item(f))
        row = content['values']
        if row:
            self.var_cat_id.set(row[0])
            self.var_name.set(row[1])

    def delete(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Select category from table", parent=self.root)
            else:
                op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                if op:
                    cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                    con.commit()
                    messagebox.showinfo("Deleted", "Category deleted successfully", parent=self.root)
                    self.show()
                    self.var_cat_id.set("")
                    self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = CategoryClass(root)
    root.mainloop()
