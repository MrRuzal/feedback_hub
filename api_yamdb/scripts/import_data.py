import csv
import os
import sys
from api_yamdb.settings import BASE_DIR

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    GenreTitle,
    User,
)


def create_user_data(row):
    User.objects.create(
        pk=row[0],
        username=row[1],
        email=row[2],
        role=row[3],
        bio=row[4],
        first_name=row[5],
        last_name=row[6],
    )


def create_category_data(row):
    Category.objects.create(pk=row[0], name=row[1], slug=row[2])


def create_genre_data(row):
    Genre.objects.create(pk=row[0], name=row[1], slug=row[2])


def create_title_data(row):
    Title.objects.create(pk=row[0], name=row[1], year=row[2], category=row[3])


def create_genre_title_data(row):
    GenreTitle.objects.create(pk=row[0], title_id=row[1], genre_id=row[2])


def create_review_data(row):
    Review.objects.create(
        pk=row[0],
        title=row[1],
        text=row[2],
        author=row[3],
        score=row[4],
        pub_date=row[5],
    )


def create_comment_data(row):
    Comment.objects.create(
        pk=row[0], review=row[1], text=row[2], author=row[3], pub_date=row[4]
    )


def run():
    your_djangoproject_home = BASE_DIR
    sys.path.append(your_djangoproject_home)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'api_yamdb.settings'
    local_base_dir = os.path.join(BASE_DIR, 'static\\data\\')
    files = {
        'users.csv': create_user_data,
        'category.csv': create_category_data,
        'genre.csv': create_genre_data,
        'titles.csv': create_title_data,
        'genre_title.csv': create_genre_title_data,
        'review.csv': create_review_data,
        'comments.csv': create_comment_data,
    }
    for file, func in files.items():
        dataReader = csv.reader(
            open(os.path.join(local_base_dir, file)),
            delimiter=',',
            quotechar='"',
        )
        for row in dataReader:
            if row[0] == 'id':
                continue
            func(row)
