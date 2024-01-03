"""
URL configuration for clgmanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from page_handler.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login_page,name="login_page"),
    path('logout/',logoutpage,name="logoutpage"),
    path('studentDashboard/',studentDashboard,name="studentDashboard"),
    path('teacherDashboard/',teacherDashboard,name="teacherDashboard"),
    path('hodDashboard/',hodDashboard,name="hodDashboard"),
    path('principalDashboard/',principalDashboard,name="principaltDashboard"),
    path('hodDashboard/pastattendance/<str:DateSelected>/',HODPastAttendance,name="PastAttendance"),
    path('teacherDashboard/pastattendance/<str:DateSelected>/',TeacherPastAttendance,name="PastAttendance"),
    path('principalDashboard/pastattendance/<str:DateSelected>/',PrincipalPastattendance,name="PastAttendance"),
    path('librarySystem',librarybookadd,name="librarySystem"),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)