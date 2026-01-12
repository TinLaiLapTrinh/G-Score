from django.views import View
from django.shortcuts import render
from core.models import StudentExamResult, Course
from admin.site import gscore_admin_site
from utilities.choice import EXAM_BLOCKS
from ..services.exam_statistics import ExamStatisticsService, StudentExamCSVForm
from django.contrib import messages
from django.urls import path
from django.shortcuts import render, redirect
from django.db import transaction
import csv

class StudentExamStatisticsAdminView(View):
    template_name = "admin/student_exam/statistics.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = StudentExamResult

    def get(self, request):
        block = request.GET.get("block", "A00")
        course_id = request.GET.get("course")  # Lấy course từ query string
        course = None

        top10 = []
        chart = {}
        subject_charts = {}
        subjects = []

        if course_id:
            try:
                course = Course.objects.get(id=course_id)

                # Chỉ fetch dữ liệu khi có course
                service = ExamStatisticsService(block=block, course=course)
                top10 = service.top10_by_block()
                chart = service.score_distribution()
                subject_charts = service.subject_distributions()
                subjects = service.subjects

            except Course.DoesNotExist:
                messages.warning(request, "Khóa học không tồn tại")

        context = {
            **gscore_admin_site.each_context(request),
            "title": "Exam Statistics",
            "exam_blocks": EXAM_BLOCKS,
            "selected_block": block,
            "courses": Course.objects.all(),  # dropdown
            "selected_course": course,
            "top10": top10,
            "chart": chart,
            "subject_charts": subject_charts,
            "subjects": subjects,
            "opts": self.model._meta,
        }

        return render(request, self.template_name, context)

class StudentExamUploadCSVAdminView(View):
    template_name = "admin/student_exam/upload_csv.html"

    def get(self, request):
        """Hiển thị form upload CSV"""
        context = {
            **gscore_admin_site.each_context(request),
            "title": "Import Student Exam Results",
            "opts": StudentExamResult._meta,
            "form": StudentExamCSVForm(),
            "courses": Course.objects.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Xử lý upload CSV"""
        form = StudentExamCSVForm(request.POST, request.FILES)

        if not form.is_valid():
            messages.error(request, "Vui lòng chọn file CSV và khóa học")
            return redirect(request.path)

        file = form.cleaned_data["file"]
        course = form.cleaned_data["course"]

        if not file.name.endswith(".csv"):
            messages.error(request, "Chỉ hỗ trợ file CSV")
            return redirect(request.path)

        results = []
        BATCH_SIZE = 1000

        try:
            decoded = file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded)

            with transaction.atomic():
                for row in reader:
                    results.append(
                        StudentExamResult(
                            registration_number=row["sbd"],
                            course=course,  # Gán khóa học vào đây
                            math=row.get("toan") or None,
                            literature=row.get("ngu_van") or None,
                            foreign_language=row.get("ngoai_ngu") or None,
                            physics=row.get("vat_li") or None,
                            chemistry=row.get("hoa_hoc") or None,
                            biology=row.get("sinh_hoc") or None,
                            history=row.get("lich_su") or None,
                            geography=row.get("dia_li") or None,
                            civic_education=row.get("gdcd") or None,
                            foreign_language_code=row.get("ma_ngoai_ngu"),
                        )
                    )

                    if len(results) >= BATCH_SIZE:
                        StudentExamResult.objects.bulk_create(results)
                        results.clear()

                if results:
                    StudentExamResult.objects.bulk_create(results)

            messages.success(request, f"Data imported successfully for course {course.code}")

        except Exception as e:
            messages.error(request, f"Import error: {e}")

        return redirect(request.path)