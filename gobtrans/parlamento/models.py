# -*- coding: utf-8 -*-
from django.db.models import Model, PositiveIntegerField


class Legislature(Model):
    """Una legislatura es un período de gobierno, la cual a su vez consta de
    períodos que son anuales."""

    number = PositiveIntegerField(_(u'number'))
    from_year = PositiveIntegerField(_(u'from year'))
    to_year = PositiveIntegerField(_(u'to year'))

    def __unicode__(self):
        return unicode(self.number)


class Period(Model):
    """
    """

    legislature = ForeignKey(Legislature, verbose_name=_(u'period'),
                             related_name='periods')
    from_date = DateTimeField(_(u'from date'))
    to_date = DateTimeField(_(u'to date'))


class Party(Model):
    """
    """

    name = CharField(_(u'party'), max_length=128)

    def __unicode__(self):
        return self.name


class Parliamentary(Model):
    """
    """

    name = CharField(_(u'name'), max_length=128)
    picture = ImageField(_(u'picture'), upload_to='parliamentaries')

    def __unicode__(self):
        return self.name


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


class Substitution(Model):
    """
    """

    SENATE = '0'
    DEPUTY = '1'
    SUBSTITUTION_IN_CHAMBER = (
        (SENATE, _(u'Senate')),
        (DEPUTY, _(u'Deputy')),
    )

    parliamentary = ForeignKey(Parliamentary, verbose_name=_(u'parliamentary'),
                               related_name='substitutions')
    in_chamber = CharField(_(u'in chamber'), max_length=1,
                           choices=SUBSTITUTION_IN_CHAMBER)
    from_date = DateTimeField(_(u'from date'))
    to_date = DateTimeField(_(u'to date'))

    def __unicode__(self):
        return self.parliamentary.__unicode__()


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
    date = DateTimeField(_(u'date'))

    def __unicode__(self):
        return unicode(self.date)


class Citation(Model):
    """
    """

    session = ForeignKey(Session, verbose_name=_(u'session'),
                         related_name='citations')
    parliamentary = ForeignKey(Parliamentary, verbose_name=_(u'parliamentary'),
                               related_name='citations')

    def __unicode__(self):
        return self.session.__unicode__()


class Absence(Model):
    """
    """

    citation = ForeignKey(Citation, verbose_name=_(u'citation'),
                          related_name='absences')
    with_notice = BooleanField(_(u'with notice'))

    def __unicode__(self):
        return self.citation.__unicode__()


class License(Model):
    """
    """

    reason = TextField(_(u'reason'))
    from_date = DateTimeField(_(u'from date'))
    to_date = DateTimeField(_(u'to date'))

    def __unicode__(self):
        return unicode(self.pk)


class Issue(Model):
    """
    """

    category = CharField(_(u'category'), max_length=128)
    origin = CharField(_(u'origin'), max_length=128)
    text = TextField(_(u'text'))

    def __unicode__(self):
        return self.category


class Entry(Model):
    """
    """

    date = DateTimeField(_(u'date'))
    origin = CharField(_(u'origin'), max_length=128)