from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, StudentExamResult
from .serializers import  UserSerializer, StudentSerializer, LecturerSerializer, StudentExamResultSerializer


class UserViewSet(viewsets.ViewSet,
                  generics.ListAPIView,
                  generics.RetrieveAPIView):

    queryset = User.objects.filter(is_active=True)
    parser_classes = [
        parsers.MultiPartParser,
        parsers.FormParser,
        parsers.JSONParser
    ]

    def get_serializer_class(self):
        if self.action == "student_register":
            return StudentSerializer
        elif self.action == "lecturer_register":
            return LecturerSerializer
        return UserSerializer
    
    @action(methods=["post"],detail=False,url_path="student-register")
    def student_register(self,request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=["post"],detail=False,url_path="lecturer-register")
    def lecturer_register(self,request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StudentExamResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudentExamResult.objects.all()
    serializer_class = StudentExamResultSerializer
    permission_classes = [permissions.AllowAny]

    lookup_field = "registration_number"
    lookup_url_kwarg = "registration_number"