# api_yamdb
## Описание проекта:
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/d1vide/api_yamdb.git
```
```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
. venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
Перенести данные из csv в базу данных:
```
python3 manage.py importcsv
```
Использованные технологии:
* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
* ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

Информация об авторах:
* <a href="https://github.com/Jim-0e">Гаджимурад Саидов</a>
* <a href="https://github.com/etgapi">Анна Цой</a>
* <a href="https://github.com/d1vide">Алексей Наумов</a>

