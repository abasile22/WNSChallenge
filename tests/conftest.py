import pytest
import sqlite3
import os
from unittest.mock import Mock


@pytest.fixture
def test_db():
    """Create a temporary test database"""
    db_path = "test_db.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient TEXT NOT NULL,
            weight REAL,
            meal_id INTEGER NOT NULL,
            FOREIGN KEY (meal_id) REFERENCES meals(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe TEXT NOT NULL,
            meal_id INTEGER NOT NULL,
            FOREIGN KEY (meal_id) REFERENCES meals(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')

    conn.commit()

    yield conn

    conn.close()
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def mock_flask_app():
    """Create a mock Flask app for testing"""
    from flask import Flask
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def mock_file():
    """Create a mock file object"""
    mock = Mock()
    mock.filename = "test_file.txt"
    mock.read.return_value = b"test content"
    return mock
