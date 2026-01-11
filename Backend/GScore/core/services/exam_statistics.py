# services/exam_statistics.py
from collections import Counter
from django.db.models import F,FloatField, ExpressionWrapper
from utilities.choice import EXAM_BLOCKS
from utilities.choice import ScoreLevel
from core.models import StudentExamResult
from functools import reduce
from django.db.models.functions import Round
import operator


class ExamStatisticsService:

    def __init__(self, block="A00"):
        self.block = block
        self.subjects = EXAM_BLOCKS.get(block, [])

    def score_distribution(self):
        counter = Counter()

        qs = StudentExamResult.objects.all()

        for obj in qs:
            scores = [
                getattr(obj, s)
                for s in self.subjects
                if getattr(obj, s) is not None
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
        if not self.subjects:
            return []

        qs = StudentExamResult.objects.all()

        for subject in self.subjects:
            qs = qs.exclude(**{f"{subject}__isnull": True})

        total_expr = reduce(
            operator.add,
            [F(subject) for subject in self.subjects]
        )

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
                "scores": [getattr(obj, s) for s in self.subjects],  # 👈 thứ tự đúng
                "total": obj.total_score,
            })

        return result

        
    def subject_distributions(self):
        """
        Trả về thống kê cho từng môn trong tổ hợp
        """
        result = {}

        qs = StudentExamResult.objects.all()

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