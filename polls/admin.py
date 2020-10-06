"""polls admin Configuration."""
from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Choice for admin."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Question for admin."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'end_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
