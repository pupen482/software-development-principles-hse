from PyQt6.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtGui import QPainter, QColor, QPen
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TodoDelegate(QStyledItemDelegate):
    """Custom delegate for todo items."""

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        """Custom painting of todo items."""
        if index.column() == 3:  
            status = index.data()
            if status == "Completed":
                painter.fillRect(option.rect, QColor(
                    200, 255, 200))  
            else:
                painter.fillRect(option.rect, QColor(
                    255, 200, 200))  

        super().paint(painter, option, index)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        """Create editor for editing items."""
        if index.column() == 3:  
            return None  
        return super().createEditor(parent, option, index)
