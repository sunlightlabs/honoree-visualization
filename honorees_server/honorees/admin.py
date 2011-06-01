from django.contrib import admin

from honorees.models import *

class ContributionHonoreeInline(admin.TabularInline):
    model = ContributionHonoree
    extra = 0
    readonly_fields = ('contribution',)

class ContributionAdmin(admin.ModelAdmin):
    inlines = (ContributionHonoreeInline,)

class HonoreeAdmin(admin.ModelAdmin):
    inlines = (ContributionHonoreeInline,)

admin.basic_site.register(Registrant)
admin.basic_site.register(Honoree, HonoreeAdmin)
admin.basic_site.register(Contribution, ContributionAdmin)
