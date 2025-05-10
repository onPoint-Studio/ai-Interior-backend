from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

def custom_exception_handler(exc, context):
    if isinstance(exc, (InvalidToken, TokenError, AuthenticationFailed)):
        return Response({'detail': 'UNAUTHORIZED'}, status=status.HTTP_401_UNAUTHORIZED)

    return exception_handler(exc, context)
