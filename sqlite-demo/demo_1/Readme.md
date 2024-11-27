# SQLite Features Demo Application

An interactive demonstration of SQLite's key features and capabilities. This application showcases various SQLite functionalities through practical examples and an interactive CLI interface.

## Features

- **Basic CRUD Operations**
  - Create, Read, Update, Delete operations
  - Different data types demonstration
  - Primary and foreign key relationships

- **Transaction Handling**
  - BEGIN, COMMIT, ROLLBACK demonstration
  - Error handling and recovery
  - Transaction isolation

- **Full-Text Search**
  - FTS5 virtual table implementation
  - Advanced text search capabilities
  - Search result ranking

- **Advanced SQL Features**
  - Aggregate functions (COUNT, SUM, AVG)
  - GROUP BY and HAVING clauses
  - Date/time functions
  - Multi-table relationships

## Installation

1. Set up Python environment:
```bash
# Install pyenv (if not already installed)
# macOS:
brew install pyenv

# Ubuntu/Debian:
curl https://pyenv.run | bash

# Configure pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

# Install Python version
pyenv install 3.11.5
pyenv local 3.11.5
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the demo in different modes:

```bash
# Interactive mode (default)
python demo.py

# Direct command mode
python demo.py crud         # Run CRUD demo
python demo.py transactions # Run transactions demo
python demo.py search      # Run full-text search demo
python demo.py aggregates  # Run aggregate functions demo
python demo.py all         # Run all demos

# Show help
python demo.py --help
```

### Interactive Menu Options

1. **Basic CRUD Operations**
   - Demonstrates basic database operations
   - Shows different data types
   - Displays results in formatted tables

2. **Transaction Handling**
   - Shows transaction isolation
   - Demonstrates rollback on errors
   - Simulates real-world scenarios

3. **Full-Text Search**
   - Demonstrates FTS5 capabilities
   - Shows search result ranking
   - Example of complex text queries

4. **Aggregate Functions**
   - Shows GROUP BY usage
   - Demonstrates SQL aggregations
   - Example of data analysis

5. **Run All Demos**
   - Executes all demonstrations
   - Complete feature showcase

6. **Drop Database**
   - Removes the database file
   - Fresh start capability

### Database Schema

```sql
-- Products table
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    in_stock BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    quantity INTEGER,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Full-text search virtual table
CREATE VIRTUAL TABLE product_search 
USING FTS5(name, description);
```

## Features In Detail

### 1. CRUD Operations
- Table creation with various data types
- Primary key auto-increment
- Foreign key relationships
- Timestamp defaults
- Boolean fields

### 2. Transaction Management
- Transaction boundaries
- Error handling
- Rollback scenarios
- Data consistency

### 3. Full-Text Search
- FTS5 virtual tables
- Search result ranking
- Complex search queries
- Text indexing

### 4. Aggregations
- GROUP BY operations
- Having clauses
- Date/time functions
- Statistical calculations

## Use Cases

This demo is particularly useful for:

- **Learning SQLite**
  - Feature exploration
  - Hands-on practice
  - Understanding capabilities

- **Development Reference**
  - Code examples
  - Best practices
  - Implementation patterns

- **Teaching/Presentation**
  - Live demonstrations
  - Interactive learning
  - Feature showcasing

## CLI Features

The application uses:
- `click` for command-line interface
- `rich` for beautiful terminal output
- Colored text output
- Formatted tables
- Progress indicators
- Interactive menus

## Contributing

Contributions are welcome! Feel free to submit issues and enhancement requests.

## License

MIT License - feel free to use this demo code in your own projects.
