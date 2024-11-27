import sqlite3
from datetime import datetime
import random
import sys
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
import click
from typing import Optional

console = Console()

class SQLiteDemo:
    def __init__(self, db_name="demo.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        self.cursor.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price DECIMAL(10,2),
            in_stock BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS product_search
        USING FTS5(name, description);
        """)
        self.conn.commit()

    def demo_basic_operations(self):
        """Demonstrate basic CRUD operations"""
        with console.status("[bold green]Performing basic CRUD operations..."):
            # Create a table for displaying results
            table = Table(title="Basic CRUD Operations")
            table.add_column("Operation", style="cyan")
            table.add_column("Result", style="green")

            # INSERT
            self.cursor.execute("""
            INSERT INTO products (name, price, in_stock)
            VALUES (?, ?, ?)
            """, ("Laptop", 999.99, True))
            table.add_row("INSERT", f"Product inserted with ID: {self.cursor.lastrowid}")

            # SELECT
            self.cursor.execute("SELECT * FROM products WHERE price > ?", (500,))
            results = self.cursor.fetchall()
            table.add_row("SELECT", f"Found {len(results)} products over $500")

            # UPDATE
            self.cursor.execute("""
            UPDATE products
            SET price = price * 1.1
            WHERE price > ?
            """, (500,))
            table.add_row("UPDATE", f"Updated {self.cursor.rowcount} products")

            # DELETE
            self.cursor.execute("DELETE FROM products WHERE in_stock = ?", (False,))
            table.add_row("DELETE", f"Deleted {self.cursor.rowcount} products")

            self.conn.commit()
            console.print(table)

    def demo_transactions(self):
        """Demonstrate transaction handling"""
        with console.status("[bold green]Testing transaction handling..."):
            try:
                self.cursor.execute("BEGIN TRANSACTION")

                self.cursor.execute("""
                INSERT INTO products (name, price, in_stock)
                VALUES (?, ?, ?)
                """, ("Test Product", 50.00, True))
                product_id = self.cursor.lastrowid

                self.cursor.execute("""
                INSERT INTO orders (product_id, quantity)
                VALUES (?, ?)
                """, (product_id, 5))

                if random.random() < 0.5:
                    raise Exception("Simulated random transaction error")

                self.cursor.execute("COMMIT")
                rprint("[green]Transaction completed successfully[/green]")

            except Exception as e:
                self.cursor.execute("ROLLBACK")
                rprint(f"[red]Transaction rolled back: {e}[/red]")

    def demo_full_text_search(self):
        """Demonstrate full-text search capabilities"""
        with console.status("[bold green]Setting up full-text search demo..."):
            sample_products = [
                ("Gaming Laptop", "High-performance gaming laptop with RGB keyboard"),
                ("Business Laptop", "Professional laptop for office work"),
                ("Student Notebook", "Affordable laptop for students")
            ]

            self.cursor.executemany("""
            INSERT INTO product_search (name, description)
            VALUES (?, ?)
            """, sample_products)

            search_term = "laptop"
            self.cursor.execute("""
            SELECT * FROM product_search
            WHERE product_search MATCH ?
            ORDER BY rank
            """, (search_term,))

            table = Table(title=f"Search Results for '{search_term}'")
            table.add_column("Name", style="cyan")
            table.add_column("Description", style="green")

            for row in self.cursor.fetchall():
                table.add_row(row[0], row[1])

            console.print(table)

    def demo_aggregate_functions(self):
        """Demonstrate aggregate functions and GROUP BY"""
        with console.status("[bold green]Calculating aggregates..."):
            self.cursor.execute("""
            SELECT
                strftime('%Y-%m', order_date) as month,
                COUNT(*) as order_count,
                SUM(quantity) as total_items,
                AVG(quantity) as avg_items
            FROM orders
            GROUP BY month
            HAVING order_count > 0
            ORDER BY month DESC
            """)

            table = Table(title="Monthly Order Statistics")
            table.add_column("Month", style="cyan")
            table.add_column("Order Count", style="green")
            table.add_column("Total Items", style="blue")
            table.add_column("Avg Items", style="magenta")

            for row in self.cursor.fetchall():
                table.add_row(*[str(x) for x in row])

            console.print(table)

    def run_all_demos(self):
        """Run all demonstration methods"""
        rprint("\n[bold blue]Running All Demos[/bold blue]")
        self.demo_basic_operations()
        self.demo_transactions()
        self.demo_full_text_search()
        self.demo_aggregate_functions()

    def drop_database(self):
        """Drop the database file"""
        self.conn.close()
        try:
            os.remove(self.db_name)
            rprint(f"[green]Database {self.db_name} has been dropped successfully.[/green]")
        except Exception as e:
            rprint(f"[red]Error dropping database: {e}[/red]")

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """SQLite Demo Application"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(interactive)

@cli.command()
def interactive():
    """Start interactive demo mode"""
    demo = SQLiteDemo()
    while True:
        console.print(Panel.fit(
            "[bold blue]SQLite Demo Menu[/bold blue]\n\n"
            "1. Basic CRUD Operations\n"
            "2. Transaction Handling\n"
            "3. Full-Text Search\n"
            "4. Aggregate Functions\n"
            "5. Run All Demos\n"
            "6. Drop Database\n"
            "Q. Quit",
            title="Menu",
            border_style="blue"
        ))

        choice = click.prompt("Enter your choice", type=str).strip().upper()

        if choice == '1':
            demo.demo_basic_operations()
        elif choice == '2':
            demo.demo_transactions()
        elif choice == '3':
            demo.demo_full_text_search()
        elif choice == '4':
            demo.demo_aggregate_functions()
        elif choice == '5':
            demo.run_all_demos()
        elif choice == '6':
            if click.confirm("Are you sure you want to drop the database?"):
                demo.drop_database()
                sys.exit()
        elif choice == 'Q':
            rprint("[yellow]Exiting SQLite Demo...[/yellow]")
            sys.exit()
        else:
            rprint("[red]Invalid choice. Please try again.[/red]")

@cli.command()
def crud():
    """Run basic CRUD operations demo"""
    demo = SQLiteDemo()
    demo.demo_basic_operations()

@cli.command()
def transactions():
    """Run transaction handling demo"""
    demo = SQLiteDemo()
    demo.demo_transactions()

@cli.command()
def search():
    """Run full-text search demo"""
    demo = SQLiteDemo()
    demo.demo_full_text_search()

@cli.command()
def aggregates():
    """Run aggregate functions demo"""
    demo = SQLiteDemo()
    demo.demo_aggregate_functions()

@cli.command()
def all():
    """Run all demos"""
    demo = SQLiteDemo()
    demo.run_all_demos()

if __name__ == "__main__":
    cli()
