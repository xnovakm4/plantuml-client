TRANSLATIONS = {
    "EN": {
        "app_title": "PlantUML Client",
        "open_folder": "Open Folder",
        "settings": "Settings",
        "render": "Render",
        "save_image": "Save Image",
        "language": "Language",
        "server_url": "Server URL:",
        "api_key": "API Key:",
        "save": "Save",
        "cancel": "Cancel",
        "error": "Error",
        "file_saved": "File saved successfully",
        "image_saved_to": "Image saved to:",
        "no_file_selected": "No file selected",
        "select_folder": "Select Folder",
        "settings_saved": "Settings saved.",
        "rendering": "Rendering...",
        "language_changed": "Language has been changed.",
        "file_load_error": "Cannot load file content.",
        "render_error": "Failed to render diagram.",
        "success": "Success",
        "info": "Information",
        "save_file": "Save File",
        "save_changes_prompt": "You have unsaved changes. Do you want to save them?",
        "zoom_in": "Zoom In",
        "zoom_out": "Zoom Out",
        "zoom_actual": "Actual Size (1:1)",
        "zoom_fit": "Fit to Window",
        "rendering_mode": "Rendering Mode:",
        "remote_server": "Remote Server",
        "local_plantuml": "Local PlantUML",
        "java_not_found": "Java Not Found",
        "java_install_instructions": "Java is required for local rendering. Please install it from https://adoptium.net/ and restart the application.",
        "downloading_plantuml": "Downloading PlantUML...",
        "plantuml_download_error": "Failed to download plantuml.jar.",
        "plantuml_download_success": "plantuml.jar downloaded successfully."
    },
    "CS": {
        "app_title": "PlantUML Klient",
        "open_folder": "Otevřít složku",
        "settings": "Nastavení",
        "render": "Vykreslit",
        "save_image": "Uložit obrázek",
        "language": "Jazyk",
        "server_url": "URL Serveru:",
        "api_key": "API Klíč:",
        "save": "Uložit",
        "cancel": "Zrušit",
        "error": "Chyba",
        "file_saved": "Soubor úspěšně uložen",
        "image_saved_to": "Obrázek uložen do:",
        "no_file_selected": "Nebyl vybrán žádný soubor",
        "select_folder": "Vyberte složku",
        "settings_saved": "Nastavení bylo uloženo.",
        "rendering": "Vykresluji...",
        "language_changed": "Jazyk byl změněn.",
        "file_load_error": "Nelze načíst obsah souboru.",
        "render_error": "Nepodařilo se vykreslit diagram.",
        "success": "Úspěch",
        "info": "Informace",
        "save_file": "Uložit soubor",
        "save_changes_prompt": "Máte neuložené změny. Chcete je uložit?",
        "zoom_in": "Přiblížit",
        "zoom_out": "Oddálit",
        "zoom_actual": "Původní velikost (1:1)",
        "zoom_fit": "Přizpůsobit oknu",
        "rendering_mode": "Režim vykreslování:",
        "remote_server": "Vzdálený server",
        "local_plantuml": "Lokální PlantUML",
        "java_not_found": "Java nenalezena",
        "java_install_instructions": "Pro lokální vykreslování je vyžadována Java. Nainstalujte ji prosím z https://adoptium.net/ a restartujte aplikaci.",
        "downloading_plantuml": "Stahuji PlantUML...",
        "plantuml_download_error": "Nepodařilo se stáhnout plantuml.jar.",
        "plantuml_download_success": "plantuml.jar byl úspěšně stažen."
    }
}

class I18n:
    _current_lang = "EN"

    @classmethod
    def set_language(cls, lang: str):
        if lang in TRANSLATIONS:
            cls._current_lang = lang

    @classmethod
    def get(cls, key: str) -> str:
        return TRANSLATIONS.get(cls._current_lang, TRANSLATIONS["EN"]).get(key, key)

    @classmethod
    def get_supported_languages(cls) -> list[str]:
        return list(TRANSLATIONS.keys())

def tr(key: str) -> str:
    return I18n.get(key)
