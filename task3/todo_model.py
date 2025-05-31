from PyQt6.QtCore import Qt, QAbstractItemModel, QModelIndex, QObject
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TodoItem:
    """Class representing a todo item."""
    title: str
    description: str
    due_date: datetime
    completed: bool = False
    category: str = "General"


class TodoModel(QAbstractItemModel):
    """Custom model for todo items."""

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._items: List[TodoItem] = []
        self._categories: Dict[str, List[int]] = {"General": []}

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the number of columns."""
        return 4  

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return the number of rows."""
        if parent.isValid():
            return 0
        return len(self._items)

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        """Create and return an index for the given row and column."""
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        return self.createIndex(row, column)

    def parent(self, child: QModelIndex) -> QModelIndex:
        """Return the parent index."""
        return QModelIndex()

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        """Return the data for the given role."""
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            item = self._items[index.row()]
            if index.column() == 0:
                return item.title
            elif index.column() == 1:
                return item.description
            elif index.column() == 2:
                return item.due_date.strftime("%Y-%m-%d %H:%M")
            elif index.column() == 3:
                return "Completed" if item.completed else "Pending"

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        """Return the header data."""
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            headers = ["Title", "Description", "Due Date", "Status"]
            return headers[section]
        return None

    def addItem(self, item: TodoItem) -> None:
        """Add a new todo item."""
        self.beginInsertRows(QModelIndex(), len(self._items), len(self._items))
        self._items.append(item)
        if item.category not in self._categories:
            self._categories[item.category] = []
        self._categories[item.category].append(len(self._items) - 1)
        self.endInsertRows()

    def removeItem(self, row: int) -> None:
        """Remove a todo item."""
        if 0 <= row < len(self._items):
            self.beginRemoveRows(QModelIndex(), row, row)
            item = self._items.pop(row)
            self._categories[item.category].remove(row)
            self.endRemoveRows()

    def updateItem(self, row: int, item: TodoItem) -> None:
        """Update a todo item."""
        if 0 <= row < len(self._items):
            self._items[row] = item
            self.dataChanged.emit(self.index(row, 0), self.index(row, 3))

    def getItem(self, row: int) -> Optional[TodoItem]:
        """Get a todo item by row."""
        if 0 <= row < len(self._items):
            return self._items[row]
        return None

    def getItemsByCategory(self, category: str) -> List[TodoItem]:
        """Get all items in a category."""
        return [self._items[i] for i in self._categories.get(category, [])]

    def getCategories(self) -> List[str]:
        """Get all categories."""
        return list(self._categories.keys())

    def clear(self) -> None:
        """Clear all todo items and categories."""
        self.beginResetModel()
        self._items.clear()
        self._categories = {"General": []}
        self.endResetModel()
