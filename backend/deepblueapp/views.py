from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH2_REDIRECT_URI
    client_class = OAuth2Client

@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    code = request.data.get('code')
    
    try:
        # Use the GoogleLogin view to handle the OAuth2 flow
        social_login_view = GoogleLogin.as_view()
        response = social_login_view(request._request)

        if response.status_code == 200:
            user = response.user
            
            # Check if the user is newly created
            is_new_user = user.date_joined == user.last_login

            # Update user info if needed
            if is_new_user:
                user.username = user.email.split('@')[0]  # Set username as part of email
                user.save()

            # Generate Django authentication token
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                'isExistingMember': not is_new_user,
                'token': token.key,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Login failed'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)





