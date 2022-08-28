from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .serializers import UserSerializer, LoginSerializer
import jwt, datetime
from django.conf import settings
from rest_framework import status


# Create your views here.
class RegisterView(APIView):
    Serilizer_class = UserSerializer
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user:

            #Generate JWT for Authentication
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')

            serializer = UserSerializer(user)
            

            #Send token via cookies
            response=Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {'user': serializer.data, 'jwt':token}
            # response.data = {'jwt':token, 'user':user}
            return response

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

class LogoutView(APIView):
    def post(self, request):
        response=Response()
        response.delete_cookie('jwt')
        response.data = {'message':  'success'}
        return response