from django.contrib import admin
from .models import Board, Thread, Post

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'description')
    search_fields = ('name', 'abbreviation')

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('subject', 'board', 'is_pinned', 'is_locked')
    list_filter = ('board', 'is_pinned', 'is_locked')
    search_fields = ('subject',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'subject', 'thread', 'created_at')
    list_filter = ('thread__board', 'created_at')
    search_fields = ('author', 'subject', 'message')
