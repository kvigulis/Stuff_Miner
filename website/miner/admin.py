from django.contrib import admin
from .models import Filter, Condition, Keyword, Result

admin.site.register(Filter)
admin.site.register(Condition)
admin.site.register(Keyword)
admin.site.register(Result)