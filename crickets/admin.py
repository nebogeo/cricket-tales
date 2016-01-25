from django.contrib import admin
from crickets.models import *

# Register your models here.
#admin.site.register(Cricket)
#admin.site.register(Personality)
admin.site.register(Movie)

# prevent creating a drop down box with millions of items
class EventAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('movie', 'timestamp')
        return self.readonly_fields
admin.site.register(Event, EventAdmin)

admin.site.register(EventType)
admin.site.register(UserProfile)
admin.site.register(Burrow)
admin.site.register(PlayerBurrowScore)
