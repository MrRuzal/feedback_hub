import csv
import os

from api_yamdb.settings import BASE_DIR
from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User,
)


def run():
    local_base_dir = os.path.join(BASE_DIR, 'static\\data\\')
    files_csv = {
        'users.csv': User,
        'category.csv': Category,
        'genre.csv': Genre,
        'titles.csv': Title,
        'genre_title.csv': GenreTitle,
        'review.csv': Review,
        'comments.csv': Comment,
    }
    for file, model in files_csv.items():
        dataReader = csv.DictReader(
            open(
                os.path.join(local_base_dir, file),
                encoding='utf-8',
            ),
        )
        if file == 'genre_title.csv':
            for row in dataReader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                model.objects.create(
                    id=row['id'], title_id=title, genre_id=genre
                )
        for row in dataReader:
            for key in ('category', 'author'):
                if key in row:
                    value = row.pop(key)
                    row[f'{key}_id'] = value
            model.objects.create(**row)
    print('Successfull!!! Import finished.')
