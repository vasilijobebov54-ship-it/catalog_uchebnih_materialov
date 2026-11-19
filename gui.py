"""Графический каталог учебных материалов (Tkinter + SQLite)."""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

import catalog_db as db


class CatalogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Каталог учебных материалов")
        self.root.geometry("800x540")
        self.root.minsize(660, 430)
        self.search = tk.StringVar()
        self.category = tk.StringVar(value="Все типы")
        self.sorted_by_title = False

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", font=("Arial", 11))
        style.configure("TButton", padding=(10, 7))
        style.configure("Treeview", font=("Arial", 11), rowheight=29)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.configure("Title.TLabel", font=("Arial", 19, "bold"))
        style.configure("Sub.TLabel", foreground="#555555")
        root.configure(bg="#f1f4f8")

        area = ttk.Frame(root, padding=20)
        area.pack(fill="both", expand=True)
        ttk.Label(area, text="Каталог учебных материалов", style="Title.TLabel").pack(anchor="w")
        ttk.Label(area, text="Поиск и управление книгами и методичками", style="Sub.TLabel").pack(anchor="w", pady=(3, 15))

        toolbar = ttk.Frame(area)
        toolbar.pack(fill="x", pady=(0, 10))
        ttk.Entry(toolbar, textvariable=self.search).pack(side="left", fill="x", expand=True)
        ttk.Button(toolbar, text="Найти", command=self.refresh).pack(side="left", padx=(8, 0))
        ttk.Button(toolbar, text="Сброс", command=self.clear_search).pack(side="left", padx=(8, 0))
        self.search.trace_add("write", lambda *_: self.refresh())

        extras = ttk.Frame(area)
        extras.pack(fill="x", pady=(0, 10))
        ttk.Label(extras, text="Тип:").pack(side="left")
        self.types_box = ttk.Combobox(extras, textvariable=self.category, state="readonly", width=20)
        self.types_box.pack(side="left", padx=8)
        self.types_box.bind("<<ComboboxSelected>>", lambda _: self.filter_by_type())
        ttk.Button(extras, text="По алфавиту", command=self.sort_by_title).pack(side="left", padx=5)
        ttk.Button(extras, text="Статистика", command=self.show_statistics).pack(side="left", padx=5)

        table_frame = ttk.Frame(area)
        table_frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(table_frame, columns=("id", "title", "type"), show="headings", selectmode="browse")
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Название")
        self.tree.heading("type", text="Тип")
        self.tree.column("id", width=65, stretch=False, anchor="center")
        self.tree.column("title", width=390)
        self.tree.column("type", width=160)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        actions = ttk.Frame(area)
        actions.pack(fill="x", pady=(12, 0))
        ttk.Button(actions, text="Добавить", command=self.add).pack(side="left", padx=(0, 7))
        ttk.Button(actions, text="Изменить", command=self.edit).pack(side="left", padx=7)
        ttk.Button(actions, text="Удалить", command=self.delete).pack(side="left", padx=7)
        ttk.Button(actions, text="Обновить", command=self.refresh).pack(side="left", padx=7)
        self.status = ttk.Label(area, text="")
        self.status.pack(anchor="w", pady=(10, 0))
        self.refresh()

    def refresh_types(self):
        choices = ["Все типы"] + db.get_types()
        self.types_box["values"] = choices
        if self.category.get() not in choices:
            self.category.set("Все типы")

    def refresh(self):
        self.refresh_types()
        selected_type = "" if self.category.get() == "Все типы" else self.category.get()
        rows = db.get_materials(self.search.get(), selected_type, self.sorted_by_title)
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in rows:
            self.tree.insert("", "end", values=(item["id"], item["title"], item["type"]))
        self.status.config(text=f"Найдено материалов: {len(rows)}")

    def clear_search(self):
        self.search.set("")
        self.category.set("Все типы")
        self.sorted_by_title = False
        self.refresh()

    def selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Каталог", "Сначала выберите материал в таблице.")
            return None
        return self.tree.item(selected[0], "values")

    def add(self):
        title = simpledialog.askstring("Добавление", "Название материала:", parent=self.root)
        if title is None:
            return
        category = simpledialog.askstring("Добавление", "Тип материала:", parent=self.root)
        if category is None:
            return
        try:
            db.add_material(title, category)
            self.refresh()
        except ValueError as error:
            messagebox.showerror("Ошибка", str(error))

    def edit(self):
        item = self.selected()
        if item is None:
            return
        title = simpledialog.askstring("Редактирование", "Новое название:", initialvalue=item[1], parent=self.root)
        if title is None:
            return
        category = simpledialog.askstring("Редактирование", "Новый тип:", initialvalue=item[2], parent=self.root)
        if category is None:
            return
        try:
            db.edit_material(int(item[0]), title, category)
            self.refresh()
        except ValueError as error:
            messagebox.showerror("Ошибка", str(error))

    def delete(self):
        item = self.selected()
        if item is None:
            return
        if messagebox.askyesno("Удаление", f"Удалить «{item[1]}»?"):
            db.delete_material(int(item[0]))
            self.refresh()

    # Три дополнительные функции второго спринта.
    def sort_by_title(self):
        self.sorted_by_title = not self.sorted_by_title
        self.refresh()

    def filter_by_type(self):
        self.refresh()

    def show_statistics(self):
        total, groups = db.statistics()
        details = "\n".join(f"{category}: {count}" for category, count in groups)
        messagebox.showinfo("Статистика каталога", f"Всего материалов: {total}\n\n{details}")


if __name__ == "__main__":
    db.initialize()
    window = tk.Tk()
    CatalogApp(window)
    window.mainloop()
