from django.contrib import admin

from .models import Entry


class EntryAdmin(admin.ModelAdmin):
    list_display = ( 
        'id', 'actor_user', 'verb_type', 'object_type', 'target_type',
        'title', 'tags', 'published', 'modified', 
    )

admin.site.register(Entry, EntryAdmin)
