from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from unfold.admin import ModelAdmin
from .site import gscore_admin_site
from core.models import StudentExamResult
import csv

from core.models import StudentExamResult


class StudentExamResultAdmin(ModelAdmin):
    list_display = ['registration_number', 'math', 'literature', 'foreign_language']
    search_fields = ['registration_number']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', 
                 self.admin_site.admin_view(self.import_csv_view),
                 name='student_exam_import'),
        ]
        return custom_urls + urls
    
    def import_csv_view(self, request):
        if request.method == 'POST':
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
                            StudentExamResult.objects.bulk_create(
                                results, batch_size=BATCH_SIZE
                            )
                            results.clear()

                    if results:
                        StudentExamResult.objects.bulk_create(results)

                messages.success(request, "Import dữ liệu thành công 🎉")

            except Exception as e:
                messages.error(request, f"Lỗi import: {e}")

            return redirect(request.path)
        
        context = {
            **self.admin_site.each_context(request),
            'title': 'Import Student Exam Results',
            'opts': self.model._meta,
        }
        return render(request, 'admin/student_exam/upload_csv.html', context)


gscore_admin_site.register(StudentExamResult, StudentExamResultAdmin)