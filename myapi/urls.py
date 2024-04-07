from django.urls import path
from .views import UserViewSet, UserDetailsAPIView, ReferralsAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('user-details/', UserDetailsAPIView.as_view(), name='user-details'),
    path('referrals/', ReferralsAPIView.as_view(), name='referrals'),
]

urlpatterns += router.urls
