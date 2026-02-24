# Build script for PyInstaller
import PyInstaller.__main__
import os

if __name__ == '__main__':
    PyInstaller.__main__.run([
        'main.py',
        '--name=PlantUML-Client',
        '--windowed',  # Prevent console window from appearing
        '--noconfirm', # Overwrite existing output directory
        '--clean',     # Clean PyInstaller cache
        '--add-data=core:core', # Include the core module/translations
        '--add-data=ui:ui',     # Include UI modules
        # Note: plantuml.jar is intentionally NOT bundled since the app auto-downloads it into its current working directory (or app support dir)
    ])
