import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

# Файл для хранения избранных пользователей
FAVORITES_FILE = "favorites.json"

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("700x500")

        # Загрузка избранного из файла
        self.favorites = self.load_favorites()

        # Виджеты
        tk.Label(root, text="Введите имя пользователя GitHub:").pack(pady=5)
        self.search_entry = tk.Entry(root, width=50)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(root, text="Поиск", command=self.search_users)
        self.search_button.pack(pady=5)

        # Список результатов
        self.results_listbox = tk.Listbox(root, width=80, height=15)
        self.results_listbox.pack(pady=10)
        self.results_listbox.bind("<Double-Button-1>", self.show_user_info)

        # Кнопка добавления в избранное
        self.fav_button = tk.Button(root, text="Добавить в избранное", command=self.add_to_favorites)
        self.fav_button.pack(pady=5)

        # Список избранных
        tk.Label(root, text="Избранные пользователи:").pack()
        self.favorites_listbox = tk.Listbox(root, width=80, height=8)
        self.favorites_listbox.pack(pady=5)
        self.favorites_listbox.bind("<Double-Button-1>", self.show_favorite_info)

        self.update_favorites_listbox()

    def load_favorites(self):
        """Загружает избранных пользователей из JSON файла."""
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_favorites(self):
        """Сохраняет избранных пользователей в JSON файл."""
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(self.favorites, f, indent=4, ensure_ascii=False)

    def search_users(self):
        """Выполняет поиск пользователей через GitHub API."""
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым!")
            return

        url = f"https://api.github.com/search/users?q={query}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            users = data.get("items", [])

            self.results_listbox.delete(0, tk.END)
            for user in users:
                self.results_listbox.insert(tk.END, f"{user['login']} — {user['html_url']}")
                # Сохраняем данные пользователя в атрибут списка
                if not hasattr(self.results_listbox, 'user_data'):
                    self.results_listbox.user_data = {}
                self.results_listbox.user_data[user['login']] = user

            if not users:
                messagebox.showinfo("Результат", "Пользователи не найдены.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить запрос:\n{e}")

    def add_to_favorites(self):
        """Добавляет выбранного пользователя в избранное."""
        selection = self.results_listbox.curselection()
        if not selection:
            messagebox.showwarning("Ошибка", "Сначала выберите пользователя из результатов поиска.")
            return

        selected_text = self.results_listbox.get(selection[0])
        username = selected_text.split(" — ")[0]

        # Проверяем, не добавлен ли уже
        if any(fav['login'] == username for fav in self.favorites):
            messagebox.showinfo("Информация", f"Пользователь {username} уже в избранном.")
            return

        # Получаем полные данные пользователя
        user_data = self.results_listbox.user_data.get(username)
        if not user_data:
            messagebox.showerror("Ошибка", "Не удалось получить данные пользователя.")
            return

        self.favorites.append(user_data)
        self.save_favorites()
        self.update_favorites_listbox()
        messagebox.showinfo("Успех", f"Пользователь {username} добавлен в избранное.")

    def update_favorites_listbox(self):
        """Обновляет список избранных пользователей в GUI."""
        self.favorites_listbox.delete(0, tk.END)
        for user in self.favorites:
            self.favorites_listbox.insert(tk.END, f"{user['login']} — {user['html_url']}")

    def show_user_info(self, event):
        """Показывает информацию о выбранном пользователе из результатов поиска."""
        selection = self.results_listbox.curselection()
        if selection:
            selected_text = self.results_listbox.get(selection[0])
            username = selected_text.split(" — ")[0]
            user_data = self.results_listbox.user_data.get(username)
            if user_data:
                info = f"Логин: {user_data['login']}\nID: {user_data['id']}\nСсылка: {user_data['html_url']}"
                messagebox.showinfo("Информация о пользователе", info)

    def show_favorite_info(self, event):
        """Показывает информацию о выбранном избранном пользователе."""
        selection = self.favorites_listbox.curselection()
        if selection:
            selected_text = self.favorites_listbox.get(selection[0])
            username = selected_text.split(" — ")[0]
            user_data = next((user for user in self.favorites if user['login'] == username), None)
            if user_data:
                info = f"Логин: {user_data['login']}\nID: {user_data['id']}\nСсылка: {user_data['html_url']}"
                messagebox.showinfo("Информация об избранном пользователе", info)

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
