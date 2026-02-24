import os
from PyQt6.QtWidgets import (QMainWindow, QSplitter, QTreeView,
                             QWidget, QVBoxLayout, QLabel, QScrollArea, QToolBar,
                             QFileDialog, QMessageBox, QPushButton, QPlainTextEdit,
                             QSizePolicy)
from PyQt6.QtGui import QPixmap, QAction, QIcon, QFileSystemModel, QCloseEvent
from PyQt6.QtCore import Qt, QDir, QModelIndex, QSize, QThread, pyqtSignal
from core.api_client import PlantUMLClient
from core.i18n import tr, I18n
from .settings_dialog import SettingsDialog
from ui.syntax_highlighter import PlantUMLHighlighter

class RenderThread(QThread):
    finished_success = pyqtSignal(object)
    finished_error = pyqtSignal(str)

    def __init__(self, api_client, content):
        super().__init__()
        self.api_client = api_client
        self.content = content

    def run(self):
        try:
            img_bytes = self.api_client.get_png(self.content)
            self.finished_success.emit(img_bytes)
        except Exception as e:
            self.finished_error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self, settings_manager):
        super().__init__()
        self.settings = settings_manager
        I18n.set_language(self.settings.get("language", "EN"))
        self.api_client = PlantUMLClient(self.settings)
        self.current_img_bytes = None
        self.current_file_path = None
        self.scale_factor = 1.0
        self.pixmap = QPixmap()
        self.render_thread = None
        
        self.init_ui()
        self.retranslate_ui()

    def closeEvent(self, event: QCloseEvent):
        if not self.check_unsaved_changes():
            event.ignore()
        else:
            event.accept()

    def init_ui(self):
        self.resize(1000, 700)
        
        # Toolbar
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)
        
        self.action_open = QAction(self)
        self.action_open.triggered.connect(self.open_folder)
        self.toolbar.addAction(self.action_open)
        
        self.action_settings = QAction(self)
        self.action_settings.triggered.connect(self.open_settings)
        self.toolbar.addAction(self.action_settings)

        self.toolbar.addSeparator()

        self.action_render = QAction(self)
        self.action_render.triggered.connect(self.render_file)
        self.toolbar.addAction(self.action_render)
        
        self.action_save_file = QAction(self)
        self.action_save_file.triggered.connect(self.save_text_file)
        self.toolbar.addAction(self.action_save_file)

        self.action_save_image = QAction(self)
        self.action_save_image.triggered.connect(self.save_image)
        self.toolbar.addAction(self.action_save_image)

        self.toolbar.addSeparator()

        self.action_zoom_in = QAction(self)
        self.action_zoom_in.triggered.connect(self.zoom_in)
        self.toolbar.addAction(self.action_zoom_in)

        self.action_zoom_out = QAction(self)
        self.action_zoom_out.triggered.connect(self.zoom_out)
        self.toolbar.addAction(self.action_zoom_out)

        self.action_zoom_actual = QAction(self)
        self.action_zoom_actual.triggered.connect(self.zoom_actual)
        self.toolbar.addAction(self.action_zoom_actual)

        self.action_zoom_fit = QAction(self)
        self.action_zoom_fit.triggered.connect(self.zoom_fit)
        self.toolbar.addAction(self.action_zoom_fit)
        
        # Central Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(splitter)

        # Left side - File explorer
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.file_model.setNameFilters(["*.puml", "*.txt"])
        self.file_model.setNameFilterDisables(False)

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        
        # Start at current directory
        self.tree_view.setRootIndex(self.file_model.index(os.getcwd()))
        
        self.tree_view.setRootIsDecorated(True)
        self.tree_view.setHeaderHidden(True)
        # Hide standard columns config to focus on name
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)
        
        self.tree_view.clicked.connect(self.on_file_selected)
        self.tree_view.doubleClicked.connect(self.on_file_double_clicked)
        
        splitter.addWidget(self.tree_view)

        # Middle side - Text Editor
        self.text_editor = QPlainTextEdit()
        self.text_editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        font = self.text_editor.font()
        font.setFamily("Menlo" if os.name != "nt" else "Consolas")
        font.setPointSize(12)
        self.text_editor.setFont(font)
        self.highlighter = PlantUMLHighlighter(self.text_editor.document())
        splitter.addWidget(self.text_editor)

        # Right side - Image view
        self.image_label = QLabel()
        self.image_label.setBackgroundRole(self.image_label.backgroundRole()) # Enable background
        self.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.image_label.setScaledContents(True)

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(self.scroll_area.backgroundRole())
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(False) # Important for custom scaling
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        splitter.addWidget(self.scroll_area)
        
        # Default Splitter ratio
        splitter.setSizes([200, 400, 400])

        self.update_zoom_actions()

    def retranslate_ui(self):
        self.setWindowTitle(tr("app_title"))
        self.action_open.setText(tr("open_folder"))
        self.action_settings.setText(tr("settings"))
        self.action_render.setText(tr("render"))
        self.action_save_file.setText(tr("save_file"))
        self.action_save_image.setText(tr("save_image"))
        self.action_zoom_in.setText(tr("zoom_in"))
        self.action_zoom_out.setText(tr("zoom_out"))
        self.action_zoom_actual.setText(tr("zoom_actual"))
        self.action_zoom_fit.setText(tr("zoom_fit"))

    def zoom_in(self):
        self.scale_image(1.25)

    def zoom_out(self):
        self.scale_image(0.8)

    def zoom_actual(self):
        self.scale_factor = 1.0
        self.update_image_label()

    def zoom_fit(self):
        if not self.pixmap.isNull():
            fit_size = self.scroll_area.viewport().size()
            
            w_ratio = fit_size.width() / float(self.pixmap.width())
            h_ratio = fit_size.height() / float(self.pixmap.height())
            
            # Use the smaller ratio to fit inside
            self.scale_factor = min(w_ratio, h_ratio)
            self.update_image_label()

    def scale_image(self, factor):
        self.scale_factor *= factor
        self.update_image_label()
        
        self.adjust_scrollbar(self.scroll_area.horizontalScrollBar(), factor)
        self.adjust_scrollbar(self.scroll_area.verticalScrollBar(), factor)

    def adjust_scrollbar(self, scrollbar, factor):
        scrollbar.setValue(int(factor * scrollbar.value() + ((factor - 1) * scrollbar.pageStep() / 2)))

    def update_image_label(self):
        if not self.pixmap.isNull():
            self.image_label.resize(self.scale_factor * self.pixmap.size())
            self.update_zoom_actions()

    def update_zoom_actions(self):
        has_image = not self.pixmap.isNull()
        self.action_zoom_in.setEnabled(has_image)
        self.action_zoom_out.setEnabled(has_image)
        self.action_zoom_actual.setEnabled(has_image)
        self.action_zoom_fit.setEnabled(has_image)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, tr("select_folder"), QDir.homePath())
        if folder:
            idx = self.file_model.setRootPath(folder)
            self.tree_view.setRootIndex(idx)

    def open_settings(self):
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec():
            # Update client and retranslate window text
            self.api_client = PlantUMLClient(self.settings)
            self.retranslate_ui()

    def check_unsaved_changes(self) -> bool:
        if self.text_editor.document().isModified() and self.current_file_path:
            reply = QMessageBox.question(
                self, 
                tr("save_file"), 
                tr("save_changes_prompt"),
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Save
            )
            if reply == QMessageBox.StandardButton.Save:
                self.save_text_file()
                return True
            elif reply == QMessageBox.StandardButton.Cancel:
                return False
        return True

    def on_file_selected(self, index: QModelIndex):
        path = self.file_model.filePath(index)
        if not self.file_model.isDir(index) and path != self.current_file_path:
            if not self.check_unsaved_changes():
                return
                
            self.current_file_path = path
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text_editor.setPlainText(content)
                self.text_editor.document().setModified(False)
                # Auto render on load
                self.render_file()
            except Exception:
                self.text_editor.setPlainText(tr("file_load_error"))

    def on_file_double_clicked(self, index: QModelIndex):
        self.on_file_selected(index)
        self.render_file()

    def render_file(self):
        content = self.text_editor.toPlainText().strip()
        if not content:
            QMessageBox.warning(self, tr("error"), tr("no_file_selected"))
            return
            
        self.statusBar().showMessage(tr("rendering"))
        self.action_render.setEnabled(False)
        
        self.render_thread = RenderThread(self.api_client, content)
        self.render_thread.finished_success.connect(self.on_render_success)
        self.render_thread.finished_error.connect(self.on_render_error)
        self.render_thread.start()

    def on_render_success(self, img_bytes: bytes):
        self.current_img_bytes = img_bytes
        self.pixmap.loadFromData(self.current_img_bytes)
        self.image_label.setPixmap(self.pixmap)
        
        self.zoom_actual()
        self.statusBar().showMessage(tr("success"), 3000)
        self.action_render.setEnabled(True)

    def on_render_error(self, error_msg: str):
        QMessageBox.critical(self, tr("error"), tr("render_error") + f"\n\n{error_msg}")
        self.statusBar().clearMessage()
        self.action_render.setEnabled(True)

    def save_text_file(self):
        if not self.current_file_path:
            QMessageBox.warning(self, tr("error"), tr("no_file_selected"))
            return
        
        content = self.text_editor.toPlainText()
        try:
            with open(self.current_file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.text_editor.document().setModified(False)
            self.statusBar().showMessage(tr("file_saved"), 3000)
        except Exception as e:
            QMessageBox.critical(self, tr("error"), str(e))

    def save_image(self):
        if not self.current_img_bytes or not self.current_file_path:
            QMessageBox.warning(self, tr("error"), tr("no_file_selected"))
            return
        
        base_name = os.path.splitext(self.current_file_path)[0]
        out_path = f"{base_name}.png"
        
        try:
            with open(out_path, "wb") as f:
                f.write(self.current_img_bytes)
            QMessageBox.information(self, tr("success"), f"{tr('image_saved_to')} {out_path}")
        except Exception as e:
            QMessageBox.critical(self, tr("error"), str(e))
