# Ubuntu Mirrors Refresher

## Overview

The **Ubuntu Mirrors Refresher** is a Python script that retrieves and checks the status of up-to-date Ubuntu mirror servers. It fetches mirror URLs from the Ubuntu Launchpad, tests their availability, and measures ping times, helping users find the best mirrors based on performance.

## Features

- **Fetches Up-to-Date Mirrors**: Automatically retrieves a list of mirrors from the [Ubuntu Launchpad](https://launchpad.net/ubuntu/+archivemirrors).
- **Concurrent Requests**: Utilizes asynchronous programming to efficiently handle multiple requests to mirror servers simultaneously.
- **Ping Time Measurement**: Records the response time for each mirror, enabling users to identify the fastest options.
- **Logging**: Detailed logging of the fetching process and results for easier debugging and analysis.

## Requirements

- Python 3.7 or higher
- `aiohttp` library
- `beautifulsoup4` library
- `requests` library

You can install the required libraries using pip:

```bash
pip install aiohttp beautifulsoup4 requests
```

## Usage

1. **Clone the repository**:

   ```bash
   git clone https://github.com/AmirBuddy/Ubuntu-Mirrors-Refresher.git
   cd Ubuntu-Mirrors-Refresher
   ```

2. **Run the script**:

   ```bash
   python main.py
   ```

3. **Output**: The script will log the top 10 up-to-date Ubuntu mirrors along with their HTTP status and ping times.

## Logging

The script uses the `logging` module to log various events and errors. The log level is set to `INFO` by default. You can modify the log level in the code to change the verbosity of the output.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, feel free to open an issue or submit a pull request.
