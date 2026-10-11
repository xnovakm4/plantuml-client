# Build script for PyInstaller
import PyInstaller.__main__
import os

if __name__ == '__main__':
    sep = os.pathsep
    PyInstaller.__main__.run([
        'main.py',
        '--name=PlantUML-Client',
        '--windowed',  # Prevent console window from appearing
        '--onefile',   # Package into a single executable file
        '--noconfirm', # Overwrite existing output directory
        '--clean',     # Clean PyInstaller cache
        f'--add-data=core{sep}core', # Include the core module/translations
        f'--add-data=ui{sep}ui',     # Include UI modules
        # Note: plantuml.jar is intentionally NOT bundled since the app auto-downloads it into its current working directory (or app support dir)
    ])
