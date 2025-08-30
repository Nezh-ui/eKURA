from django.contrib import admin

class VoterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'registered_on')
    search_fields = ('name', 'email')
    list_filter = ('registered_on',)

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'election', 'position')
    search_fields = ('name',)
    list_filter = ('election', 'position')
