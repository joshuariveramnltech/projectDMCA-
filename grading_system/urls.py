from django.urls import path
from . import views

app_name = 'grading_system'

urlpatterns = [
    path('faculty/assigned/subjects/',
         views.view_assigned_subject, name="view_assigned_subject"),
    path('faculty/view/students/per/subject/<int:level_section_id>/<int:subject_id>/',
         views.view_students_per_subject, name="view_students_per_subject"),
    path('faculty/view/student/profile/<int:user_id>/<short_name>/',
         views.view_student_profile, name='view_student_profile'),
    path('faculty/edit/student/subject-grade/<int:user_id>/<user_full_name>/<int:subject_grade_id>/',
         views.edit_student_subjectgrade, name='edit_student_subjectGrade'),
    path('faculty/view/student/final-grade/',
         views.view_students_finalgrade, name='view_students_finalgrade'),
    path('faculty/edit/student/final-grade/<int:user_id>/<int:level_id>/',
         views.edit_student_finalgrade, name='edit_student_finalgrade'),
    path('student/subject/<student_level>/<student_section>/',
         views.student_level_section_subject, name="student_level_section_subject"),
    path('student/view/faculty/profile/<int:user_id>/<short_name>/',
         views.view_faculty_profile, name='view_faculty_profile'),
    path('student/view/all/grades/',
         views.view_all_grades, name='view_all_grades'),
]
