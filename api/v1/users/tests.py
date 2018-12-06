from django.db.utils import IntegrityError
from faker import Faker
from rest_framework.test import APITestCase

from .models import User

fake = Faker('ko_KR')


class UserTest(APITestCase):
    @staticmethod
    def create_user_directly(username, email, password):
        return User.objects.create(username=username,
                                   email=email, password=password)

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
            self.assertEqual(result.status_code, 201)

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
            self.assertEqual(result.status_code, 400)
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

    def test_blank_username(self):
        try:
            _ = User.objects.create(email=fake.email(), username=None,
                                    password=fake.password())
            raise Exception('Username can not be null')
        except IntegrityError:
            pass

    def test_blank_email(self):
        try:
            _ = User.objects.create(email=None, username=fake.user_name(),
                                    password=fake.password())
            raise Exception('Email can not be null')
        except IntegrityError:
            pass

    def test_validate_short_password(self):
        pass

    def test_login(self):
        pass

    def test_update_jwt_token_on_client_side(self):
        pass

    def test_re_generate_token_by_refresh_token(self):
        pass

    def test_login(self):
        pass

    def test_validate_jwt_token_after_login(self):
        pass

    def test_login_not_match_password(self):
        pass

    def test_login_not_found_email(self):
        pass

    def test_login_not_found_username(self):
        pass

    def test_update_profile_with_token(self):
        pass

    def test_update_profile_with_invalid_token(self):
        pass

    def test_update_profile_without_token(self):
        pass

    def test_delete_user_with_token(self):
        pass

    def test_delete_user_with_invalid_token(self):
        pass

    def test_delete_user_without_token(self):
        pass

    def test_soft_delete_user(self):
        pass
