materials = {
    1: {"title": "Основы Python", "type": "книга"},
    2: {"title": "Практические задания по Python", "type": "методичка"},
    3: {"title": "Основы алгоритмизации", "type": "книга"},
}


def show_all():
    for item_id, item in materials.items():
        print(f"{item_id}. {item['title']} ({item['type']})")


def show_by_id():
    try:
        material_id = int(input("Введите ID материала: "))
    except ValueError:
        print("Ошибка: введите целое число.")
        return

    if material_id <= 0:
        print("Ошибка: ID должен быть положительным.")
        return

    material = materials.get(material_id)
    if material is None:
        print("Материал не найден.")
    else:
        print(f"ID: {material_id}")
        print(f"Название: {material['title']}")
        print(f"Тип: {material['type']}")


def search_by_title():
    query = input("Введите название: ").strip().lower()
    if not query:
        print("Введите название для поиска.")
        return

    found = False
    for item_id, item in materials.items():
        if query in item["title"].lower():
            print(f"{item_id}. {item['title']} ({item['type']})")
            found = True

    if not found:
        print("Материалы не найдены.")


def add_material():
    title = input("Название материала: ").strip()
    if not title:
        print("Название не может быть пустым.")
        return

    material_type = input("Тип материала: ").strip()
    if not material_type:
        print("Тип не может быть пустым.")
        return

    new_id = max(materials, default=0) + 1
    materials[new_id] = {"title": title, "type": material_type}
    print(f"Материал добавлен. ID: {new_id}")


def edit_material():
    try:
        material_id = int(input("Введите ID материала: "))
    except ValueError:
        print("Ошибка: введите целое число.")
        return

    if material_id not in materials:
        print("Материал не найден.")
        return

    title = input("Новое название: ").strip()
    material_type = input("Новый тип: ").strip()
    if not title or not material_type:
        print("Название и тип не могут быть пустыми.")
        return

    materials[material_id] = {"title": title, "type": material_type}
    print("Материал изменён.")


def main():
    while True:
        print("\nКаталог учебных материалов")
        print("-" * 30)
        print("1 - Все материалы")
        print("2 - Поиск по ID")
        print("3 - Поиск по названию")
        print("4 - Добавить материал")
        print("5 - Редактировать материал")
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
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
