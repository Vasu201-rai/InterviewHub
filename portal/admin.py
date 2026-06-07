from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth.models import User
from .models import Question

class QuestionResource(resources.ModelResource):
    
    user = Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = Question
        fields = ('id', 'title', 'answer', 'category', 'user')

    def before_import_row(self, row, **kwargs):
        row['user'] = User.objects.filter(is_superuser=True).first().username

class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource

admin.site.register(Question, QuestionAdmin)