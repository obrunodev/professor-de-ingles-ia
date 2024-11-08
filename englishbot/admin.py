from django.contrib import admin
from englishbot.models import Student, Message, TeacherPrompt


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    ...


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    ...


@admin.register(TeacherPrompt)
class TeacherPromptAdmin(admin.ModelAdmin):
    ...
