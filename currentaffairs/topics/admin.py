from django.contrib import admin
from .models import (
    Topic,
    TopicReadStatus,
    Poll,
    PollOption,
    PollVote,
    PollReadStatus,
)


# =========================
# Topics
# =========================

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'is_open',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'is_open',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
        'content',
        'author__email',
    )

    filter_horizontal = ('participants',)


@admin.register(TopicReadStatus)
class TopicReadStatusAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'topic',
        'last_read_at',
    )

    search_fields = (
        'user__email',
        'topic__title',
    )


# =========================
# Polls
# =========================

class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 1


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'short_question',
        'author',
        'is_open',
        'is_anonymous',
        'allow_multiple',
        'created_at',
    )

    list_filter = (
        'is_open',
        'is_anonymous',
        'allow_multiple',
        'created_at',
    )

    search_fields = (
        'question',
        'author__email',
    )

    filter_horizontal = ('participants',)
    inlines = [PollOptionInline]

    def short_question(self, obj):
        return obj.question[:60]

    short_question.short_description = 'Question'


@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'poll',
        'option',
        'user',
        'created_at',
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'poll__question',
        'user__email',
    )


@admin.register(PollReadStatus)
class PollReadStatusAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'poll',
        'last_read_at',
    )

    search_fields = (
        'user__email',
        'poll__question',
    )
