from django.forms.utils import mark_safe
from django.shortcuts import render, redirect
from django.db import transaction
import csv
from django.utils.html import format_html
from django.contrib import admin
from .models import User, StudentExamResult, Course
from admin.site import gscore_admin_site
from unfold.admin import ModelAdmin
from admin.components import action_button, option_display
from utilities.choice import UserType
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import path
from core.admin_views import views


class UserAdmin(ModelAdmin):
    """
    Trang quản lý người dùng
    """

    list_display = ["username", "is_active", "email", "user_type_display"]
    search_fields = ["username", "email"]
    list_filter = ["is_active", "date_joined"]
    sortable_by = ["username"]
    readonly_fields = ["avatar_view"]
    filter_horizontal = ["user_permissions"]

    fieldsets = [
        (
            "User profile",
            {"fields": ["is_active", "username", "email", "avatar_view"]},
        ),
        (
            "Permissions",
            {
                "description": "Config user permissions",
                "classes": ["collapse"],
                "fields": ["user_type", "user_permissions", "is_staff", "is_superuser"],
            },
        ),
    ]

    def avatar_view(self, user):
        if user:
            return mark_safe(f"<img src='{user.avatar.url}' width='200' />")

    def user_type_display(self, user: User):
        """Hiển thị loại tài khoản dưới dạng biểu tượng màu."""

        if user.is_superuser:
            return option_display("Admin", color="red")

        if user.user_type == UserType.LECTURER:
            return option_display("Lecturer", color="purple")

        if user.user_type == UserType.STUDENT:
            return option_display("Student", color="teal")

    user_type_display.short_description = "User Type"

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj == request.user:
            return False
        return super().has_delete_permission(request, obj)
    
class CourseAdmin(ModelAdmin):
    list_display = ['code', 'name', 'start_year', 'end_year']
    search_fields = ['code', 'name']
    list_filter = ['start_year', 'end_year']

    fieldsets = [
        (
            "Course Info",
            {"fields": ["code", "name", "start_year", "end_year"]}
        ),
    ]

class StudentExamResultAdmin(ModelAdmin):
    list_display = ['registration_number', 'course', 'math', 'literature', 'foreign_language']
    search_fields = ['registration_number']
    list_filter = ['course']
    readonly_fields = ['math', 'literature', 'foreign_language', 
                       'physics', 'chemistry', 'biology',
                       'history', 'geography', 'civic_education', 'foreign_language_code']

    def get_queryset(self, request):
        """Chỉ fetch khi có filter `course`"""
        qs = super().get_queryset(request)
        course_id = request.GET.get('course')
        if course_id:
            qs = qs.filter(course_id=course_id)
        return qs

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import-csv/',
                self.admin_site.admin_view(views.StudentExamUploadCSVAdminView.as_view()),
                name='core_studentexamresult_import',
            ),
            path(
                'statistics/', 
                self.admin_site.admin_view(views.StudentExamStatisticsAdminView.as_view()),
                name='core_studentexamresult_statistics',
            ),
        ]
        return custom_urls + urls

    def statistics_button(self, obj=None):
        return action_button("📊 Statistics", "statistics/", "blue")
    

gscore_admin_site.register(Course, CourseAdmin)
gscore_admin_site.register(User, UserAdmin)
gscore_admin_site.register(StudentExamResult, StudentExamResultAdmin)