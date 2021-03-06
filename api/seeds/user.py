from django.db import transaction
from faker import Faker

from api.users.models import User


@transaction.atomic
def generate_data(number):
    fake = Faker('ko_KR')
    if not User.objects.filter(username='flatcoke').exists():
        User.objects.create(username='flatcoke', email='flatcoke89@gmail.com',
                            password='qwer1234', is_superuser=True,
                            is_staff=True)
    for i in range(number):
        User.objects.create(
            username=fake.user_name(),
            email=fake.email(),
            password='qwer1234',
        )
