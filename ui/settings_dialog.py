from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox)
from core.i18n import tr, I18n

class SettingsDialog(QDialog):
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings = settings_manager
        self.setWindowTitle(tr("settings"))
        self.setMinimumWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Rendering Mode
        mode_layout = QHBoxLayout()
        mode_label = QLabel(tr("rendering_mode"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItem(tr("remote_server"), "remote")
        self.mode_combo.addItem(tr("local_plantuml"), "local")
        
        current_mode = self.settings.get("rendering_mode", "remote")
        index = self.mode_combo.findData(current_mode)
        if index >= 0:
            self.mode_combo.setCurrentIndex(index)
            
        self.mode_combo.currentIndexChanged.connect(self.toggle_server_fields)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        layout.addLayout(mode_layout)

        # Language
        lang_layout = QHBoxLayout()
        lang_label = QLabel(tr("language"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(I18n.get_supported_languages())
        current_lang = self.settings.get("language", "EN")
        self.lang_combo.setCurrentText(current_lang)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)

        # Server URL
        self.url_label = QLabel(tr("server_url"))
        self.url_input = QLineEdit()
        self.url_input.setText(self.settings.get("server_url", ""))
        self.url_layout = QHBoxLayout()
        self.url_layout.addWidget(self.url_label)
        self.url_layout.addWidget(self.url_input)
        layout.addLayout(self.url_layout)

        # API Key
        self.api_label = QLabel(tr("api_key"))
        self.api_input = QLineEdit()
        self.api_input.setText(self.settings.get("api_key", ""))
        self.api_layout = QHBoxLayout()
        self.api_layout.addWidget(self.api_label)
        self.api_layout.addWidget(self.api_input)
        layout.addLayout(self.api_layout)
        
        self.toggle_server_fields()

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton(tr("save"))
        save_btn.clicked.connect(self.save_settings)
        cancel_btn = QPushButton(tr("cancel"))
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def toggle_server_fields(self):
        is_remote = self.mode_combo.currentData() == "remote"
        self.url_label.setVisible(is_remote)
        self.url_input.setVisible(is_remote)
        self.api_label.setVisible(is_remote)
        self.api_input.setVisible(is_remote)

    def save_settings(self):
        self.settings.set("language", self.lang_combo.currentText())
        self.settings.set("rendering_mode", self.mode_combo.currentData())
        self.settings.set("server_url", self.url_input.text().strip())
        self.settings.set("api_key", self.api_input.text().strip())
        I18n.set_language(self.lang_combo.currentText())
        
        QMessageBox.information(self, tr("info"), tr("settings_saved") + "\n" + tr("language_changed"))
        self.accept()
