from django.contrib import admin
from punchclock.models import ClockSession

@admin.register(ClockSession)
class ClockAdmin(admin.ModelAdmin):
	list_display = ['user', 'in_time', 'out_time', 'clocked_in']