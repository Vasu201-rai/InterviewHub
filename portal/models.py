from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    CATEGORY_CHOICES = [
        ('Python', 'Python'),
        ('SQL', 'SQL'),
        ('Django', 'Django'),
        ('Web', 'Web Development'),
        ('React', 'React'),
        ('JavaScript', 'JavaScript'),
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
    ]

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    title = models.CharField(max_length=255)

    answer = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Bookmark(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'question']

    def __str__(self):
        return f"{self.user.username} - {self.question.title}"