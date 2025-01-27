from rest_framework import authentication
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import AccessToken


class MicroserviceUser:
    def __init__(self, user_id):
        self.id = user_id
        self.is_authenticated = True
        self._is_anonymous = False
        self.is_active = True

    @property
    def is_anonymous(self):
        return self._is_anonymous

    def __str__(self):
        return f"MicroserviceUser: {self.id}"


class MicroserviceAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return None
            
        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ', 1)[1]
        
        try:
            decoded_token = AccessToken(token)
            user_id = decoded_token.payload.get('user_id')
            
            if not user_id:
                raise exceptions.AuthenticationFailed('No user ID in token')
                
            user = MicroserviceUser(user_id)
            return (user, None)
            
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))