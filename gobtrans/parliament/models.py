# -*- coding: utf-8 -*-
# vim: tw=80
from django.db.models import (BooleanField, CharField, DateField,
                              DateTimeField, ForeignKey, ImageField, Model,
                              OneToOneField, PositiveIntegerField, TextField,)

from django.utils.translation import ugettext_lazy as _


class Legislature(Model):
    """A legislature is a 5 year government. It contains Periods which are
    yearly.
    """

    number = PositiveIntegerField(_(u'number'), unique=True)
    from_year = PositiveIntegerField(_(u'from year'))
    to_year = PositiveIntegerField(_(u'to year'))

    def __unicode__(self):
        return unicode(self.number)

    class Meta:
        verbose_name = _(u'legislature')
        verbose_name_plural = _(u'legislatures')


class Period(Model):
    """Every year begins a new Period. On the year of the elections the period
    begins on march, the other 4 years it begins on freburary.
    """

    legislature = ForeignKey(Legislature, verbose_name=_(u'period'),
                             related_name='periods')
    from_date = DateTimeField(_(u'from date'), unique=True)
    to_date = DateTimeField(_(u'to date'), unique=True)

    class Meta:
        verbose_name = _(u'period')
        verbose_name_plural = _(u'periods')


class Party(Model):
    """A political party.
    """

    name = CharField(_(u'party'), max_length=128, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'party')
        verbose_name_plural = _(u'parties')


class Parliamentary(Model):
    """A parliamentary is a person. It's not Senator nor Deputy by itself, that
    depends on the Legislature and Parliamentary relation.
    """

    id_parliament = CharField(u'id parliament', max_length=5, unique=True)
    first_name = CharField(_(u'first name'), max_length=128)
    last_name = CharField(_(u'last name'), max_length=128)
    picture = ImageField(_(u'picture'), upload_to='parliamentaries')

    def __unicode__(self):
        return " ".join((self.first_name, self.last_name))

    class Meta:
        verbose_name = _(u'parliamentary')
        verbose_name_plural = _(u'parliamentaries')


class Senator(Model):
    """
    """

    legislature = ForeignKey(Legislature, verbose_name=_(u'legislature'),
                             related_name='senators')
    parliamentary = ForeignKey(Parliamentary, verbose_name=_(u'parliamentary'),
                               related_name='senators')
    party = ForeignKey(Party, verbose_name=_(u'party'),
                       related_name='senators')

    def __unicode__(self):
        return self.parliamentary.__unicode__()

    class Meta:
        unique_together = (('legislature', 'parliamentary', 'party',),)
        verbose_name = _(u'senator')
        verbose_name_plural = _(u'senators')


class Deputy(Model):
    """
    """

    legislature = ForeignKey(Legislature, verbose_name=_(u'legislature'),
                             related_name='deputies')
    parliamentary = ForeignKey(Parliamentary, verbose_name=_(u'parliamentary'),
                               related_name='deputies')
    party = ForeignKey(Party, verbose_name=_(u'party'),
                       related_name='deputies')

    def __unicode__(self):
        return self.parliamentary.__unicode__()

    class Meta:
        unique_together = (('legislature', 'parliamentary', 'party',),)
        verbose_name = _(u'deputy')
        verbose_name_plural = _(u'deputies')


class Substitution(Model):
    """A substitution of a parliamentary.
    """

    SENATE = '0'
    DEPUTY = '1'
    SUBSTITUTION_IN_CHAMBER = (
        (SENATE, _(u'Senate')),
        (DEPUTY, _(u'Deputy')),
    )

    parliamentary = ForeignKey(Parliamentary, verbose_name=_(u'parliamentary'),
                               related_name='substitutions')
    substitutes = ForeignKey(Parliamentary, verbose_name=_(u'substitutes'),
                             related_name='substituted_by', blank=True,
                             null=True)
    in_chamber = CharField(_(u'in chamber'), max_length=1,
                           choices=SUBSTITUTION_IN_CHAMBER)
    from_date = DateTimeField(_(u'from date'), blank=True, null=True)
    to_date = DateTimeField(_(u'to date'), blank=True, null=True)
    reason = CharField(_(u'reason'), max_length=255)

    def __unicode__(self):
        return self.parliamentary.__unicode__()

    class Meta:
        verbose_name = _(u'substitution')
        verbose_name_plural = _(u'substitutions')


class Session(Model):
    """
    """

    SENATE = '0'
    DEPUTY = '1'
    SESSION_CHAMBER = (
        (SENATE, _(u'Senate')),
        (DEPUTY, _(u'Deputy')),
    )


    period = ForeignKey(Period, verbose_name=_(u'period'),
                        related_name='sessions')
    chamber = CharField(_(u'chamber'), max_length=1, choices=SESSION_CHAMBER)
    internal_id = PositiveIntegerField(_(u'internal id'))
    date = DateField(_(u'date'))

    def __unicode__(self):
        return unicode(self.date)

    class Meta:
        unique_together = (('period', 'internal_id'),)
        verbose_name = _(u'session')
        verbose_name_plural = _(u'sessions')


class Citation(Model):
    """
    """

    session = ForeignKey(Session, verbose_name=_(u'session'),
                         related_name='citations')
    parliamentary = ForeignKey(Parliamentary, verbose_name=_(u'parliamentary'),
                               related_name='citations')

    def __unicode__(self):
        return self.session.__unicode__()

    class Meta:
        unique_together = (('session', 'parliamentary'),)
        verbose_name = _(u'citation')
        verbose_name_plural = _(u'citations')


class Absence(Model):
    """
    """

    citation = OneToOneField(Citation, verbose_name=_(u'citation'),
                             related_name='absences', unique=True)
    with_notice = BooleanField(_(u'with notice'))

    def __unicode__(self):
        return self.citation.__unicode__()

    class Meta:
        verbose_name = _(u'absence')
        verbose_name_plural = _(u'absences')


class License(Model):
    """
    """

    parliamentary = ForeignKey(Parliamentary, verbose_name=_(u'parliamentary'),
                               related_name='licenses')
    reason = TextField(_(u'reason'))
    from_date = DateTimeField(_(u'from date'))
    to_date = DateTimeField(_(u'to date'))

    def __unicode__(self):
        return unicode(self.pk)

    class Meta:
        unique_together = (('parliamentary', 'from_date'),
                            ('parliamentary', 'to_date'))
        verbose_name = _(u'license')
        verbose_name_plural = _(u'licenses')


# FIXME:
class Issue(Model):
    """
    """

    category = CharField(_(u'category'), max_length=128)
    origin = CharField(_(u'origin'), max_length=128)
    text = TextField(_(u'text'))

    def __unicode__(self):
        return self.category

    class Meta:
        verbose_name = _(u'issue')
        verbose_name_plural = _(u'issues')


class Entry(Model):
    """
    """

    date = DateTimeField(_(u'date'))
    origin = CharField(_(u'origin'), max_length=128)

    class Meta:
        verbose_name = _(u'entry')
        verbose_name_plural = _(u'entries')
