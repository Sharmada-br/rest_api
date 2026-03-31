from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer


# 🟢 Register API
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Registered Successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🟢 Login API
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data

            token = RefreshToken.for_user(user)

            return Response({
                "refresh": str(token),
                "access": str(token.access_token)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🟢 Profile API (GET only)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)


# 🟢 User Detail API (GET, PATCH, DELETE)
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # 🔹 GET → View user
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    # 🔹 PATCH → Update user
    def patch(self, request):
        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Updated Successfully"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 DELETE → Delete user
    def delete(self, request):
        request.user.delete()
        return Response(
            {"msg": "User Deleted Successfully"},
            status=status.HTTP_200_OK
        )