from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ads import views
from ads.views import CategoryListView, Ad, CategoryDetail, AdDetail, CategoryUpdate, CategoryDelete, AdsUpdate, \
    AdsDelete, AdsImageView, LocationViewSet, \
    AdCreateView, SelectionsListView, SelectionsDetailView, SelectionsCreateView, SelectionsUpdateView, \
    SelectionsDeleteView \
    #UserListView, UserDetailView, UserDelete, UserUpdate, UserCreateView,
from main_avito import settings

router = routers.SimpleRouter()
router.register(r'location', LocationViewSet)

urlpatterns = [
                  path('', views.get),
                  path('cat/', CategoryListView.as_view()),
                  path('ad/', Ad.as_view()),
                  path('ad/create/', AdCreateView.as_view()),
                  path('cat/<int:pk>/', CategoryDetail.as_view()),
                  path('cat/<int:pk>/update/', CategoryUpdate.as_view()),
                  path('cat/<int:pk>/delete/', CategoryDelete.as_view()),
                  path('ad/<int:pk>/', AdDetail.as_view()),
                  path('ad/<int:pk>/upload_image/', AdsImageView.as_view()),
                  path('ad/<int:pk>/update/', AdsUpdate.as_view()),
                  path('ad/<int:pk>/delete/', AdsDelete.as_view()),
                  # path('user/', UserListView.as_view()),
                  # path('user/create/', UserCreateView.as_view()),
                  # path('user/<int:pk>/', UserDetailView.as_view()),
                  # path('user/<int:pk>/update/', UserUpdate.as_view()),
                  # path('user/<int:pk>/delete/', UserDelete.as_view()),
                  path('selection/', SelectionsListView.as_view()),
                  path('selection/create/', SelectionsCreateView.as_view()),
                  path('selection/<int:pk>/', SelectionsDetailView.as_view()),
                  path('selection/<int:pk>/update/', SelectionsUpdateView.as_view()),
                  path('selection/<int:pk>/delete/', SelectionsDeleteView.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + router.urls


