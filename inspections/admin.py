from django.contrib import admin
from .models import Parish, Inspection, Question, InspectionQuestion, InspectionImage


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'is_default')


@admin.register(InspectionImage)
class InspectionImageAdmin(admin.ModelAdmin):
    list_display = ('inspection', 'image', 'uploaded_at')


admin.site.register(Parish)
admin.site.register(Inspection)
admin.site.register(InspectionQuestion)
