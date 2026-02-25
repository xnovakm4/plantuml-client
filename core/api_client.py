import os
import subprocess
import requests
from .plantuml_encoder import encode_plantuml
from .i18n import tr

class PlantUMLClient:
    def __init__(self, settings_manager):
        self.settings = settings_manager
        app_dir = os.path.expanduser("~/.plantuml-client")
        os.makedirs(app_dir, exist_ok=True)
        self.jar_path = os.path.join(app_dir, "plantuml.jar")

    def get_png(self, puml_text: str) -> bytes:
        """
        Retrieves PNG bytes. Acts as a router between remote and local rendering.
        """
        mode = self.settings.get("rendering_mode", "remote")
        if mode == "local":
            return self._render_local(puml_text)
        else:
            return self._render_remote(puml_text)
            
    def _render_remote(self, puml_text: str) -> bytes:
        encoded = encode_plantuml(puml_text)
        server_url = self.settings.get("server_url", "")
        api_key = self.settings.get("api_key", "")
        
        if not server_url:
            raise ValueError("Server URL is not configured.")
        
        url = f"{server_url.rstrip('/')}/png/{encoded}"
        headers = {}
        if api_key:
            headers["X-API-Key"] = api_key
            
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException:
            raise RuntimeError(tr("remote_render_failed"))

    def _render_local(self, puml_text: str) -> bytes:
        import tempfile
        # Check if java is installed
        try:
            subprocess.run(["java", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            raise RuntimeError(tr("java_install_instructions"))

        # Check if plantuml.jar exists, download if not
        if not os.path.exists(self.jar_path):
            self._download_plantuml()

        fd, puml_path = tempfile.mkstemp(suffix=".puml")
        png_path = puml_path.replace(".puml", ".png")
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(puml_text)

            # Run plantuml with Smetana layout engine to generate the file
            process = subprocess.run(
                ["java", "-jar", self.jar_path, "-Playout=smetana", puml_path],
                capture_output=True,
                check=True
            )
            
            if not os.path.exists(png_path):
                err_msg = process.stderr.decode('utf-8', errors='replace') if process.stderr else "PlantUML failed to generate PNG."
                raise RuntimeError(err_msg)
                
            with open(png_path, "rb") as f:
                png_bytes = f.read()
                
            return png_bytes
            
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.decode('utf-8', errors='replace') if e.stderr else str(e)
            raise RuntimeError(err_msg)
        finally:
            if os.path.exists(puml_path):
                os.remove(puml_path)
            if os.path.exists(png_path):
                os.remove(png_path)

    def _download_plantuml(self):
        url = "https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(self.jar_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        else:
            raise RuntimeError(tr("plantuml_download_error"))
