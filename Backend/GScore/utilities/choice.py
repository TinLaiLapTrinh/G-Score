from django.db import models

class UserType(models.TextChoices):
    """
    Loại người dùng
    """
    ADMIN = "Admin", "Quản trị viên"
    LECTURER = "Lecturer", "Giảng viên"
    STUDENT = "Student", "Học sinh"
    
EXAM_BLOCKS = {
    "A00": ["math", "physics", "chemistry"],
    "A01": ["math", "physics", "foreign_language"],
    "B00": ["math", "chemistry", "biology"],
    "C00": ["literature", "history", "geography"],
    "D01": ["math", "literature", "foreign_language"],
}

class ScoreLevel:
    LEVELS = [">=8", "6-8", "4-6", "<4"]
    COLORS = ["#2ecc71", "#3498db", "#f1c40f", "#e74c3c"]

    @staticmethod
    def get(score):
        if score is None:
            return None
        if score >= 8:
            return ">=8"
        if score >= 6:
            return "6-8"
        if score >= 4:
            return "4-6"
        return "<4"