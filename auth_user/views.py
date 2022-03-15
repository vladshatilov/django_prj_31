from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from auth_user.serializers import UserCreateSerializer, UserSerializer, UserSimpleSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSimpleSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.user.id)
        # try:
        refresh_token = request.data['refresh_token']
        print(refresh_token)
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
        # except Exception:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
