from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'position','is_identified')
    list_filter = (('position', admin.ChoicesFieldListFilter),)
    search_fields = ('first_name',)

admin.site.register(User, UserAdmin)
