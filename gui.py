import tkinter as tk
from tkinter import messagebox


def not_ready():
    messagebox.showinfo("Каталог", "Функция будет добавлена позже.")


root = tk.Tk()
root.title("Каталог учебных материалов")
root.geometry("520x400")

tk.Label(root, text="Каталог учебных материалов", font=("Arial", 16)).pack(pady=12)

search_frame = tk.Frame(root)
search_frame.pack(fill="x", padx=15)
tk.Label(search_frame, text="Поиск:").pack(side="left")
search_entry = tk.Entry(search_frame)
search_entry.pack(side="left", fill="x", expand=True, padx=8)
tk.Button(search_frame, text="Найти", command=not_ready).pack(side="left")

materials_list = tk.Listbox(root, height=11)
materials_list.pack(fill="both", expand=True, padx=15, pady=12)

buttons = tk.Frame(root)
buttons.pack(pady=(0, 15))
tk.Button(buttons, text="Добавить", command=not_ready).pack(side="left", padx=5)
tk.Button(buttons, text="Изменить", command=not_ready).pack(side="left", padx=5)
tk.Button(buttons, text="Удалить", command=not_ready).pack(side="left", padx=5)
tk.Button(buttons, text="Обновить", command=not_ready).pack(side="left", padx=5)

root.mainloop()
