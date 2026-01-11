from django.views import View
from django.shortcuts import render
from core.models import StudentExamResult
from admin.site import gscore_admin_site
from utilities.choice import EXAM_BLOCKS
from ..services.exam_statistics import ExamStatisticsService
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

        service = ExamStatisticsService(block=block)

        context = {
            **gscore_admin_site.each_context(request),
            "title": "Exam Statistics",
            "exam_blocks": EXAM_BLOCKS,
            "selected_block": block,
            "chart": service.score_distribution(),
            "top10": service.top10_by_block(),
            "subject_charts": service.subject_distributions(), 
            "subjects": service.subjects,  
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
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Xử lý upload CSV"""
        file = request.FILES.get("file")

        if not file:
            messages.error(request, "Vui lòng chọn file CSV")
            return redirect(request.path)

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

            messages.success(request, "Data import successfuly")

        except Exception as e:
            messages.error(request, f"Import error: {e}")

        return redirect(request.path)