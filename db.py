import sqlite3
import os

def create_db():
    # Use absolute path for database
    db_path = os.path.abspath("company.db")
    con = sqlite3.connect(database=db_path)
    cur = con.cursor()
    
    # Employee Table
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
    
    # Supplier Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS supplier(
            invoice TEXT PRIMARY KEY,
            name TEXT,
            contact TEXT,
            desc TEXT
        )
    """)
    
    # Category Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS category(
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)
    
    # Product Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS product(
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            Category TEXT,
            Supplier TEXT,
            name TEXT,
            price TEXT,
            qty TEXT,
            status TEXT
        )
    """)

    # Sales Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales(
            sid INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice TEXT,
            date TEXT,
            product_name TEXT,
            price REAL,
            qty INTEGER,
            total REAL
        )
    """)
    
    # Billing Table (NEW - to store invoice/billing records)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS billing(
            bid INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice TEXT UNIQUE,
            customer_name TEXT,
            customer_contact TEXT,
            bill_date TEXT,
            bill_time TEXT,
            subtotal REAL,
            tax REAL,
            total_amount REAL,
            status TEXT
        )
    """)
    
    con.commit()
    con.close()

def reinitialize_with_realistic_data(force=False):
    create_db()
    # Use absolute path for database
    db_path = os.path.abspath("company.db")
    con = sqlite3.connect(database=db_path)
    cur = con.cursor()
    
    # Check if we need to migrate (if old dummy data exists)
    needs_init = force
    if not force:
        try:
            cur.execute("SELECT COUNT(*) FROM product WHERE name='Product 1'")
            if cur.fetchone()[0] > 0:
                needs_init = True
            cur.execute("SELECT COUNT(*) FROM employee WHERE name='Employee 1'")
            if cur.fetchone()[0] > 0:
                needs_init = True
            
            # Also check if database is empty
            cur.execute("SELECT COUNT(*) FROM product")
            if cur.fetchone()[0] == 0:
                needs_init = True
        except Exception:
            needs_init = True
            
    if needs_init:
        # Drop tables to clear schema mismatches
        cur.execute("DROP TABLE IF EXISTS employee")
        cur.execute("DROP TABLE IF EXISTS supplier")
        cur.execute("DROP TABLE IF EXISTS category")
        cur.execute("DROP TABLE IF EXISTS product")
        cur.execute("DROP TABLE IF EXISTS sales")
        cur.execute("DROP TABLE IF EXISTS billing")
        con.commit()
        
        # Recreate tables
        con.close()
        create_db()
        db_path = os.path.abspath("company.db")
        con = sqlite3.connect(database=db_path)
        cur = con.cursor()
        
        # 1. Categories (10)
        categories = [
            ("Electronics",),
            ("Office Supplies",),
            ("Furniture",),
            ("Apparel",),
            ("Food & Beverages",),
            ("Cosmetics",),
            ("Home Appliances",),
            ("Sports Equipment",),
            ("Toys & Games",),
            ("Automotive Accessories",)
        ]
        cur.executemany("INSERT INTO category (name) VALUES (?)", categories)
        
        # 2. Suppliers (10)
        suppliers = [
            ("INV-101", "TechDistributors Ltd.", "9876543101", "Electronics and gadgets distributor"),
            ("INV-102", "Global Paper Co.", "9876543102", "Stationery and paper supplies manufacturer"),
            ("INV-103", "Comfort Office Furniture", "9876543103", "Ergonomic chairs, desks and storage units"),
            ("INV-104", "StyleWear Clothing", "9876543104", "Casual apparel and staff uniforms"),
            ("INV-105", "Refreshment Hub Inc.", "9876543105", "Organic tea, coffee and snacks"),
            ("INV-106", "GlowBeauty Organics", "9876543106", "Organic cosmetics and skin care products"),
            ("INV-107", "HomeComfort Appliances", "9876543107", "Kitchen and home electrical appliances"),
            ("INV-108", "ActiveSports Gear", "9876543108", "Professional sports equipment and sportswear"),
            ("INV-109", "FunTime Toys", "9876543109", "Educational toys and games for children"),
            ("INV-110", "AutoParts Express", "9876543110", "Car accessories and maintenance spares")
        ]
        cur.executemany("INSERT INTO supplier VALUES (?,?,?,?)", suppliers)
        
        # 3. Products (10)
        products = [
            ("Electronics", "TechDistributors Ltd.", "Laptop Dell XPS", "75000", "15", "Active"),
            ("Electronics", "TechDistributors Ltd.", "Wireless Mouse Logitech", "1500", "50", "Active"),
            ("Office Supplies", "Global Paper Co.", "A4 Paper Rim", "350", "100", "Active"),
            ("Furniture", "Comfort Office Furniture", "Ergonomic Office Chair", "8500", "20", "Active"),
            ("Apparel", "StyleWear Clothing", "Cotton T-Shirt Blue", "600", "40", "Active"),
            ("Food & Beverages", "Refreshment Hub Inc.", "Organic Green Tea", "250", "60", "Active"),
            ("Cosmetics", "GlowBeauty Organics", "Aloe Vera Face Wash", "180", "35", "Active"),
            ("Home Appliances", "HomeComfort Appliances", "Electric Kettle", "2200", "25", "Active"),
            ("Sports Equipment", "ActiveSports Gear", "Leather Football", "1200", "30", "Active"),
            ("Automotive Accessories", "AutoParts Express", "LED Headlight Bulb", "950", "15", "Active")
        ]
        cur.executemany("INSERT INTO product (Category, Supplier, name, price, qty, status) VALUES (?,?,?,?,?,?)", products)
        
        # 4. Employees (10)
        employees = [
            ("EMP001", "John Doe", "john.doe@gmail.com", "Male", "9876543001", "1992-05-15", "2021-06-01", "45000", "MBA", "HR", "Manager", "New Delhi"),
            ("EMP002", "Jane Smith", "jane.smith@gmail.com", "Female", "9876543002", "1995-08-22", "2022-01-15", "60000", "B.Tech", "IT", "Software Engineer", "Noida"),
            ("EMP003", "David Lee", "david.lee@gmail.com", "Male", "9876543003", "1988-11-05", "2020-03-10", "55000", "B.Com", "Accounts", "Senior Accountant", "Gurgaon"),
            ("EMP004", "Emily Davis", "emily.davis@gmail.com", "Female", "9876543004", "1993-02-18", "2023-07-01", "40000", "B.Sc", "Sales", "Executive", "Delhi"),
            ("EMP005", "Michael Brown", "michael.brown@gmail.com", "Male", "9876543005", "1990-09-30", "2019-11-12", "70000", "MBA", "Operations", "Operations Head", "Faridabad"),
            ("EMP006", "Sarah Wilson", "sarah.wilson@gmail.com", "Female", "9876543006", "1996-04-12", "2024-02-01", "35000", "BBA", "Support", "Customer Support", "Ghaziabad"),
            ("EMP007", "James Taylor", "james.taylor@gmail.com", "Male", "9876543007", "1991-12-25", "2022-09-15", "50000", "M.Tech", "QA", "Test Engineer", "Noida"),
            ("EMP008", "Jessica Garcia", "jessica.garcia@gmail.com", "Female", "9876543008", "1994-07-08", "2021-10-20", "48000", "B.Des", "Marketing", "Designer", "Delhi"),
            ("EMP009", "Robert Martinez", "robert.martinez@gmail.com", "Male", "9876543009", "1987-03-14", "2018-05-01", "90000", "MBA", "Management", "General Manager", "New Delhi"),
            ("EMP010", "Mary Rodriguez", "mary.rodriguez@gmail.com", "Female", "9876543010", "1997-10-02", "2023-11-01", "32000", "B.Com", "Sales", "Assistant", "Gurgaon")
        ]
        cur.executemany("INSERT INTO employee VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", employees)
        
        # 5. Sales (5 realistic sales records)
        sales = [
            ("INV-20260610", "2026-06-10", "Laptop Dell XPS", 75000.0, 1, 75000.0),
            ("INV-20260612", "2026-06-12", "Wireless Mouse Logitech", 1500.0, 2, 3000.0),
            ("INV-20260614", "2026-06-14", "Ergonomic Office Chair", 8500.0, 1, 8500.0),
            ("INV-20260615", "2026-06-15", "A4 Paper Rim", 350.0, 5, 1750.0),
            ("INV-20260616", "2026-06-16", "Cotton T-Shirt Blue", 600.0, 3, 1800.0)
        ]
        cur.executemany("INSERT INTO sales (invoice, date, product_name, price, qty, total) VALUES (?,?,?,?,?,?)", sales)
        
        con.commit()
    con.close()

if __name__ == "__main__":
    reinitialize_with_realistic_data(force=True)
    print("Database fully re-initialized with 10 realistic records for each table!")