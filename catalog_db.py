"""Хранение каталога в SQLite. База создаётся при первом запуске."""
import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("materials.db")
JSON_PATH = Path(__file__).with_name("materials.json")
DEMO = [
    ("Основы Python", "книга"),
    ("Практические задания по Python", "методичка"),
    ("Основы алгоритмизации", "книга"),
]


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL
        )""")
        count = con.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
        if count:
            return
        if JSON_PATH.exists():
            try:
                data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
                for key, item in sorted(data.items(), key=lambda pair: int(pair[0])):
                    con.execute(
                        "INSERT INTO materials(id, title, type) VALUES (?, ?, ?)",
                        (int(key), item["title"], item["type"]),
                    )
                return
            except (ValueError, KeyError, TypeError, json.JSONDecodeError):
                print("Не удалось импортировать materials.json. Используем примеры.")
        con.executemany("INSERT INTO materials(title, type) VALUES (?, ?)", DEMO)


def get_materials(search="", category="", sort=False):
    sql = "SELECT id, title, type FROM materials WHERE title LIKE ?"
    params = ["%" + search + "%"]
    if category:
        sql += " AND type = ?"
        params.append(category)
    sql += " ORDER BY title COLLATE NOCASE, id" if sort else " ORDER BY id"
    with connect() as con:
        return [dict(row) for row in con.execute(sql, params)]


def get_types():
    with connect() as con:
        return [row[0] for row in con.execute("SELECT DISTINCT type FROM materials ORDER BY type")]


def add_material(title, category):
    if not title.strip() or not category.strip():
        raise ValueError("Название и тип не могут быть пустыми.")
    with connect() as con:
        return con.execute(
            "INSERT INTO materials(title, type) VALUES (?, ?)",
            (title.strip(), category.strip()),
        ).lastrowid


def edit_material(material_id, title, category):
    if not title.strip() or not category.strip():
        raise ValueError("Название и тип не могут быть пустыми.")
    with connect() as con:
        cursor = con.execute(
            "UPDATE materials SET title = ?, type = ? WHERE id = ?",
            (title.strip(), category.strip(), material_id),
        )
        return cursor.rowcount > 0


def delete_material(material_id):
    with connect() as con:
        return con.execute("DELETE FROM materials WHERE id = ?", (material_id,)).rowcount > 0


def statistics():
    with connect() as con:
        total = con.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
        groups = con.execute(
            "SELECT type, COUNT(*) AS amount FROM materials GROUP BY type ORDER BY type"
        ).fetchall()
    return total, [(row["type"], row["amount"]) for row in groups]
