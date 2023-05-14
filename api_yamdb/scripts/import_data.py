import csv
from io import TextIOWrapper
import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class Command(BaseCommand):
    help = 'Import data from csv files'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to the folder with csv files')

    def run(self, *args, **kwargs):
        path = kwargs['path']

        models = {
            'category.csv': (Category, ['id', 'name', 'slug']),
            'comment.csv': (Comment, ['id', 'review_id', 'author_id', 'text', 'pub_date']),
            'genre.csv': (Genre, ['id', 'name', 'slug']),
            'review.csv': (Review, ['id', 'title_id', 'author_id', 'text', 'pub_date', 'score']),
            'title.csv': (Title, ['id', 'name', 'count_review', 'sum_score', 'year', 'description', 'category_id']),
            'user.csv': (User, ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'password', 'role']),
        }

        for filename, (model, fields) in models.items():
            with open(os.path.join(path, filename), newline='') as csvfile:
                reader = csv.DictReader(TextIOWrapper(csvfile, 'utf-8'), delimiter=',')
                objs = [model(**{field: row[field] for field in fields}) for row in reader]
                model.objects.bulk_create(objs, ignore_conflicts=True)
