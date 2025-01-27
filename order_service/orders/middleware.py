from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import  AccessToken
from django.http import JsonResponse

class CustomUser:
    def __init__(self, user_id):
        self.id = user_id
        self.is_authenticated = True
        self.is_active = True

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        try:
            auth_header = request.headers.get("Authorization")
            print(f"Auth header received: {auth_header}")
            if not auth_header:
                return JsonResponse({'error': 'No token provided'}, status=401)

            if not auth_header.startswith('Bearer'):
                return JsonResponse({'error': 'Invalid token format. Must start with "Bearer"'}, status=401)
            
            token = auth_header.split()[1]

            request.META['HTTP_AUTHORIZATION'] = f"Bearer {token}"
            
            try:
                decoded_token = AccessToken(token)
                # print(f"Token payload: {decoded_token}")
                user_id = decoded_token.payload.get('user_id')
                print(f"ID from token {user_id}")

                request.user = CustomUser(user_id)
                request.token = token
                request.payload = decoded_token.payload
                
                print(request.user.id)
                response = self.get_response(request)
                if response.status_code == 401:
                    try:
                        print(f"Response content: {response.content}")
                    except Exception as e:
                        print(f"Could not print response content: {e}")
                
                return response
            
            except Exception as e:
                print(f"Token decoded error {str(e)}")
                return JsonResponse({"error":f"Token decoded error {str(e)}"}, status=401)

            # try:
            #     auth_result = self.jwt_authenticator.authenticate(request)
            #     print(f"Auth result: {auth_result}")
            #     if auth_result is None:
            #             # return JsonResponse({
            #             #     'error': 'Authentication failed',
            #             #     'detail': 'Could not authenticate with provided token'
            #             # }, status=401)
            #         request.user = CustomUser(user_id)
            #         request.token = token
            #     else:
            #         user, token = auth_result
            #         request.user = user
            #         request.token = token
            #         print(user)
            #     # request.user_info = validated_data
            #     return self.get_response(request)
            
            # except Exception as auth_error:
            #     print(f"Authentication error: {str(auth_error)}")
            #     print(f"Authentication traceback: {traceback.format_exc()}")
            #     return JsonResponse({
            #         'error': 'Authentication process failed',
            #         'detail': str(auth_error)
            #     }, status=401)
        
        except Exception as e:
            return JsonResponse({'error': "Error coming from final try"}, status=401)
        

    