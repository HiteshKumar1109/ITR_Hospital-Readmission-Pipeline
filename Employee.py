from tkinter import *
from tkinter import ttk, messagebox
import sqlite3 as sq
import os


class EmployeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720+100+50")
        self.root.title("Employee Management System")
        self.root.config(bg="#f4f6f8")
        self.root.resizable(False, False)

        self.create_db()

        # Title
        title = Label(
            self.root,
            text="Employee Management System",
            font=("Segoe UI", 24, "bold"),
            bg="#1f4e79",
            fg="white",
            pady=12
        )
        title.pack(fill=X)

        # Search Frame
        search_frame = LabelFrame(
            self.root,
            text="Search Employee",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#1f4e79",
            bd=2,
            relief=RIDGE
        )
        search_frame.place(x=300, y=80, width=700, height=80)

        self.cmb_search = ttk.Combobox(
            search_frame,
            values=("Select", "ID", "Name", "Email", "Contact", "Department", "Designation"),
            font=("Segoe UI", 12),
            state="readonly",
            justify=CENTER
        )
        self.cmb_search.place(x=20, y=10, width=160, height=32)
        self.cmb_search.current(0)

        self.txt_search = Entry(
            search_frame,
            font=("Segoe UI", 12),
            bg="#fffde7",
            bd=2,
            relief=GROOVE
        )
        self.txt_search.place(x=200, y=10, width=240, height=32)

        btn_search = Button(
            search_frame,
            text="Search",
            font=("Segoe UI", 11, "bold"),
            bg="#1976d2",
            fg="white",
            cursor="hand2",
            bd=0,
            command=self.search
        )
        btn_search.place(x=470, y=10, width=90, height=32)

        btn_show = Button(
            search_frame,
            text="Show All",
            font=("Segoe UI", 11, "bold"),
            bg="#43a047",
            fg="white",
            cursor="hand2",
            bd=0,
            command=self.show
        )
        btn_show.place(x=570, y=10, width=100, height=32)

        # Main Frame
        main_frame = Frame(self.root, bg="#f4f6f8")
        main_frame.place(x=20, y=170, width=1240, height=520)

        # Left Form Frame
        form_frame = Frame(main_frame, bg="white", bd=3, relief=RIDGE)
        form_frame.place(x=0, y=0, width=430, height=520)

        form_title = Label(
            form_frame,
            text="Employee Details",
            font=("Segoe UI", 18, "bold"),
            bg="#2e7d32",
            fg="white",
            pady=10
        )
        form_title.pack(fill=X)

        # Labels and Entries
        Label(form_frame, text="Employee ID", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").place(x=20, y=60)
        self.txt_emp_id = Entry(form_frame, font=("Segoe UI", 11), bg="#f9f9f9", bd=2, relief=GROOVE)
        self.txt_emp_id.place(x=150, y=60, width=250)

        Label(form_frame, text="Name", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").place(x=20, y=95)
        self.txt_name = Entry(form_frame, font=("Segoe UI", 11), bg="#f9f9f9", bd=2, relief=GROOVE)
        self.txt_name.place(x=150, y=95, width=250)

        Label(form_frame, text="Email", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").place(x=20, y=130)
        self.txt_email = Entry(form_frame, font=("Segoe UI", 11), bg="#f9f9f9", bd=2, relief=GROOVE)
        self.txt_email.place(x=150, y=130, width=250)

        Label(form_frame, text="Gender", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").place(x=20, y=165)
        self.cmb_gender = ttk.Combobox(
            form_frame,
            values=("Select", "Male", "Female", "Other"),
            font=("Segoe UI", 11),
            state="readonly",
            justify=CENTER
        )
        self.cmb_gender.place(x=150, y=165, width=250, height=28)
        self.cmb_gender.current(0)

        Label(form_frame, text="Contact", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").place(x=20, y=200)
        self.txt_contact = Entry(form_frame, font=("Segoe UI", 11), bg="#f9f9f9", bd=2, relief=GROOVE)
        self.txt_contact.place(x=150, y=200, width=250)

        Label(form_frame, text="D.O.B", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").place(x=20, y=235)
        self.txt_dob = Entry(form_frame, font=("Segoe UI", 11), bg="#f9f9f9", bd=2, relief=GROOVE)
        self.txt_dob.place(x=150, y=235, width=250)

        Label(form_frame, text="Joining Date", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").place(x=20, y=270)
        self.txt_join = Entry(form_frame, font=("Segoe UI", 11), bg="#f9f9f9", bd=2, relief=GROOVE)
        self.txt_join.place(x=150, y=270, width=250)

        Label(form_frame, text="Salary", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").place(x=20, y=305)
        self.txt_salary = Entry(form_frame, font=("Segoe UI", 11), bg="#f9f9f9", bd=2, relief=GROOVE)
        self.txt_salary.place(x=150, y=305, width=250)

        Label(form_frame, text="Education", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").place(x=20, y=340)
        self.txt_education = Entry(form_frame, font=("Segoe UI", 11), bg="#f9f9f9", bd=2, relief=GROOVE)
        self.txt_education.place(x=150, y=340, width=250)

        Label(form_frame, text="Department", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").place(x=20, y=375)
        self.txt_department = Entry(form_frame, font=("Segoe UI", 11), bg="#f9f9f9", bd=2, relief=GROOVE)
        self.txt_department.place(x=150, y=375, width=250)

        Label(form_frame, text="Designation", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").place(x=20, y=410)
        self.txt_designation = Entry(form_frame, font=("Segoe UI", 11), bg="#f9f9f9", bd=2, relief=GROOVE)
        self.txt_designation.place(x=150, y=410, width=250)

        Label(form_frame, text="Address", font=("Segoe UI", 11, "bold"), bg="white", fg="#333").place(x=20, y=445)
        self.txt_address = Entry(form_frame, font=("Segoe UI", 11), bg="#f9f9f9", bd=2, relief=GROOVE)
        self.txt_address.place(x=150, y=445, width=250)

        # Buttons
        btn_frame = Frame(form_frame, bg="white")
        btn_frame.place(x=15, y=480, width=400, height=35)

        Button(btn_frame, text="Add", font=("Segoe UI", 11, "bold"), bg="#1976d2", fg="white", bd=0, cursor="hand2", command=self.Add).place(x=0, y=0, width=90, height=32)
        Button(btn_frame, text="Update", font=("Segoe UI", 11, "bold"), bg="#fb8c00", fg="white", bd=0, cursor="hand2", command=self.update).place(x=100, y=0, width=90, height=32)
        Button(btn_frame, text="Delete", font=("Segoe UI", 11, "bold"), bg="#e53935", fg="white", bd=0, cursor="hand2", command=self.delete).place(x=200, y=0, width=90, height=32)
        Button(btn_frame, text="Clear", font=("Segoe UI", 11, "bold"), bg="#546e7a", fg="white", bd=0, cursor="hand2", command=self.clear).place(x=300, y=0, width=90, height=32)

        # Right Table Frame
        table_frame = Frame(main_frame, bg="white", bd=3, relief=RIDGE)
        table_frame.place(x=450, y=0, width=790, height=520)

        table_title = Label(
            table_frame,
            text="Employee DATA",
            font=("Segoe UI", 18, "bold"),
            bg="#6a1b9a",
            fg="white",
            pady=10
        )
        table_title.pack(fill=X)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="white",
            foreground="#333333",
            rowheight=28,
            fieldbackground="white",
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#3949ab",
            foreground="white"
        )
        style.map("Treeview", background=[("selected", "#90caf9")])

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.employee_table = ttk.Treeview(
            table_frame,
            columns=("eid", "name", "email", "gender", "contact", "dob", "join_date", "salary", "education", "department", "designation", "address"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.employee_table.xview)
        scroll_y.config(command=self.employee_table.yview)

        self.employee_table.heading("eid", text="Emp ID")
        self.employee_table.heading("name", text="Name")
        self.employee_table.heading("email", text="Email")
        self.employee_table.heading("gender", text="Gender")
        self.employee_table.heading("contact", text="Contact")
        self.employee_table.heading("dob", text="D.O.B")
        self.employee_table.heading("join_date", text="Joining Date")
        self.employee_table.heading("salary", text="Salary")
        self.employee_table.heading("education", text="Education")
        self.employee_table.heading("department", text="Department")
        self.employee_table.heading("designation", text="Designation")
        self.employee_table.heading("address", text="Address")

        self.employee_table["show"] = "headings"

        self.employee_table.column("eid", width=80)
        self.employee_table.column("name", width=120)
        self.employee_table.column("email", width=170)
        self.employee_table.column("gender", width=90)
        self.employee_table.column("contact", width=110)
        self.employee_table.column("dob", width=100)
        self.employee_table.column("join_date", width=120)
        self.employee_table.column("salary", width=100)
        self.employee_table.column("education", width=130)
        self.employee_table.column("department", width=130)
        self.employee_table.column("designation", width=130)
        self.employee_table.column("address", width=180)

        self.employee_table.pack(fill=BOTH, expand=1)
        self.employee_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def create_db(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employee(
                eid TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                gender TEXT,
                contact TEXT,
                dob TEXT,
                join_date TEXT,
                salary TEXT,
                education TEXT,
                department TEXT,
                designation TEXT,
                address TEXT
            )
        """)
        con.commit()
        con.close()

    def Add(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            if self.txt_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            elif self.txt_name.get() == "":
                messagebox.showerror("Error", "Employee Name must be required", parent=self.root)
            elif self.txt_email.get() == "":
                messagebox.showerror("Error", "Employee Email must be required", parent=self.root)
            elif self.cmb_gender.get() == "Select":
                messagebox.showerror("Error", "Employee Gender must be required", parent=self.root)
            elif self.txt_contact.get() == "":
                messagebox.showerror("Error", "Employee Contact must be required", parent=self.root)
            elif self.txt_dob.get() == "":
                messagebox.showerror("Error", "Employee D.O.B must be required", parent=self.root)
            elif self.txt_join.get() == "":
                messagebox.showerror("Error", "Employee Joining Date must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.txt_emp_id.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Employee ID already assigned, try different", parent=self.root)
                else:
                    cur.execute("""
                        INSERT INTO employee
                        (eid, name, email, gender, contact, dob, join_date, salary, education, department, designation, address)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        self.txt_emp_id.get(),
                        self.txt_name.get(),
                        self.txt_email.get(),
                        self.cmb_gender.get(),
                        self.txt_contact.get(),
                        self.txt_dob.get(),
                        self.txt_join.get(),
                        self.txt_salary.get(),
                        self.txt_education.get(),
                        self.txt_department.get(),
                        self.txt_designation.get(),
                        self.txt_address.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee added successfully", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            self.employee_table.delete(*self.employee_table.get_children())
            for row in rows:
                self.employee_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.employee_table.focus()
        content = self.employee_table.item(f)
        row = content["values"]
        if row:
            self.txt_emp_id.delete(0, END)
            self.txt_emp_id.insert(0, row[0])

            self.txt_name.delete(0, END)
            self.txt_name.insert(0, row[1])

            self.txt_email.delete(0, END)
            self.txt_email.insert(0, row[2])

            self.cmb_gender.set(row[3])

            self.txt_contact.delete(0, END)
            self.txt_contact.insert(0, row[4])

            self.txt_dob.delete(0, END)
            self.txt_dob.insert(0, row[5])

            self.txt_join.delete(0, END)
            self.txt_join.insert(0, row[6])

            self.txt_salary.delete(0, END)
            self.txt_salary.insert(0, row[7])

            self.txt_education.delete(0, END)
            self.txt_education.insert(0, row[8])

            self.txt_department.delete(0, END)
            self.txt_department.insert(0, row[9])

            self.txt_designation.delete(0, END)
            self.txt_designation.insert(0, row[10])

            self.txt_address.delete(0, END)
            self.txt_address.insert(0, row[11])

    def update(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            if self.txt_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID is required", parent=self.root)
            else:
                cur.execute("""
                    UPDATE employee SET
                        name=?,
                        email=?,
                        gender=?,
                        contact=?,
                        dob=?,
                        join_date=?,
                        salary=?,
                        education=?,
                        department=?,
                        designation=?,
                        address=?
                    WHERE eid=?
                """, (
                    self.txt_name.get(),
                    self.txt_email.get(),
                    self.cmb_gender.get(),
                    self.txt_contact.get(),
                    self.txt_dob.get(),
                    self.txt_join.get(),
                    self.txt_salary.get(),
                    self.txt_education.get(),
                    self.txt_department.get(),
                    self.txt_designation.get(),
                    self.txt_address.get(),
                    self.txt_emp_id.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Employee updated successfully", parent=self.root)
                self.show()
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            if self.txt_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID is required", parent=self.root)
            else:
                op = messagebox.askyesno("Confirm", "Do you really want to delete this employee?", parent=self.root)
                if op:
                    cur.execute("DELETE FROM employee WHERE eid=?", (self.txt_emp_id.get(),))
                    con.commit()
                    messagebox.showinfo("Deleted", "Employee deleted successfully", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.txt_emp_id.delete(0, END)
        self.txt_name.delete(0, END)
        self.txt_email.delete(0, END)
        self.cmb_gender.current(0)
        self.txt_contact.delete(0, END)
        self.txt_dob.delete(0, END)
        self.txt_join.delete(0, END)
        self.txt_salary.delete(0, END)
        self.txt_education.delete(0, END)
        self.txt_department.delete(0, END)
        self.txt_designation.delete(0, END)
        self.txt_address.delete(0, END)
        self.txt_search.delete(0, END)
        self.cmb_search.current(0)

    def search(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        cur = con.cursor()
        try:
            if self.cmb_search.get() == "Select":
                messagebox.showerror("Error", "Select search option", parent=self.root)
                return
            if self.txt_search.get() == "":
                messagebox.showerror("Error", "Search input required", parent=self.root)
                return

            col_map = {
                "ID": "eid",
                "Name": "name",
                "Email": "email",
                "Contact": "contact",
                "Department": "department",
                "Designation": "designation"
            }

            col_name = col_map.get(self.cmb_search.get())
            query = f"SELECT * FROM employee WHERE {col_name} LIKE ?"
            cur.execute(query, ('%' + self.txt_search.get() + '%',))
            rows = cur.fetchall()

            self.employee_table.delete(*self.employee_table.get_children())
            for row in rows:
                self.employee_table.insert('', END, values=row)

            if len(rows) == 0:
                messagebox.showinfo("Result", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = EmployeeClass(root)
    root.mainloop()