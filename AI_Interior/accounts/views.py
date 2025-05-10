from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .authentication import CustomJWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class RegisterView(APIView):
    @swagger_auto_schema(
        operation_description="Реєстрація",
        request_body=RegisterSerializer
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response()
        response.data = {
            'data': access_token
        }
        return response

class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="Авторизація",
        request_body=LoginSerializer
    )
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise ValidationError({ 'detail': 'INVALID_CREDENTIALS'})

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response()
        
        response.data = {
            'data': access_token
        }
        return response

class UserView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Отримання даних користувача через JWT (Authorization: Bearer)",
        security=[{'Bearer': []}],
        responses={200: UserSerializer()}
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

