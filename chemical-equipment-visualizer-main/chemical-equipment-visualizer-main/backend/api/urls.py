from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, health_check
from .auth_views import register, login, logout  # Add this

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health_check, name='health_check'),
    path('auth/register/', register, name='register'),  # Add
    path('auth/login/', login, name='login'),          # Add
    path('auth/logout/', logout, name='logout'),       # Add
]