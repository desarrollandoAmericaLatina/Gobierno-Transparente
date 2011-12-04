# -*- coding: utf-8 -*-
from .models import (Absence, Citation, Deputy, Entry, Issue, Legislature,
                     License, Parliamentary, Party, Period, Senator, Session,
                     Substitution,)

from django.contrib.admin import site, ModelAdmin
from django.utils.translation import ugettext_lazy as _


class AbsenceAdmin(ModelAdmin):

    pass


class CitationAdmin(ModelAdmin):

    pass


class DeputyAdmin(ModelAdmin):

    pass


class EntryAdmin(ModelAdmin):

    pass


class IssueAdmin(ModelAdmin):

    pass


class LegislatureAdmin(ModelAdmin):

    pass


class LicenseAdmin(ModelAdmin):

    pass


class ParliamentaryAdmin(ModelAdmin):

    pass


def party_parliamentaries(obj):
    return obj.senators.all().count() + obj.deputies.all().count()
party_parliamentaries.short_description = _(u'parliamentaries')


class PartyAdmin(ModelAdmin):

    list_display = ('name', party_parliamentaries)


class PeriodAdmin(ModelAdmin):

    pass


class SenatorAdmin(ModelAdmin):

    pass


class SessionAdmin(ModelAdmin):

    pass


class SubstitutionAdmin(ModelAdmin):

    pass


site.register(Absence, AbsenceAdmin)
site.register(Citation, CitationAdmin)
site.register(Deputy, DeputyAdmin)
site.register(Entry, EntryAdmin)
site.register(Issue, IssueAdmin)
site.register(Legislature, LegislatureAdmin)
site.register(License, LicenseAdmin)
site.register(Parliamentary, ParliamentaryAdmin)
site.register(Party, PartyAdmin)
site.register(Period, PeriodAdmin)
site.register(Senator, SenatorAdmin)
site.register(Session, SessionAdmin)
site.register(Substitution, SubstitutionAdmin)
