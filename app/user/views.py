"""
Views for the user API
"""
# from requests import Response
from .analytics.services import get_user_log_analytics
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

# from rest_framework.permissions import IsAuthenticated
# from user.analytics.services import get_user_log_analytics
# from rest_framework.views import APIView

from user.serializers import (
    UserLogAnalyticsSerializer,
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

#####################################
# TEXT ANALYTICS API


class UserLogAnalyticsView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserLogAnalyticsSerializer

    def get_object(self):
        return get_user_log_analytics(self.request.user)
