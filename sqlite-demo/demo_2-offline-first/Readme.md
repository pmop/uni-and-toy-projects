# SQLite Edge Computing Demo

This demo showcases how to build offline-first applications using SQLite for edge computing scenarios. It demonstrates resilient data handling with intermittent network connectivity, a common requirement in edge computing, IoT devices, and mobile applications.

## Features

- **Offline-First Operation**
  - Local-first data storage with SQLite
  - Automatic background synchronization
  - Resilient to network interruptions
  - Transaction queuing and retry mechanisms

- **Sync Management**
  - Background sync worker
  - Configurable retry attempts
  - Comprehensive sync logging
  - Real-time sync status monitoring

- **Interactive Demo Interface**
  - Record transactions
  - Toggle online/offline status
  - Force sync attempts
  - View sync statistics and logs

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

Run the demo:
```bash
python offline_demo.py
```

### Demo Menu Options

1. **Record New Transaction**
   - Add a new transaction to local storage
   - Will be synced when online

2. **Toggle Online/Offline**
   - Simulate network connectivity changes
   - Triggers automatic sync when going online

3. **Force Sync Attempt**
   - Manually trigger synchronization
   - Useful for testing sync behavior

4. **Show Sync Status**
   - View current sync statistics
   - Monitor pending transactions

5. **View Sync Log**
   - Check recent sync events
   - Debug sync issues

### Database Schema

The demo uses three main tables:

```sql
-- Transactions table
CREATE TABLE transactions (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10,2),
    description TEXT,
    synced INTEGER DEFAULT 0,
    sync_timestamp DATETIME,
    retry_count INTEGER DEFAULT 0
);

-- Sync log
CREATE TABLE sync_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT,
    details TEXT
);

-- Local configuration
CREATE TABLE config (
    key TEXT PRIMARY KEY,
    value TEXT,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Use Cases

This demo is particularly useful for:

- **IoT Devices**
  - Sensor data collection
  - Intermittent connectivity handling
  - Local data buffering

- **Mobile Applications**
  - Offline-first operations
  - Background sync
  - Data persistence

- **Edge Computing**
  - Local data processing
  - Resilient operations
  - Sync management

- **Field Operations**
  - Remote data collection
  - Disconnected operations
  - Data integrity maintenance

## Best Practices Demonstrated

1. **Data Integrity**
   - Unique transaction IDs
   - Sync status tracking
   - Retry mechanisms

2. **Error Handling**
   - Failed sync retry
   - Comprehensive logging
   - Status monitoring

3. **Performance**
   - Asynchronous sync
   - Background processing
   - Queue-based operations

4. **User Experience**
   - Immediate local storage
   - Real-time status updates
   - Interactive interface

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this demo code in your own projects.