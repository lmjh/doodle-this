from django.contrib import admin
from .models import Activity, Adjective, Creature, Location


class ActivityAdmin(admin.ModelAdmin):
    list_display: (
        'activity',
    )


class AdjectiveAdmin(admin.ModelAdmin):
    list_display: (
        'determiner',
        'adjective',
    )


class CreatureAdmin(admin.ModelAdmin):
    list_display: (
        'determiner',
        'creature',
        'plural',
    )


class LocationAdmin(admin.ModelAdmin):
    list_display: (
        'location',
    )


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Adjective, AdjectiveAdmin)
admin.site.register(Creature, CreatureAdmin)
admin.site.register(Location, LocationAdmin)