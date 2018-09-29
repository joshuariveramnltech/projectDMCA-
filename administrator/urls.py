from django.urls import path
from . import views
# Create your forms here


app_name = 'administrator'

urlpatterns = [
    path('dmca/create/user/', views.create_user, name='create_user'),
    path('dmca/create/user/done/', views.create_user_done, name='create_user_done'),
    path('dmca/view/users/', views.view_users, name='view_users'),
    path('dmca/delete/user/<int:user_id>/',
         views.delete_user, name='delete_user'),
    path('dmca/edit/user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('dmca/edit/level/section/<int:level_section_id>',
         views.edit_level_section, name='edit_level_section'),
    path('dmca/view/level/section/',
         views.view_level_section, name='view_level_section'),
    path('dmca/delete/level/section/<int:level_section_id>',
         views.delete_level_section, name='delete_level_section'),
    path('dmca/create/subject/<int:user_id>/',
         views.create_subject, name='create_subject'),
    path('dmca/edit/subject/<slug:subject_slug>/<int:user_id>/',
         views.edit_subject, name='edit_subject'),
    path('dmca/delete/subject/<slug:subject_slug>/<int:user_id>/',
         views.delete_subject, name='delete_subject'),
    path('dmca/enroll/subject/<int:user_id>/<user_full_name>/',
         views.enrollment_admission_student, name='enrollment_admission'),
    path('dmca/delete/subject/grade/<int:user_id>/<user_full_name>/<int:subject_grade_id>/',
         views.delete_subject_grade, name='delete_subject_grade'),
    path('dmca/edit/subject/grade/<int:user_id>/<user_full_name>/<int:subject_grade_id>/',
         views.edit_subjectGrade_admin, name='edit_subjectGrade_admin'),
    path('dmca/create/final/grade/',
         views.create_student_finalLevelGradeAdmin, name='create_student_finalLevelGradeAdmin'),
    path('dmca/edit/final/grade/<int:final_grade_id>/<user_full_name>/',
         views.edit_student_finalLevelGradeAdmin, name='edit_student_finalLevelGradeAdmin'),
    path('dmca/delete/grade/<int:final_grade_id>/<user_full_name>/',
         views.delete_student_finalLevelGradeAdmin, name='delete_student_finalLevelGradeAdmin'),
]
