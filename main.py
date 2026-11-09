materials = {
    1: {"title": "Основы Python", "type": "книга"},
    2: {"title": "Практические задания по Python", "type": "методичка"},
    3: {"title": "Основы алгоритмизации", "type": "книга"},
}


def main():
    print("Каталог учебных материалов")

    try:
        material_id = int(input("Введите ID материала: "))
    except ValueError:
        print("Ошибка: ID должен быть целым положительным числом.")
        return

    if material_id <= 0:
        print("Ошибка: ID должен быть целым положительным числом.")
        return

    # Ищем материал по ID
    material = materials.get(material_id)
    if material is None:
        print("Материал не найден.")
    else:
        print(f"ID: {material_id}")
        print(f"Название: {material['title']}")
        print(f"Тип: {material['type']}")


if __name__ == "__main__":
    main()
