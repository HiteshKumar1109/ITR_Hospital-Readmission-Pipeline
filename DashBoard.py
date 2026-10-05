from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from Employee import EmployeeClass
from Supplier import SupplierClass
from Category import CategoryClass
from Product import ProductClass
from SalesAnalysis import SalesAnalysisClass
from time import strftime
import sqlite3 as sq
import os
from Billing import BillingClass
import db

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System and Sales Analysis")
        self.root.config(bg="#f4f6f8")

        # Re-initialize database with realistic 10 records on startup
        try:
            db.reinitialize_with_realistic_data(force=True)
        except Exception as ex:
            messagebox.showerror("Database Error", f"Failed to initialize database: {str(ex)}")

       
        try:
            img = Image.open("images/LOGO.png")
            img = img.resize((75, 75), Image.LANCZOS)
            self.icon_title = ImageTk.PhotoImage(img)
        except:
            self.icon_title = None

        # Title
        title = Label(
            self.root,
            text="Inventory Management System & Sales Analysis",
            image=self.icon_title,
            compound=LEFT,
            font=("Segoe UI", 30, "bold"),
            bg="#2C3E50",
            fg="white",
            anchor="w",
            padx=20
        )
        title.place(x=0, y=0, relwidth=1, height=80)
        

        # Clock
        self.lbl_clock = Label(
            self.root,
            text="Welcome To Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
            font=("Segoe UI", 12),
            bg="#34495E",
            fg="white",
        )
        self.lbl_clock.place(x=0, y=80, relwidth=1, height=35)
        
        # Left Menu Frame
        Leftmenu = Frame(self.root, bd=0, bg="#2C3E50")
        Leftmenu.place(x=0, y=115, width=250, height=750)

        # Sidebar Title
        lbl_menu = Label(Leftmenu, text="MENU", font=("Segoe UI", 18, "bold"), bg="#1ABC9C", fg="white")
        lbl_menu.pack(fill=X)

        # Menu Buttons
        self.create_menu_button(Leftmenu, " Dashboard", self.update_content, "dashboard.png")
        self.create_menu_button(Leftmenu, " Employee", self.open_employee, "teamwork.png")
        self.create_menu_button(Leftmenu, " Supplier", self.open_supplier, "supplier.png")
        self.create_menu_button(Leftmenu, " Category", self.open_category, "classification.png")
        self.create_menu_button(Leftmenu, " Products", self.open_product, "products.png")
        self.create_menu_button(Leftmenu, " Billing", self.open_billing, "sales.png")
        self.create_menu_button(Leftmenu, " Sales Analysis", self.open_sales, "sales.png")
        self.create_menu_button(Leftmenu, " Exit", self.root.quit, "exit.png")

        # Content
        self.lbl_employee = self.create_stat_card("Total Employees", "#1ABC9C", 300, 150)
        self.lbl_supplier = self.create_stat_card("Total Suppliers", "#E67E22", 650, 150)
        self.lbl_category = self.create_stat_card("Total Categories", "#9B59B6", 1000, 150)
        self.lbl_product = self.create_stat_card("Total Products", "#34495E", 300, 350)
        self.lbl_sales = self.create_stat_card("Total Sales Records", "#E74C3C", 650, 350)

        # Footer
        footer = Label(
            self.root,
            text=" Inventory Management System & Sales Analysis | Developed by: Hitesh Kumar | All Rights Reserved",
            font=("Segoe UI", 10),
            bg="#2C3E50",
            fg="white"
        )
        footer.pack(side=BOTTOM, fill=X)

        self.update_clock()
        self.update_content()
        self.auto_refresh_content()

    def create_menu_button(self, parent, text, command, icon_name):
        try:
            icon = Image.open(f"images/{icon_name}")
            icon = icon.resize((25, 25), Image.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon)
            # Use unique attribute names based on text to prevent reference overwriting
            ref_name = f"icon_{text.strip().replace(' ', '_').lower()}"
            setattr(self, ref_name, icon_photo) # Keep reference
        except:
            icon_photo = None

        btn = Button(
            parent,
            text=text,
            image=icon_photo if icon_photo else "",
            compound=LEFT,
            font=("Segoe UI", 14, "bold"),
            cursor="hand2",
            bg="#2C3E50",
            fg="white",
            bd=0,
            padx=20,
            anchor="w",
            command=command,
            activebackground="#34495E",
            activeforeground="#1ABC9C"
        )
        btn.pack(fill=X, pady=5)

    def create_stat_card(self, title, color, x, y):
        card = Label(self.root, text=f"{title}\n[ 0 ]", font=("Segoe UI", 20, "bold"), bg=color, fg="white", bd=5, relief=RIDGE)
        card.place(x=x, y=y, width=300, height=150)
        return card

    def update_clock(self):
        time_str = strftime("%I:%M:%S %p")
        date_str = strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome To Inventory Management System\t\t Date: {date_str}\t\t Time: {time_str}")
        self.lbl_clock.after(1000, self.update_clock)

    def auto_refresh_content(self):
        """Auto-refresh dashboard content every 2 seconds"""
        try:
            self._update_dashboard_stats(show_error=False)
        except Exception:
            pass  # Silently ignore errors during auto-refresh
        finally:
            # Schedule next refresh
            self.root.after(2000, self.auto_refresh_content)

    def update_content(self):
        """Manual refresh - shows errors"""
        self._update_dashboard_stats(show_error=True)

    def _update_dashboard_stats(self, show_error=False):
        """Internal method to update all dashboard statistics"""
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            self.lbl_employee.config(text=f"Total Employees\n[ {len(cur.fetchall())} ]")

            cur.execute("SELECT * FROM supplier")
            self.lbl_supplier.config(text=f"Total Suppliers\n[ {len(cur.fetchall())} ]")

            cur.execute("SELECT * FROM category")
            self.lbl_category.config(text=f"Total Categories\n[ {len(cur.fetchall())} ]")

            cur.execute("SELECT * FROM product")
            self.lbl_product.config(text=f"Total Products\n[ {len(cur.fetchall())} ]")

            cur.execute("SELECT * FROM sales")
            self.lbl_sales.config(text=f"Total Sales Records\n[ {len(cur.fetchall())} ]")

        except Exception as ex:
            if show_error:
                messagebox.showerror("Database Error", f"Failed to load dashboard data:\n{str(ex)}")
            print(f"Dashboard Refresh Error: {str(ex)}")
        finally:
            con.close()

    def open_employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = EmployeeClass(self.new_win)

    def open_supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SupplierClass(self.new_win)

    def open_category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CategoryClass(self.new_win)

    def open_product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ProductClass(self.new_win)

    def open_sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SalesAnalysisClass(self.new_win)

    def open_billing(self):
        try:
            self.new_win = Toplevel(self.root)
            self.new_obj = BillingClass(self.new_win)
        except Exception as ex:
            import traceback
            messagebox.showerror("Error", f"Failed to open Billing screen:\n{traceback.format_exc()}")

    def logout(self):
        self.root.destroy()
        

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
