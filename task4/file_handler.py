import json
import sys
import os
from datetime import datetime
from typing import List
from dataclasses import asdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from task3.todo_model import TodoItem


class FileHandler:
    """Handler for reading and writing todo items in JSON format."""

    @staticmethod
    def save_json(items: List[TodoItem], filename: str) -> None:
        """Save todo items to a JSON file."""
        data = [asdict(item) for item in items]
        for item in data:
            item['due_date'] = item['due_date'].isoformat()

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_json(filename: str) -> List[TodoItem]:
        """Load todo items from a JSON file."""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        items = []
        for item in data:
            item['due_date'] = datetime.fromisoformat(item['due_date'])
            items.append(TodoItem(**item))
        return items

    @staticmethod
    def save_xml(items: List[TodoItem], filename: str) -> None:
        """Save todo items to an XML file."""
        doc = xml.dom.minidom.Document()
        root = doc.createElement('todos')
        doc.appendChild(root)

        for item in items:
            todo = doc.createElement('todo')
            for key, value in asdict(item).items():
                if key == 'due_date':
                    value = value.isoformat()
                elif isinstance(value, bool):
                    value = str(value).lower()
                elem = doc.createElement(key)
                elem.appendChild(doc.createTextNode(str(value)))
                todo.appendChild(elem)
            root.appendChild(todo)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(doc.toprettyxml(indent='  '))

    @staticmethod
    def load_xml(filename: str) -> List[TodoItem]:
        """Load todo items from an XML file."""
        doc = xml.dom.minidom.parse(filename)
        items = []

        for todo in doc.getElementsByTagName('todo'):
            item_data = {}
            for child in todo.childNodes:
                if child.nodeType == xml.dom.Node.ELEMENT_NODE:
                    key = child.tagName
                    value = child.firstChild.nodeValue
                    if key == 'due_date':
                        value = datetime.fromisoformat(value)
                    elif key == 'completed':
                        value = value.lower() == 'true'
                    item_data[key] = value
            items.append(TodoItem(**item_data))
        return items

    @staticmethod
    def save_ini(items: List[TodoItem], filename: str) -> None:
        """Save todo items to an INI file."""
        config = configparser.ConfigParser()

        for i, item in enumerate(items):
            section = f'todo_{i}'
            config[section] = asdict(item)
            config[section]['due_date'] = item.due_date.isoformat()
            config[section]['completed'] = str(item.completed).lower()

        with open(filename, 'w', encoding='utf-8') as f:
            config.write(f)

    @staticmethod
    def load_ini(filename: str) -> List[TodoItem]:
        """Load todo items from an INI file."""
        config = configparser.ConfigParser()
        config.read(filename, encoding='utf-8')

        items = []
        for section in config.sections():
            item_data = dict(config[section])
            item_data['due_date'] = datetime.fromisoformat(
                item_data['due_date'])
            item_data['completed'] = item_data['completed'].lower() == 'true'
            items.append(TodoItem(**item_data))
        return items
