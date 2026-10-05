from tkinter import *
from tkinter import ttk, messagebox
import sqlite3 as sq
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SalesAnalysisClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x600+220+130")
        self.root.title("Sales Analysis Dashboard")
        self.root.config(bg="#f4f6f8")
        self.root.focus_force()

        # Title
        title = Label(self.root, text="Sales Analysis Dashboard", font=("Segoe UI", 24, "bold"), bg="#2c3e50", fg="white", pady=10)
        title.pack(fill=X)

        # Left Control Frame
        control_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        control_frame.place(x=10, y=80, width=300, height=500)

        Label(control_frame, text="View Charts", font=("Segoe UI", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=20)

        btn_sales_by_date = Button(control_frame, text="Sales by Date", command=self.plot_sales_by_date, font=("Segoe UI", 12, "bold"), bg="#3498db", fg="white", cursor="hand2", bd=0)
        btn_sales_by_date.pack(fill=X, padx=20, pady=10, ipady=5)

        btn_top_products = Button(control_frame, text="Top Products", command=self.plot_top_products, font=("Segoe UI", 12, "bold"), bg="#e67e22", fg="white", cursor="hand2", bd=0)
        btn_top_products.pack(fill=X, padx=20, pady=10, ipady=5)
        
        btn_combined = Button(control_frame, text="Full Dashboard", command=self.plot_combined, font=("Segoe UI", 12, "bold"), bg="#9b59b6", fg="white", cursor="hand2", bd=0)
        btn_combined.pack(fill=X, padx=20, pady=10, ipady=5)
        
        btn_show_data = Button(control_frame, text="Show All Data", command=self.show_sales_table, font=("Segoe UI", 12, "bold"), bg="#27ae60", fg="white", cursor="hand2", bd=0)
        btn_show_data.pack(fill=X, padx=20, pady=10, ipady=5)

        # Right Chart Frame
        self.chart_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        self.chart_frame.place(x=320, y=80, width=760, height=500)
        
        self.placeholder_label = Label(self.chart_frame, text="Select an analysis from the left", font=("Segoe UI", 16), bg="white", fg="grey")
        self.placeholder_label.pack(expand=True)

    def fetch_data(self):
        db_path = os.path.abspath("company.db")
        con = sq.connect(database=db_path)
        df = pd.read_sql_query("SELECT * FROM sales", con)
        con.close()
        return df

    def clear_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

    def plot_sales_by_date(self):
        self.clear_chart()
        try:
            df = self.fetch_data()
            if df.empty:
                messagebox.showinfo("No Data", "No sales records found.")
                return
            
            df['date'] = pd.to_datetime(df['date'])
            sales_by_date = df.groupby('date')['total'].sum().reset_index()
            sales_by_date = sales_by_date.sort_values('date')

            fig, ax = plt.subplots(figsize=(7, 4.2))
            ax.plot(sales_by_date['date'], sales_by_date['total'], marker='o', linewidth=2, color='#1f77b4', markerfacecolor='#2c3e50')
            ax.fill_between(sales_by_date['date'], sales_by_date['total'], color='#1f77b4', alpha=0.1)
            ax.set_title("Total Sales Trend Over Time", fontsize=12, fontweight='bold', pad=15, color='#2c3e50')
            ax.set_xlabel("Date", fontsize=10, labelpad=8)
            ax.set_ylabel("Total Revenue ($)", fontsize=10, labelpad=8)
            ax.grid(True, linestyle=':', alpha=0.6, color='#ccc')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#ddd')
            ax.spines['bottom'].set_color('#ddd')
            plt.xticks(rotation=30)
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=10)
        except Exception as ex:
            messagebox.showerror("Error", f"Could not generate chart: {str(ex)}")

    def plot_top_products(self):
        self.clear_chart()
        try:
            df = self.fetch_data()
            if df.empty:
                messagebox.showinfo("No Data", "No sales records found.")
                return
            
            top_products = df.groupby('product_name')['qty'].sum().sort_values(ascending=False).head(5)

            fig, ax = plt.subplots(figsize=(7, 4.2))
            colors = ['#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e']
            top_products.plot(kind='bar', color=colors[:len(top_products)], ax=ax, width=0.5)
            ax.set_title("Top 5 Best Selling Products (Quantity)", fontsize=12, fontweight='bold', pad=15, color='#2c3e50')
            ax.set_xlabel("Product Name", fontsize=10, labelpad=8)
            ax.set_ylabel("Total Quantity Sold", fontsize=10, labelpad=8)
            ax.grid(True, axis='y', linestyle=':', alpha=0.6, color='#ccc')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#ddd')
            ax.spines['bottom'].set_color('#ddd')
            plt.xticks(rotation=30)
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=10)
        except Exception as ex:
            messagebox.showerror("Error", f"Could not generate chart: {str(ex)}")

    def show_sales_table(self):
        self.clear_chart()
        try:
            df = self.fetch_data()
            if df.empty:
                messagebox.showinfo("No Data", "No sales records found.")
                return

            # Styled Table Header and Fields
            scrolly = Scrollbar(self.chart_frame, orient=VERTICAL)
            scrollx = Scrollbar(self.chart_frame, orient=HORIZONTAL)

            table = ttk.Treeview(self.chart_frame, columns=list(df.columns), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
            scrollx.pack(side=BOTTOM, fill=X)
            scrolly.pack(side=RIGHT, fill=Y)
            scrollx.config(command=table.xview)
            scrolly.config(command=table.yview)

            for col in df.columns:
                table.heading(col, text=col)
                table.column(col, width=100, anchor=CENTER)
            
            table["show"] = "headings"
            
            for index, row in df.iterrows():
                table.insert('', END, values=list(row))
            
            table.pack(fill=BOTH, expand=1, padx=10, pady=10)
        except Exception as ex:
            messagebox.showerror("Error", f"Could not display table: {str(ex)}")

    def plot_combined(self):
        self.clear_chart()
        try:
            df = self.fetch_data()
            if df.empty:
                messagebox.showinfo("No Data", "No sales records found.")
                return

            # 1. Calculate KPI Metrics
            total_sales = df['total'].sum()
            total_orders = df['invoice'].nunique()
            units_sold = df['qty'].sum()

            # 2. Render KPI cards at the top
            kpi_frame = Frame(self.chart_frame, bg="white")
            kpi_frame.pack(fill=X, pady=(15, 5))

            # Card 1: Total Revenue
            c1 = Frame(kpi_frame, bg="#ebf5fb", bd=1, relief=GROOVE)
            c1.pack(side=LEFT, padx=15, expand=True, fill=X)
            Label(c1, text="TOTAL REVENUE", font=("Segoe UI", 9, "bold"), bg="#ebf5fb", fg="#2980b9").pack(pady=(5, 0))
            Label(c1, text=f"${total_sales:,.2f}", font=("Segoe UI", 16, "bold"), bg="#ebf5fb", fg="#2c3e50").pack(pady=(0, 5))

            # Card 2: Total Orders
            c2 = Frame(kpi_frame, bg="#eafaf1", bd=1, relief=GROOVE)
            c2.pack(side=LEFT, padx=15, expand=True, fill=X)
            Label(c2, text="TOTAL TRANSACTIONS", font=("Segoe UI", 9, "bold"), bg="#eafaf1", fg="#27ae60").pack(pady=(5, 0))
            Label(c2, text=f"{total_orders}", font=("Segoe UI", 16, "bold"), bg="#eafaf1", fg="#2c3e50").pack(pady=(0, 5))

            # Card 3: Items Sold
            c3 = Frame(kpi_frame, bg="#fef9e7", bd=1, relief=GROOVE)
            c3.pack(side=LEFT, padx=15, expand=True, fill=X)
            Label(c3, text="ITEMS SOLD", font=("Segoe UI", 9, "bold"), bg="#fef9e7", fg="#f39c12").pack(pady=(5, 0))
            Label(c3, text=f"{units_sold}", font=("Segoe UI", 16, "bold"), bg="#fef9e7", fg="#2c3e50").pack(pady=(0, 5))

            # 3. Create matplotlib figure with side-by-side subplots (1 row, 2 columns)
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.5))
            
            # Subplot 1: Sales by Date (Line Area Chart)
            df['date'] = pd.to_datetime(df['date'])
            sales_by_date = df.groupby('date')['total'].sum().reset_index()
            sales_by_date = sales_by_date.sort_values('date')

            ax1.plot(sales_by_date['date'], sales_by_date['total'], marker='o', linewidth=2, color='#2980b9', markerfacecolor='#2c3e50')
            ax1.fill_between(sales_by_date['date'], sales_by_date['total'], color='#2980b9', alpha=0.1)
            ax1.set_title("Revenue Over Time", fontsize=10, fontweight='bold', pad=10, color='#2c3e50')
            ax1.grid(True, linestyle=':', alpha=0.6, color='#ccc')
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['left'].set_color('#ddd')
            ax1.spines['bottom'].set_color('#ddd')
            ax1.tick_params(axis='x', rotation=25, labelsize=8)
            ax1.tick_params(axis='y', labelsize=8)

            # Subplot 2: Top Products (Multi-color Bar Chart)
            top_products = df.groupby('product_name')['qty'].sum().sort_values(ascending=False).head(5)
            colors = ['#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e']
            top_products.plot(kind='bar', color=colors[:len(top_products)], ax=ax2, width=0.55)
            ax2.set_title("Top 5 Products sold (Qty)", fontsize=10, fontweight='bold', pad=10, color='#2c3e50')
            ax2.grid(True, axis='y', linestyle=':', alpha=0.6, color='#ccc')
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.spines['left'].set_color('#ddd')
            ax2.spines['bottom'].set_color('#ddd')
            ax2.tick_params(axis='x', rotation=25, labelsize=8)
            ax2.tick_params(axis='y', labelsize=8)

            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=(5, 10))
            
        except Exception as ex:
            messagebox.showerror("Error", f"Could not generate combined charts: {str(ex)}")

if __name__ == "__main__":
    root = Tk()
    obj = SalesAnalysisClass(root)
    root.mainloop()
