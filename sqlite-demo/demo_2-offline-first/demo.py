import sqlite3
import json
import uuid
import time
from datetime import datetime
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import click
from typing import Optional
import queue
import threading
import random

console = Console()

class OfflineFirstDemo:
    def __init__(self, db_name="edge.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.sync_queue = queue.Queue()
        self.setup_database()
        self.sync_thread = None
        self.is_online = False
        self.sync_running = False

    def setup_database(self):
        """Initialize the database schema with sync tracking"""
        self.cursor.executescript("""
        -- Transactions table with sync status
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            amount DECIMAL(10,2),
            description TEXT,
            synced INTEGER DEFAULT 0,
            sync_timestamp DATETIME,
            retry_count INTEGER DEFAULT 0
        );

        -- Sync log for debugging and monitoring
        CREATE TABLE IF NOT EXISTS sync_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            event_type TEXT,
            details TEXT
        );
        
        -- Local configuration
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()

    def log_sync_event(self, event_type: str, details: str):
        """Record sync-related events"""
        self.cursor.execute("""
        INSERT INTO sync_log (event_type, details)
        VALUES (?, ?)
        """, (event_type, details))
        self.conn.commit()

    def record_transaction(self, amount: float, description: str):
        """Record a new transaction locally"""
        transaction_id = str(uuid.uuid4())
        try:
            self.cursor.execute("""
            INSERT INTO transactions (id, amount, description)
            VALUES (?, ?, ?)
            """, (transaction_id, amount, description))
            self.conn.commit()
            
            self.sync_queue.put(transaction_id)
            console.print(f"[green]Transaction recorded locally: {transaction_id}[/green]")
            
            # Try immediate sync if online
            if self.is_online:
                self.sync_pending_transactions()
                
        except Exception as e:
            console.print(f"[red]Error recording transaction: {e}[/red]")

    def simulate_server_sync(self, transaction_id: str) -> bool:
        """Simulate syncing with a remote server"""
        # Simulate network latency
        time.sleep(random.uniform(0.1, 0.5))
        
        # Simulate occasional network failures
        if random.random() < 0.2:  # 20% chance of failure
            return False
            
        return True

    def sync_pending_transactions(self):
        """Sync pending transactions to the server"""
        if not self.is_online:
            console.print("[yellow]Device is offline. Transactions will sync when connection is restored.[/yellow]")
            return

        self.cursor.execute("""
        SELECT id, amount, description 
        FROM transactions 
        WHERE synced = 0 AND retry_count < 3
        ORDER BY timestamp
        """)
        
        pending = self.cursor.fetchall()
        
        if not pending:
            console.print("[green]No pending transactions to sync[/green]")
            return

        for transaction in pending:
            transaction_id, amount, description = transaction
            
            try:
                # Attempt to sync with simulated server
                sync_success = self.simulate_server_sync(transaction_id)
                
                if sync_success:
                    self.cursor.execute("""
                    UPDATE transactions 
                    SET synced = 1, sync_timestamp = CURRENT_TIMESTAMP 
                    WHERE id = ?
                    """, (transaction_id,))
                    self.log_sync_event("sync_success", f"Transaction {transaction_id} synced successfully")
                    console.print(f"[green]Synced transaction: {transaction_id}[/green]")
                else:
                    self.cursor.execute("""
                    UPDATE transactions 
                    SET retry_count = retry_count + 1 
                    WHERE id = ?
                    """, (transaction_id,))
                    self.log_sync_event("sync_failure", f"Failed to sync transaction {transaction_id}")
                    console.print(f"[red]Failed to sync transaction: {transaction_id}[/red]")
                
                self.conn.commit()
                
            except Exception as e:
                self.log_sync_event("sync_error", f"Error syncing {transaction_id}: {str(e)}")
                console.print(f"[red]Error syncing transaction {transaction_id}: {e}[/red]")

    def start_sync_worker(self):
        """Start background sync worker"""
        self.sync_running = True
        
        def worker():
            while self.sync_running:
                if self.is_online:
                    self.sync_pending_transactions()
                time.sleep(5)  # Check every 5 seconds
        
        self.sync_thread = threading.Thread(target=worker, daemon=True)
        self.sync_thread.start()

    def stop_sync_worker(self):
        """Stop background sync worker"""
        self.sync_running = False
        if self.sync_thread:
            self.sync_thread.join()

    def toggle_connection(self):
        """Toggle online/offline status"""
        self.is_online = not self.is_online
        status = "ONLINE" if self.is_online else "OFFLINE"
        console.print(f"[bold {'green' if self.is_online else 'red'}]Device is now {status}[/bold]")
        
        if self.is_online:
            self.sync_pending_transactions()

    def show_sync_status(self):
        """Display sync status information"""
        self.cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN synced = 1 THEN 1 ELSE 0 END) as synced,
            SUM(CASE WHEN synced = 0 AND retry_count < 3 THEN 1 ELSE 0 END) as pending,
            SUM(CASE WHEN retry_count >= 3 THEN 1 ELSE 0 END) as failed
        FROM transactions
        """)
        
        stats = self.cursor.fetchone()
        
        table = Table(title="Sync Status")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="green")
        
        table.add_row("Total Transactions", str(stats[0]))
        table.add_row("Synced", str(stats[1]))
        table.add_row("Pending", str(stats[2]))
        table.add_row("Failed", str(stats[3]))
        
        console.print(table)

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Offline-First SQLite Demo"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(interactive)

@cli.command()
def interactive():
    """Start interactive demo mode"""
    demo = OfflineFirstDemo()
    demo.start_sync_worker()

    while True:
        console.print(Panel.fit(
            "[bold blue]Offline-First Demo Menu[/bold blue]\n\n"
            "1. Record New Transaction\n"
            "2. Toggle Online/Offline\n"
            "3. Force Sync Attempt\n"
            "4. Show Sync Status\n"
            "5. View Sync Log\n"
            "Q. Quit",
            title="Menu",
            border_style="blue"
        ))

        choice = click.prompt("Enter your choice", type=str).strip().upper()

        if choice == '1':
            amount = click.prompt("Enter amount", type=float)
            description = click.prompt("Enter description", type=str)
            demo.record_transaction(amount, description)
        elif choice == '2':
            demo.toggle_connection()
        elif choice == '3':
            demo.sync_pending_transactions()
        elif choice == '4':
            demo.show_sync_status()
        elif choice == '5':
            demo.cursor.execute("""
            SELECT timestamp, event_type, details 
            FROM sync_log 
            ORDER BY timestamp DESC 
            LIMIT 10
            """)
            table = Table(title="Recent Sync Events")
            table.add_column("Timestamp", style="cyan")
            table.add_column("Event", style="green")
            table.add_column("Details", style="white")
            
            for row in demo.cursor.fetchall():
                table.add_row(str(row[0]), row[1], row[2])
            
            console.print(table)
        elif choice == 'Q':
            demo.stop_sync_worker()
            console.print("[yellow]Exiting demo...[/yellow]")
            break
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")

if __name__ == "__main__":
    cli()