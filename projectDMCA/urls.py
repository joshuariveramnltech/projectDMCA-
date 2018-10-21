"""projectDMCA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'DMCA Administration'
admin.site.index_title = 'DMCA Administration'
admin.site.site_title = 'Admin Site'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls', namespace='account')),
    # login, logout and password_reset form
    path('account/', include('django.contrib.auth.urls')),
    path('administrator/', include('administrator.urls', namespace='administrator')),
    path('announcement/', include('announcement.urls', namespace='announcement')),
    path('academic/', include('grading_system.urls', namespace='grading_system')),
    path('accounting/transaction/', include('accounting_transaction.urls',
                                            namespace='accounting_transaction')),
    path('', include('admission.urls', namespace='admission')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
