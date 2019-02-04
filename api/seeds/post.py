from faker import Faker
from django.db import transaction
from api.users.models import User
from api.posts.models import Post, Comment
from api.management.commands.seed import SeedException
from random import choice, choices

dependence = [User]


@transaction.atomic
def generate_data(number):
    for i in dependence:
        if not i.objects.exists():
            raise SeedException('flog needs %s' % str(type(i)))

    users = User.objects.order_by('?').all()[:number]
    fake = Faker('ko_KR')

    flogs = []
    for u in users:
        flogs.append(Post.objects.create(title=fake.sentence(),
                                         content=fake.sentence(), user=u))
    comments = []
    for f in choices(flogs, k=int(len(flogs) / 2)):
        comments.append(f.comments.create(user=choice(users),
                                          content=fake.word()))

    for c in choices(comments, k=int(len(comments) / 2)):
        Comment.objects.create(user=choice(users),
                               post=c.post,
                               comment=c,
                               content=fake.word())
