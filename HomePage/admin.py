from django.contrib import admin
from .models import Question, Choice

admin.site.site_header = "StockMarket Admin"
admin.site.site_title = "StockMarket Admin Area"
admin.site.index_title = "Welcome to the StockMarket admin area"


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

# admin.site.register(Question)
# admin.site.register(Choice)


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['questions_text']}),
                 ('Date Information', {'fields': ['pub_date'], 'classes':['collapse']}), ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
