from django.contrib import admin
from .models import Parish, Inspection, Question, GeneralComment

admin.site.register(Parish)
admin.site.register(Inspection)
admin.site.register(Question)
admin.site.register(GeneralComment)

