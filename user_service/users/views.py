from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import User, UserSerializer
import json
# Create your views here.


class UserRegistrationView(APIView):
    psermission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TokenValidationView(APIView):
    def post(self, request):
        token = request.data.get("token")
        try:
            decoded_token = AccessToken(token)
            user_id = decoded_token.payload.get("user_id")
            user = User.objects.get(id=user_id)
            print(json.dumps(user)) 

            return Response(
                {"valid": True,
                "user": {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_active': user.is_active
                }}
            )  
        except Exception as e:
            return Response({
                "valid": False,
                "detail": str(e)},
                status=401
            )
