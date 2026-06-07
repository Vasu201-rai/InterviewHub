from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Question

class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        fields = ('id', 'title', 'answer', 'category', 'user')

class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource

admin.site.register(Question, QuestionAdmin)