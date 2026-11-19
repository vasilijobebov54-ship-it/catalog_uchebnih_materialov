"""Консольная версия каталога, использующая общую базу SQLite."""
import catalog_db as db


def show_all():
    rows = db.get_materials()
    if not rows:
        print("Каталог пуст.")
    for item in rows:
        print(f"{item['id']}. {item['title']} ({item['type']})")


def read_id():
    try:
        material_id = int(input("Введите ID материала: "))
        if material_id <= 0:
            raise ValueError
        return material_id
    except ValueError:
        print("Ошибка: введите положительный целый ID.")
        return None


def show_by_id():
    material_id = read_id()
    if material_id is None:
        return
    item = next((row for row in db.get_materials() if row["id"] == material_id), None)
    if item is None:
        print("Материал не найден.")
    else:
        print(f"ID: {item['id']}")
        print(f"Название: {item['title']}")
        print(f"Тип: {item['type']}")
        print(f"Файл: {item['file_path'] or 'не прикреплён'}")


def search_by_title():
    query = input("Введите название: ").strip()
    if not query:
        print("Введите название для поиска.")
        return
    rows = db.get_materials(search=query)
    if not rows:
        print("Материалы не найдены.")
    for item in rows:
        print(f"{item['id']}. {item['title']} ({item['type']})")


def add_material():
    title = input("Название материала: ").strip()
    material_type = input("Тип материала: ").strip()
    try:
        new_id = db.add_material(title, material_type)
        print(f"Материал добавлен. ID: {new_id}")
    except ValueError as error:
        print(error)


def edit_material():
    material_id = read_id()
    if material_id is None:
        return
    title = input("Новое название: ").strip()
    material_type = input("Новый тип: ").strip()
    try:
        if db.edit_material(material_id, title, material_type):
            print("Материал изменён.")
        else:
            print("Материал не найден.")
    except ValueError as error:
        print(error)


def delete_material():
    material_id = read_id()
    if material_id is None:
        return
    if db.delete_material(material_id):
        print("Материал удалён.")
    else:
        print("Материал не найден.")


def main():
    db.initialize()
    while True:
        print("\nКаталог учебных материалов")
        print("-" * 30)
        print("1 - Все материалы")
        print("2 - Поиск по ID")
        print("3 - Поиск по названию")
        print("4 - Добавить материал")
        print("5 - Редактировать материал")
        print("6 - Удалить материал")
        print("0 - Выход")
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            show_all()
        elif choice == "2":
            show_by_id()
        elif choice == "3":
            search_by_title()
        elif choice == "4":
            add_material()
        elif choice == "5":
            edit_material()
        elif choice == "6":
            delete_material()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
