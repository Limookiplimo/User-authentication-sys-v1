import jwt
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from rest_framework.response import Response
from users.models import User
from .serializers import UserSerializer

class JWTAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None
        
        prefix, token = auth_data.decode('utf-8').split(' ')

        try:
            payload=jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])

            user=User.objects.filter(id=payload['id']).first()
            serializer=UserSerializer(user)
            return Response (serializer.data)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Login token is expired')

        except jwt.DecodeError:
            raise AuthenticationFailed('Login token is invalid')


        # return super().authenticate(request)