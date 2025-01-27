from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.http import JsonResponse

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        try:
            auth_header = request.headers.get("Authoriization")
            if not auth_header:
                return JsonResponse({'error': 'No token provided'}, status=401)
            
            auth_result = self.jwt_authenticator.authenticate(request)
            if auth_result is None:
                return JsonResponse({"error": "Invalid Token"}, status=status.HTTP_401_UNAUTHORISED)
            
            user, token = auth_result
            request.user = user
            request.token = token
            print(user)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status.HTTP_401_UNAUTHORIZED)
        
        return self.get_response(request)

    