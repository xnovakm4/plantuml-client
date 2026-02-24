import re
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import Qt

class PlantUMLHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # 1. Keywords (Blue)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keywords = [
            r"@startuml", r"@enduml", r"!define", r"!include", r"title",
            r"skinparam", r"as", r"true", r"false", r"actor", r"participant",
            r"usecase", r"class", r"interface", r"package", r"node",
            r"database", r"cloud", r"state", r"note", r"end note", r"return"
        ]
        for word in keywords:
            if word.startswith("@") or word.startswith("!"):
                pattern = re.compile(f"{word}\\b")
            else:
                pattern = re.compile(f"\\b{word}\\b")
            self.highlighting_rules.append((pattern, keyword_format))

        # Braces
        brace_pattern = re.compile(r"[{}]")
        self.highlighting_rules.append((brace_pattern, keyword_format))

        # 2. Properties and Defines (Teal / Dark Cyan)
        property_format = QTextCharFormat()
        property_format.setForeground(QColor("darkcyan"))
        properties = [
            r"BackgroundColor", r"BorderColor", r"FontColor", r"Shadowing", r"linetype"
        ]
        for prop in properties:
            self.highlighting_rules.append((re.compile(f"\\b{prop}\\b"), property_format))
            
        # Highlight anything after !include as Teal until the end of word or line
        include_val_pattern = re.compile(r"(?<=!include )\S+")
        self.highlighting_rules.append((include_val_pattern, property_format))
        
        define_val_pattern = re.compile(r"(?<=!define )\S+")
        self.highlighting_rules.append((define_val_pattern, property_format))

        # 3. Hex Colors (SeaGreen)
        hexcolor_format = QTextCharFormat()
        hexcolor_format.setForeground(QColor("seagreen"))
        hexcolor_pattern = re.compile(r"#[0-9a-fA-F]{3,6}\b")
        self.highlighting_rules.append((hexcolor_pattern, hexcolor_format))

        # 4. Strings (Brown / Dark Red)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(163, 21, 21)) # Brownish red
        string_pattern = re.compile(r'"[^"\\]*(\\.[^"\\]*)*"')
        self.highlighting_rules.append((string_pattern, string_format))

        # 5. Comments (Red)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("red"))
        comment_pattern = re.compile(r"'.*")
        self.highlighting_rules.append((comment_pattern, comment_format))

    def highlightBlock(self, text: str):
        # We process highlights in order, later rules can override earlier ones if needed.
        for pattern, fmt in self.highlighting_rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)
