from django.contrib import admin
from .models import Person, Volunteer, Contact, Cause, Donate, work, Event, EventImage
# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_per_page = 1000  # Set the number of persons per page

admin.site.register(Person, PersonAdmin)  # Register Person with custom admin
admin.site.register(Volunteer)
admin.site.register(Contact)
admin.site.register(Cause)
admin.site.register(Donate)
admin.site.register(work)



class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1  # Number of extra fields for images

class EventAdmin(admin.ModelAdmin):
    inlines = [EventImageInline]

admin.site.register(Event, EventAdmin)

