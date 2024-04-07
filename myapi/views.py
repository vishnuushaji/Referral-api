from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import User
from rest_framework import pagination

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        name = serializer.validated_data.get('name')
        referral_code = serializer.validated_data.get('referral_code') 

        user = User.objects.create_user(email=email, password=password, name=name, referral_code=referral_code, is_active=True)
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_201_CREATED)



class UserDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def get_object(self):
        return self.request.user




class CustomPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ReferralsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        user = request.user
        referral_code = user.referral_code
        referred_users = User.objects.filter(referral_code=referral_code)

        # Paginate the list of referred users
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(referred_users, request)
        serializer = UserSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
