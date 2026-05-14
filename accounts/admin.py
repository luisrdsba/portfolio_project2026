from django.contrib import admin
from .models import MagicLink


@admin.register(MagicLink)
class MagicLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'criado_em', 'usado')
    list_filter = ('usado',)
