<div align="center">
 <h1>Schedule I Stats Display</h1>
</div>
Schedule I Stats Display is a Python-based application that displays save game statistics for the game "Schedule I". It uses PyWebView for the GUI and integrates with the Steam API to fetch account and game-related data.

## Features

- Fetch and display save game statistics.
- Integrates with the Steam API to retrieve account and game information.
- Interactive GUI built with PyWebView.
- Supports multiple Steam accounts and save folders.

## Requirements
 - [.NET Framework 4.7.2>](https://dotnet.microsoft.com/en-us/download/dotnet-framework)
 - [WebView2](developer.microsoft.com/en-us/microsoft-edge/webview2#download)

The following Python packages are required to run the application:
- `requests`
- `pywebview`
- `QtPy`
- `cefpython3`
- `nuitka`
- `wheel`
- `setuptools`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SquashyHydra/Schedule-I-Stats-Display.git
   cd Schedule-I-Stats-Display
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your Steam API key:
   - Obtain your Steam API key from [Steam API Key](https://steamcommunity.com/dev/apikey).
   - Enter the key when prompted by the application.

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Follow the on-screen instructions to:
   - Select a Steam account.
   - Choose a save folder.
   - View detailed game statistics.

## images
<div align="center">
 <img src="https://i.imgur.com/nM0ETK1.png" alt="Account Selection" width="700">
 <img src="https://i.imgur.com/MEiC16F.png" alt="Save Selection" width="700">
 <img src="https://i.imgur.com/X3xdF2j.png" alt="Display Data" width="700">
</div>

## Compiling

For detailed compiling instructions, visit the [Wiki](https://github.com/SquashyHydra/Schedule-I-Stats/wiki/Compiling-to-windows-executable).

## Setting Up a Python Environment

For detailed enviroment setup instructions, visit the [Wiki](https://github.com/SquashyHydra/Schedule-I-Stats/wiki/Setting-Up-a-Python-Environment).

## Development

### File Structure

- `app.py`: Main entry point for the application.
- `Save.py`: Handles save game data fetching and processing.
- `Steam.py`: Integrates with the Steam API.
- `frontend/`: Contains HTML, CSS, and JavaScript files for the GUI.

### Frontend Files

- `accounts.html`: Displays Steam accounts.
- `loading.html`: Allows users to select save folders.
- `stats.html`: Displays detailed save game statistics.
- `style.css`: Styles for the frontend.
- `scripts.js`, `loading.js`, `stats.js`: JavaScript files for interactivity.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the GNU License. See the `LICENSE` file for details.
