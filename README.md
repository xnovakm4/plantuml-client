# PlantUML Client

A cross-platform desktop application built with Python, PyQt6, and QThread architecture for editing, viewing, and rendering PlantUML diagrams.

## Key Features

- **Asynchronous Live Preview:** Fast, non-blocking rendering of PlantUML files utilizing background PyQt threads to keep the UI perfectly responsive.
- **Dual Rendering Modes:**
  - **Remote Server:** Render diagrams over the network using an external PlantUML API (with support for custom Server URLs and API Keys).
  - **Local PlantUML Engine:** Render diagrams securely offline using a local Java-based PlantUML process without needing a running web server.
- **Cross-Platform Smetana Engine:** The local rendering utilizes PlantUML's pure Java `Smetana` layout engine, entirely eliminating the complex need to install Graphviz natively on macOS/Windows/Linux.
- **Smart Dependency Management:** Automatically downloads the required `plantuml.jar` engine into a secure `~/.plantuml-client` system directory if it is not already present.
- **Multi-language Support:** Full i18n localization in English and Czech, seamlessly switchable in real-time.
- **Standalone Releases:** Ready-to-use compiled executables (Windows `.exe`, macOS `.app`, Linux binaries) are built automatically. 

## Downloading Binaries
You can download the pre-compiled standalone application for your operating system from the [GitHub Releases](https://github.com/xnovakm4/plantuml-client/releases) page.

## Running from Source

### Prerequisites
- Python 3.10+
- Java JRE installed and available in your system PATH (only if you want to use the Local Rendering feature).

### Setup

```bash
# Clone the repository
git clone https://github.com/xnovakm4/plantuml-client.git
cd plantuml-client

# Install dependencies 
pip install -r requirements.txt

# Run the app!
python main.py
```

## Compiling Your Own Executables
You can easily bundle the Python application into an offline `.exe` / `.app` using PyInstaller:

```bash
# Install bundler dependency
pip install pyinstaller

# Run the build script
python build.py
```
The compiled, ready-to-run output will be generated inside the `dist/` root directory.
