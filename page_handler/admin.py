from django.contrib import admin

from page_handler.models import *
# Register your models here.
admin.site.register(HOD_model)
admin.site.register(teacher_model)
admin.site.register(student_model)
admin.site.register(course_model)
admin.site.register(announcement_model)
admin.site.register(student_attendance_model)
admin.site.register(book_model)
admin.site.register(book_issue_model)
admin.site.register(HOD_picture)
admin.site.register(Teacher_picture)
admin.site.register(Student_picture)
