from django.db.utils import IntegrityError
from rest_framework import status
from faker import Faker
from api.common.tests import generate_jwt_token_by_user, APITestCase

from .models import User

fake = Faker('ko_KR')


class UserTest(APITestCase):
    @staticmethod
    def create_user_directly(username, email, password):
        return User.objects.create(username=username,
                                   email=email, password=password)

    @classmethod
    def create_flatcoke(cls):
        return cls.create_user_directly('flatcoke', 'flatcoke@test.com',
                                        'qwer1234')

    @staticmethod
    def create_user_like_by_facebook_token():
        return User.objects.create(username='TaeminKim',
                                   email='flatcoke@test.com',
                                   provider='facebook',
                                   uid=fake.random.randrange(1, 999999),
                                   password=User.objects.make_random_password())

    @staticmethod
    def create_user_like_by_google_token():
        return User.objects.create(username='TaeminKim',
                                   email='flatcoke@gmail.com',
                                   provider='google',
                                   uid=fake.random.randrange(1, 999999),
                                   password=User.objects.make_random_password())

    def post_user(self, username, email, password):
        return self.client.post('/api/v1/users/', {'username': username,
                                                   'email': email,
                                                   'password': password
                                                   })

    def test_to_be_set_hash_password_by_hook(self):
        password = 'qwer1234'
        user = self.create_user_directly(username='flatcoke',
                                         email='flatcoke89@gmail.com',
                                         password=password)
        self.assertNotEqual(user.password, password,
                            'after save password hook not works')

    def test_create_user_success(self):
        cases = [
            {
                'username': 'flatcoke',
                'email': 'flatcoke@gmail.com',
                'password': 'asda33fqw!er'
            }, {
                'username': 'c121213',
                'email': 'c121213@gmail.com',
                'password': 'as#d_fqwer'
            }, {
                'username': 'flat',
                'email': 'flat@gmail.com',
                'password': 'qwer1234qwer'
            }, {
                'username': 'coke',
                'email': 'flatoke@nate.com',
                'password': 'asdfqsdfg$$wer'
            },
        ]
        for data in cases:
            result = self.post_user(**data)
            self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_email(self):
        cases = [
            'aa@bbcom',
            'aabbcom.com',
            '@aabbcom.',
            'b@aabbcom.a',
        ]
        for i in cases:
            username = fake.user_name()
            password = fake.password()
            result = self.post_user(username=username, email=i,
                                    password=password)
            self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
            email_field = result.json().get('email')
            self.assertIsNotNone(email_field)

    def test_validate_unique_email(self):
        email = 'iam@flatcoke.com'
        password = fake.password()
        username = fake.user_name()
        self.post_user(username=username, email=email,
                       password=password)  # success
        for i in range(2):
            username = fake.user_name()
            result = self.post_user(username=username, email=email,
                                    password=password)
            self.assertIsNotNone(result.json().get('email'))
            self.assertIn('Already exists email', result.json().get('email'))

    def test_validate_unique_username(self):
        username = 'flatcoke'
        password = fake.password()
        email = fake.email()
        self.post_user(username=username, email=email,
                       password=password)  # success
        for i in range(2):
            email = fake.email()
            result = self.post_user(username=username, email=email,
                                    password=password)
            self.assertIsNotNone(result.json().get('username'))
            self.assertIn('Already exists username',
                          result.json().get('username'))

    def test_validate_unique_username_after_soft_delete(self):
        username = 'flatcoke'
        password = fake.password()
        email = fake.email()
        user = self.create_user_directly(username=username, email=email,
                                         password=password)  # success
        user.delete()
        self.assertIsNotNone(user.deleted_at)

        email = fake.email()
        result = self.post_user(username=username, email=email,
                                password=password)
        self.assertIsNotNone(result.json().get('username'))
        self.assertIn('Already exists username',
                      result.json().get('username'))

    def test_validate_unique_email_after_soft_delete(self):
        email = 'flatcoke@gmail.com'
        password = fake.password()
        username = fake.user_name()
        user = self.create_user_directly(username=username, email=email,
                                         password=password)  # success
        user.delete()
        self.assertIsNotNone(user.deleted_at)

        username = fake.user_name()
        result = self.post_user(username=username, email=email,
                                password=password)
        self.assertIsNotNone(result.json().get('email'))
        self.assertIn('Already exists email',
                      result.json().get('email'))

    def test_create_user_with_blank_username(self):
        try:
            _ = User.objects.create(email=fake.email(), username=None,
                                    password=fake.password())
            raise Exception('Username can not be null')
        except IntegrityError:
            pass

    def test_create_user_with_blank_email(self):
        try:
            _ = User.objects.create(email=None, username=fake.user_name(),
                                    password=fake.password())
            raise Exception('Email can not be null')
        except IntegrityError:
            pass

    def test_validate_short_password(self):
        pass

    def test_jwt_token_and_update_username_by_the_token(self):
        user = self.create_flatcoke()
        res = self.client.post('/api/auth/token/',
                               {'email': user.email,
                                'password': 'qwer1234'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        json_data = res.json()
        self.assertIn('token', json_data)
        token = json_data['token']

        user_id = User.objects.filter(email=user.email) \
            .values_list('id', flat=True).first()
        headers = {'HTTP_AUTHORIZATION': 'JWT ' + token}

        will_be_this = 'Taemin'
        self.client.patch('/api/v1/users/1/',
                          {'username': will_be_this}, **headers)
        username_after_patching = User.objects. \
            values_list('username', flat=True).get(pk=user_id)
        self.assertEqual(username_after_patching, will_be_this)

    def test_jwt_refresh_token_and_update_username_by_the_token(self):
        user = self.create_flatcoke()
        token = generate_jwt_token_by_user(user)

        res = self.client.post('/api/auth/token/refresh/', {'token': token})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        token = res.json()['token']

        user_id = User.objects.filter(email=user.email) \
            .values_list('id', flat=True).first()
        headers = {'HTTP_AUTHORIZATION': 'JWT ' + token}

        will_be_this = 'Taemin'
        self.client.patch('/api/v1/users/1/',
                          {'username': will_be_this}, **headers)
        username_after_patching = User.objects. \
            values_list('username', flat=True).get(pk=user_id)
        self.assertEqual(username_after_patching, will_be_this)

    def update_username_for_token(self, user, token):
        user_id = User.objects.filter(email=user.email) \
            .values_list('id', flat=True).first()
        headers = {'HTTP_AUTHORIZATION': 'JWT ' + token}

        will_be_this = 'Taemin'
        self.client.patch('/api/v1/users/1/',
                          {'username': will_be_this}, **headers)
        username_after_patching = User.objects. \
            values_list('username', flat=True).get(pk=user_id)
        return username_after_patching == will_be_this

    def test_get_jwt_token_with_not_matched_password(self):
        user = self.create_flatcoke()
        res = self.client.post('/api/auth/token/',
                               {'email': user.email,
                                'password': 'this_is_not_valid_password'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_username_with_invalid_token_and_without_token(self):
        user = self.create_flatcoke()
        token = 'this.is.not_valid_token'
        user_id = User.objects.filter(email=user.email) \
            .values_list('id', flat=True).first()
        headers = {'HTTP_AUTHORIZATION': 'JWT ' + token}

        wont_be_this = 'Taemin'
        res = self.client.patch('/api/v1/users/1/',
                          {'username': wont_be_this}, **headers)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        username_after_patching = User.objects. \
            values_list('username', flat=True).get(pk=user_id)
        self.assertNotEqual(username_after_patching, wont_be_this)

        res = self.client.patch('/api/v1/users/1/',
                                {'username': wont_be_this})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        username_after_patching = User.objects. \
            values_list('username', flat=True).get(pk=user_id)
        self.assertNotEqual(username_after_patching, wont_be_this)

    def test_soft_delete_user(self):
        user = self.create_flatcoke()
        another_user = self.create_user_directly('aa', 'bb@cc.com', 'qwer1234')
        headers = self.header_with_jwt_token(another_user)

        # Try to delete user using another user token
        res = self.client.delete('/api/v1/users/%s/' % user.id, {}, **headers)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        headers = self.header_with_jwt_token(user)
        res = self.client.delete('/api/v1/users/%s/' % user.id, {}, **headers)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        self.assertIsNone(User.objects.filter(email=user.email).first())
        self.assertIsNotNone(User.with_deleted.filter(email=user.email).first())
