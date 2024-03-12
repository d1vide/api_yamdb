import csv
import sqlite3
import datetime

from django.db.models import ForeignKey
from django.core.management.base import BaseCommand

from reviews.models import Comment, Review, Title


class Command(BaseCommand):
    help = 'Команда для импорта csv файлов в БД sqlite'

    def add_arguments(self, parser):
        parser.add_argument('-c', '--category',
                            action='store_true',
                            default=False, help='Импорт в таблицу category')
        parser.add_argument('-g', '--genre',
                            action='store_true',
                            default=False, help='Импорт в таблицу genre')
        parser.add_argument('-u', '--users',
                            action='store_true',
                            default=False, help='Импорт в таблицу user')
        parser.add_argument('-t', '--titles',
                            action='store_true',
                            default=False, help='Импорт в таблицу titles')
        parser.add_argument('-m', '--genretitles',
                            action='store_true',
                            default=False, help='Импорт в таблицу genre_title')
        parser.add_argument('-r', '--review',
                            action='store_true',
                            default=False, help='Импорт в таблицу review')
        parser.add_argument('-n', '--comments',
                            action='store_true',
                            default=False, help='Импорт в таблицу comments')

    def _import_table(self, db_table, csv_table, model=None):
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        with open(f'static/data/{csv_table}.csv', 'r',
                  encoding='utf-8-sig') as file:
            contents = csv.reader(file)
            fields = next(contents)
            if model:
                for i in range(len(fields)):
                    if fields[i][-2:] != 'id' and \
                        isinstance(model._meta.get_field(fields[i]),
                                   ForeignKey):
                        fields[i] += '_id'
            insert_query = (f"INSERT INTO {db_table} ({', '.join(fields)}) "
                            f"VALUES({', '.join('?' * len(fields))})")
            cur.executemany(insert_query, contents)
        con.commit()
        con.close()

    def _import_user(self):
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        with open('static/data/users.csv', 'r',
                  encoding='utf-8-sig') as file:
            contents = csv.reader(file)
            fields = next(contents)
            username_csv_index = fields.index('username')
            insert_query = (f"INSERT INTO users_user ({', '.join(fields)}, "
                            f"password, is_superuser, is_staff, is_active, "
                            f"date_joined) VALUES"
                            f"({', '.join('?' * (len(fields) + 5))})")
            for content in contents:
                changed_content = content
                changed_content.append(changed_content[username_csv_index])
                changed_content.append(False)
                changed_content.append(False)
                changed_content.append(False)
                changed_content.append(datetime.datetime.now())
                cur.execute(insert_query, content)
        con.commit()
        con.close()

    def handle(self, *args, **options):
        if options['category']:
            self._import_table('reviews_category', 'category')
        elif options['genre']:
            self._import_table('reviews_genre', 'genre')
        elif options['users']:
            self._import_user()
        elif options['titles']:
            self._import_table('reviews_title', 'titles', Title)
        elif options['genretitles']:
            self._import_table('reviews_titlegenre', 'genre_title')
        elif options['review']:
            self._import_table('reviews_review', 'review', Review)
        elif options['comments']:
            self._import_table('reviews_comment', 'comments', Comment)
        else:
            self._import_table('reviews_category', 'category')
            self._import_table('reviews_genre', 'genre')
            self._import_user()
            self._import_table('reviews_title', 'titles', Title)
            self._import_table('reviews_titlegenre', 'genre_title')
            self._import_table('reviews_review', 'review', Review)
            self._import_table('reviews_comment', 'comments', Comment)
