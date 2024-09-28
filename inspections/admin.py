from django.contrib import admin
from .models import Parish, Inspection, Question, GeneralComment


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'response')


class InspectionAdmin(admin.ModelAdmin):
    list_display = ('parish', 'created_at', 'updated_at')


admin.site.register(Parish)
admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(GeneralComment)
