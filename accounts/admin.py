from django.contrib import admin
from .models import Trial, CleaningRecord, ShiftMessage, ManagerMessage
from .models import CleaningTask


@admin.register(Trial)
class TrialAdmin(admin.ModelAdmin):
    list_display = ('name','trial_type','status','date','time','created_by')
    list_filter = ('trial_type','date','status')


@admin.register(CleaningRecord)
class CleaningAdmin(admin.ModelAdmin):
    list_display = ('date','arrived','left')


@admin.register(ShiftMessage)
class ShiftMessageAdmin(admin.ModelAdmin):
    list_display = ('date','author','updated_at')


@admin.register(ManagerMessage)
class ManagerMessageAdmin(admin.ModelAdmin):
    list_display = ('date','author','updated_at')


@admin.register(CleaningTask)
class CleaningTaskAdmin(admin.ModelAdmin):
    list_display = ('weekday','time','area','title','status')
    list_filter = ('weekday','status')
    search_fields = ('title','area','details')
