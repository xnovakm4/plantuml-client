# Tech Stack

- **Language**: Python 3.10+
- **GUI Framework**: PyQt6
- **Architecture**: Separated UI (Views) and Core (Logic, Models, API)
- **Settings & Config**: JSON files `config.json`
- **Localization**: Python `gettext` or simple JSON dictionary files based on selected language. 

## Database / Config Migration

- Pri priprave nove verze aplikace, pro migraci databaze (tj. lokálního konfiguračního souboru v tomto případě) postupuj takto:
    1. Spusť migraci staré konfigurace v `config_manager.py`.
    2. Načti aktuálně uložený JSON s nastavením.
    3. Zkontroluj přítomnost nových klíčů a zadej jejich výchozí hodnoty.
    4. Odstraň klíče, které již nejsou podporovány.
    5. Ulož aktualizovaný JSON.
