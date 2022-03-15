from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from auth_user.views import LogOutView, UserCreateView, UserDetailView, UserListView

urlpatterns = [
    path('register/', UserCreateView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
        # path('user/<int:pk>/update/', UserUpdate.as_view()),
        # path('user/<int:pk>/delete/', UserDelete.as_view()),
]