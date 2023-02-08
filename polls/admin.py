from django.contrib import admin

# Register your models here.

from .models import Question, Choice, User

admin.site.site_header = "Polly Admin"
admin.site.site_title = "Polly Admin Area"
admin.site.index_title = "Welcome to the Polly Admin Area"
 
 
class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3
 
 
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question_text']}), ('Date Information', {
        'fields': ['pub_date'], 'classes': ['collapse']}), ]
    inlines = [ChoiceInLine]
 
admin.site.register(User)
admin.site.register(Question, QuestionAdmin)
