from rest_framework.test import APITestCase as BaseAPITestCase
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def generate_jwt_token_by_user(user):
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


class APITestCase(BaseAPITestCase):
    @staticmethod
    def header_with_jwt_token(user, header=None):
        if header is None:
            header = {}
        token = generate_jwt_token_by_user(user)
        header['HTTP_AUTHORIZATION'] = 'JWT ' + token
        return header
