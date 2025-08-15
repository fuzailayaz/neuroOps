from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .serializers import (
    UserSerializer, 
    RegisterSerializer, 
    CustomTokenObtainPairSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "message": "User created successfully."
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Registration error: {str(e)}")
            logger.error(f"Request data: {request.data}")
            logger.error(f"Errors: {getattr(serializer, 'errors', None)}")
            
            # Return detailed error message
            error_message = str(e)
            if hasattr(e, 'detail') and isinstance(e.detail, dict):
                error_message = ", ".join([f"{k}: {v[0]}" for k, v in e.detail.items()])
            elif hasattr(serializer, 'errors'):
                error_message = ", ".join([f"{k}: {v[0]}" for k, v in serializer.errors.items()])
                
            return Response({"detail": error_message}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
