from django.urls import path
from . import views
# Create your url patterns here

app_name = "accounting_transaction"

urlpatterns = [
    path('view/list/', views.view_user_list, name='view_user_list'),
    path('view/statement/<user_full_name>/<int:user_id>/',
         views.view_statement, name='view_statement'),
    path('delete/statement/<int:statement_id>/<student_full_name>/<int:student_id>/',
         views.delete_statement, name='delete_statement'),
    path('update/statement/<int:statement_id>/<student_full_name>/<int:student_id>/',
         views.update_statement, name='update_statement'),
    path('view/account-statement/',
         views.student_view_statement, name='student_view_statement'),
]
