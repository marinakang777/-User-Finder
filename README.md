# User Finder

**Автор:
 **Ногова Алина
Группа/курс: Python начальный уровень
Дата: Май 2026 

## Описание
GUI-приложение для поиска пользователей GitHub через официальное API.  
Позволяет добавлять пользователей в избранное и сохранять их в JSON-файл.

Технологии
Python 3
Tkinter (GUI)
requests (работа с API)
JSON (хранение данных)

## Как использовать API
Приложение использует **GitHub Search API**:
- Эндпоинт: `https://api.github.com/search/users?q={query}`
- Метод: `GET`
- Ответ содержит список пользователей с логинами, ID и ссылками на профили.

## Установка и запуск
1. Установите Python 3.6+.
2. Установите зависимости:
   ```bash
 3. Запустите:

bash

python github_user_finder.py

Примеры использования

Введите octocat в поле поиска → нажмите "Поиск" → получите профили.

Дважды кликните по пользователю в результатах — информация.

Выберите пользователя → "Добавить в избранное" → он сохранится в favorites.json.

Избранные отображаются в нижнем списке, по двойному клику — детали.

Тесты (примеры для проверки)
Пустое поле поиска → предупреждение.

Поиск test → список пользователей.

Добавление одного пользователя несколько раз → сообщение "уже в избранном".

После перезапуска приложения избранные сохраняются.

Ссылка на репозиторий
https://github.com/marinakang777/-User-Finder


## 4. Как проверить работу

1. Скопируйте код в файл `github_user_finder.py`.
2. Установите `requests`: `pip install requests`.
3. Запустите приложение.
4. Выполните поиск (например, `python` или `torvalds`).
5. Добавьте пользователей в избранное.
6. Закройте и откройте заново — избранные сохраняются в `favorites.json`.
  pip install requests


mkdir github-user-finder
cd github-user-finder

# Создаём файлы
echo -e "__pycache__/\n*.pyc\nfavorites.json\n*.log" > .gitignore
touch README.md
# Скопируйте код выше в github_user_finder.py

Git
git init
git add .
git commit -m "Initial commit: GitHub User Finder"
git remote add origin https://github.com/marinakang777/-User-Finder.git
git push -u origin main
