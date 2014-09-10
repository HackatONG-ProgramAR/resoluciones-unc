import string

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from document.models import Document, Person, Date


class YearListFilter(admin.SimpleListFilter):
    title = _(u'year')

    parameter_name = 'year'

    def lookups(self, request, model_admin):
        years = range(1975,1985)
        return zip(years, years) + [('unk', _(u'Unknown'))]

    def queryset(self, request, queryset):
        year = self.value()
        if year == 'unk':
            return queryset.filter(date=None)
        elif year:
            return queryset.filter(date__year=int(year))


class DocumentAdmin(admin.ModelAdmin):
    search_fields = ['number']
    list_display = ('number', 'date')
    list_filter = (YearListFilter,)
    readonly_fields = ('number', 'date', 'file_links')
    date_hierarchy = 'date'

    def file_links(self, instance):
        files = instance.files()
        return '<br/>'.join(f.link_tag() for f in files)
    file_links.allow_tags = True


class InitialListFilter(admin.SimpleListFilter):
    title = _(u'initial')

    parameter_name = 'initial'

    def lookups(self, request, model_admin):
        initials = string.uppercase
        return zip(initials, initials) + [('other', _(u'Other'))]

    def queryset(self, request, queryset):
        initial = self.value()
        if initial == 'other':
            return queryset.exclude(name__regex=r'^[A-Z]')
        elif initial:
            return queryset.filter(name__startswith=initial)


class EntityAdmin(admin.ModelAdmin):

    def occurrences(self, instance):
        occurrences = instance.occurrences()
        return '<br/>'.join(o.link_tag() for o in occurrences)
    occurrences.allow_tags = True
    occurrences.short_description = _(u'occurrences')

    def occurrence_count(self, instance):
       return instance.entityoccurrence__count
    occurrence_count.short_description = _(u'occurrence count')
    occurrence_count.admin_order_field = 'entityoccurrence__count'


class PersonAdmin(EntityAdmin):
    search_fields = ['name']
    list_display = ('name', 'occurrence_count')
    list_filter = (InitialListFilter,)

    fields = ('name', 'identifier', 'occurrences')
    readonly_fields = ('name', 'identifier', 'occurrences')

    def get_queryset(self, request):
        return Person.objects.annotate(Count('entityoccurrence', distinct=True))


class DateAdmin(EntityAdmin):
    search_fields = ['key']
    list_display = ('key', 'occurrence_count')

    fields = ('key', 'occurrences')
    readonly_fields = ('key', 'occurrences')

    def get_queryset(self, request):
        return Date.objects.annotate(Count('entityoccurrence', distinct=True))


admin.site.register(Document, DocumentAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Date, DateAdmin)
