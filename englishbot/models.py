from core.models import BaseModel
from django.db import models


class Student(BaseModel):
    telegram_username = models.CharField('username do Telegram', max_length=100)
    name = models.CharField('Nome do estudante', max_length=255)

    class Meta:
        verbose_name = 'Estudante'
        verbose_name_plural = 'Estudantes'
    
    def __str__(self):
        return self.name


class Message(BaseModel):

    class RoleChoices(models.TextChoices):
        USER = 'user', 'Usuário'
        ASSISTANT = 'assistant', 'IA'

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    role = models.CharField('Quem mandou a mensagem', max_length=10, choices=RoleChoices.choices)
    content = models.TextField('Conteúdo da mensagem')

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
    
    def __str__(self):
        return '%s: (%s) -> %s' % (
            self.student.name,
            self.role,
            self.content[:50] + '...'
        )


class TeacherPrompt(BaseModel):
    content = models.TextField('Conteúdo')

    class Meta:
        verbose_name = 'Prompt do professor'
        verbose_name_plural = 'Prompts do professor'
    
    def __str__(self):
        return self.content[:50]
