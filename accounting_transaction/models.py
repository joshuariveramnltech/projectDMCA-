from django.db import models
from account.models import StudentProfile
from grading_system.models import GeneralSchoolYear
from grading_system.models import SY
# Create your models here.


class Statement(models.Model):
    current_school_year = GeneralSchoolYear.objects.get(id=1)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    school_year = models.CharField(
        max_length=25, choices=SY, default=str(current_school_year))
    break_down = models.TextField(null=True, blank=True)
    assessment = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Assessment (Php)")
    payment = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Payment (Php)")
    balance = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Balance (Php)")
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.student.user.get_full_name + " " + self.school_year
