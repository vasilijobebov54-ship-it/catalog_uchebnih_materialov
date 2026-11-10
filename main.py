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


def main():
    while True:
        print("\nКаталог учебных материалов")
        print("-" * 30)
        print("1 - Все материалы")
        print("2 - Поиск по ID")
        print("3 - Поиск по названию")
        print("4 - Добавить материал")
        print("0 - Выход")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            show_all()
        elif choice == "2":
            show_by_id()
        elif choice in ("3", "4"):
            print("Функция пока в разработке.")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
