from django.contrib import admin

# Register your models here.
from .models import Activity, Grade, Subject, Device, Profile, Software, Concept


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'subject', 'grade', 'approved')


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Device)
admin.site.register(Profile)
admin.site.register(Software)
admin.site.register(Concept)
