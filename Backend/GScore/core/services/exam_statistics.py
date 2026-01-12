# services/exam_statistics.py
from collections import Counter
from django.db.models import F,FloatField, ExpressionWrapper
from utilities.choice import EXAM_BLOCKS
from utilities.choice import ScoreLevel
from core.models import StudentExamResult
from functools import reduce
from django.db.models.functions import Round
import operator
from core.models import Course

from django import forms

class StudentExamCSVForm(forms.Form):
    file = forms.FileField(label="CSV file")
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        label="Select Course",
        help_text="Chọn khóa học cho dữ liệu CSV"
    )


class ExamStatisticsService:

    def __init__(self, block="A00", course=None):
        self.block = block
        self.course = course
        self.subjects = EXAM_BLOCKS.get(block, [])

    def get_queryset(self):
        """
        Chỉ trả về queryset cho course được chọn
        Nếu course chưa chọn hoặc không có record nào -> None
        """
        if not self.course:
            return None

        qs = StudentExamResult.objects.filter(course=self.course)

        # Không filter block nữa vì không tồn tại field block
        # if self.block:
        #     qs = qs.filter(block=self.block)

        if not qs.exists():
            return None

        return qs

    def score_distribution(self):
        """
        Thống kê phân phối điểm trung bình theo level
        """
        qs = self.get_queryset()
        if not qs:
            # Nếu không có dữ liệu trả về rỗng
            return {"labels": ScoreLevel.LEVELS,
                    "data": [0]*len(ScoreLevel.LEVELS),
                    "colors": ScoreLevel.COLORS}

        counter = Counter()
        for obj in qs:
            scores = [
                getattr(obj, s) for s in self.subjects if getattr(obj, s) is not None
            ]
            if len(scores) != len(self.subjects):
                continue
            avg_score = sum(scores) / len(scores)
            level = ScoreLevel.get(avg_score)
            counter[level] += 1

        return {
            "labels": ScoreLevel.LEVELS,
            "data": [counter.get(l, 0) for l in ScoreLevel.LEVELS],
            "colors": ScoreLevel.COLORS,
        }

    def top10_by_block(self):
        """
        Top 10 học sinh theo tổng điểm của khối
        """
        qs = self.get_queryset()
        if not qs or not self.subjects:
            return []

        for subject in self.subjects:
            qs = qs.exclude(**{f"{subject}__isnull": True})

        total_expr = reduce(operator.add, [F(subject) for subject in self.subjects])

        qs = (
            qs.annotate(
                total_score=Round(
                    ExpressionWrapper(total_expr, output_field=FloatField()),
                    precision=2
                )
            )
            .order_by("-total_score")[:10]
        )

        result = []
        for idx, obj in enumerate(qs, start=1):
            result.append({
                "rank": idx,
                "registration_number": obj.registration_number,
                "scores": [getattr(obj, s) for s in self.subjects],
                "total": obj.total_score,
            })

        return result

    def subject_distributions(self):
        """
        Thống kê phân phối điểm theo từng môn trong khối
        """
        qs = self.get_queryset()
        result = {}

        if not qs:
            # Nếu không có dữ liệu -> mỗi môn trả về 0
            for subject in self.subjects:
                result[subject] = {
                    "labels": ScoreLevel.LEVELS,
                    "data": [0]*len(ScoreLevel.LEVELS),
                    "colors": ScoreLevel.COLORS
                }
            return result

        for subject in self.subjects:
            counter = Counter()
            for obj in qs:
                score = getattr(obj, subject, None)
                if score is None:
                    continue
                level = ScoreLevel.get(score)
                counter[level] += 1

            result[subject] = {
                "labels": ScoreLevel.LEVELS,
                "data": [counter.get(l, 0) for l in ScoreLevel.LEVELS],
                "colors": ScoreLevel.COLORS,
            }

        return result
