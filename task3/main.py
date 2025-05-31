import sys
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLineEdit, QTextEdit,
                             QDateTimeEdit, QComboBox, QTreeView, QMessageBox)
from PyQt6.QtCore import Qt
from todo_model import TodoModel, TodoItem
from todo_delegate import TodoDelegate


class TodoView(QMainWindow):
    """Main window for the todo application."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo List - MVC Example")
        self.setGeometry(100, 100, 800, 600)

        self.model = TodoModel()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        form_layout = QHBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Title")
        form_layout.addWidget(self.title_input)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Description")
        self.description_input.setMaximumHeight(50)
        form_layout.addWidget(self.description_input)

        self.due_date_input = QDateTimeEdit()
        self.due_date_input.setDateTime(datetime.now())
        form_layout.addWidget(self.due_date_input)

        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItem("General")
        form_layout.addWidget(self.category_input)

        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        form_layout.addWidget(add_button)

        layout.addLayout(form_layout)

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setItemDelegate(TodoDelegate())
        self.tree_view.setAlternatingRowColors(True)
        layout.addWidget(self.tree_view)

        button_layout = QHBoxLayout()

        complete_button = QPushButton("Mark as Completed")
        complete_button.clicked.connect(self.mark_completed)
        button_layout.addWidget(complete_button)

        delete_button = QPushButton("Delete Task")
        delete_button.clicked.connect(self.delete_task)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        self.add_sample_tasks()

    def add_task(self):
        """Add a new task to the model."""
        title = self.title_input.text()
        description = self.description_input.toPlainText()
        due_date = self.due_date_input.dateTime().toPyDateTime()
        category = self.category_input.currentText()

        if not title:
            QMessageBox.warning(self, "Warning", "Title cannot be empty!")
            return

        item = TodoItem(
            title=title,
            description=description,
            due_date=due_date,
            category=category
        )

        self.model.addItem(item)
        self.clear_inputs()

        if category not in [self.category_input.itemText(i) for i in range(self.category_input.count())]:
            self.category_input.addItem(category)

    def clear_inputs(self):
        """Clear all input fields."""
        self.title_input.clear()
        self.description_input.clear()
        self.due_date_input.setDateTime(datetime.now())
        self.category_input.setCurrentText("General")

    def mark_completed(self):
        """Mark selected task as completed."""
        indexes = self.tree_view.selectedIndexes()
        if not indexes:
            return

        row = indexes[0].row()
        item = self.model.getItem(row)
        if item:
            item.completed = True
            self.model.updateItem(row, item)

    def delete_task(self):
        """Delete selected task."""
        indexes = self.tree_view.selectedIndexes()
        if not indexes:
            return

        row = indexes[0].row()
        self.model.removeItem(row)

    def add_sample_tasks(self):
        """Add some sample tasks to demonstrate the application."""
        sample_tasks = [
            TodoItem(
                title="Complete Project",
                description="Finish the MVC project implementation",
                due_date=datetime.now(),
                category="Work"
            ),
            TodoItem(
                title="Buy Groceries",
                description="Milk, eggs, bread",
                due_date=datetime.now(),
                category="Personal"
            ),
            TodoItem(
                title="Exercise",
                description="30 minutes of cardio",
                due_date=datetime.now(),
                completed=True,
                category="Health"
            )
        ]

        for task in sample_tasks:
            self.model.addItem(task)
            if task.category not in [self.category_input.itemText(i) for i in range(self.category_input.count())]:
                self.category_input.addItem(task.category)


def main():
    app = QApplication(sys.argv)
    view = TodoView()
    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
