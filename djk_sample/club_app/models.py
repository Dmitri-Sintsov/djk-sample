from collections import OrderedDict
from django.db import models
from django_jinja_knockout.tpl import format_local_date

class Club(models.Model):
    CATEGORY_RECREATIONAL = 0
    CATEGORY_PROFESSIONAL = 1
    CATEGORIES = (
        (CATEGORY_RECREATIONAL, 'Recreational'),
        (CATEGORY_PROFESSIONAL, 'Professional'),
    )
    SPORT_BADMINTON = 0
    SPORT_TENNIS = 1
    SPORT_TABLE_TENNIS = 2
    SPORT_SQUASH = 3
    SPORTS = (
        (SPORT_BADMINTON, 'Badminton'),
        (SPORT_TENNIS, 'Tennis'),
        (SPORT_TABLE_TENNIS, 'Table tennis'),
        (SPORT_SQUASH, 'Squash'),
    )
    title = models.CharField(max_length=64, verbose_name='Title')
    sport = models.IntegerField(choices=SPORTS, default=SPORT_BADMINTON, verbose_name='Sport')
    category = models.IntegerField(choices=CATEGORIES, default=CATEGORY_RECREATIONAL, verbose_name='Category')
    foundation_date = models.DateField(db_index=True, verbose_name='Foundation date')

    def get_str_fields(self):
        return OrderedDict([
            ('title', title),
            ('sport', self.get_sport_display()),
            ('category', self.get_category_display()),
            ('foundation_date', format_local_date(self.foundation_date))
        ])

    def __str__(self):
        return ' › '.join(list(self.get_str_fields.values()))

class ClubInventory(models.Model):
    name = models.CharField(max_length=64, verbose_name='Name')
    manufacturer = models.CharField(max_length=64, verbose_name='Manufacturer')
    club = models.ForeignKey(Club, verbose_name='Club')

class ClubMember(models.Model):
    ROLE_OWNER = 0
    ROLE_FOUNDER = 1
    ROLE_PROFESSIONAL = 2
    ROLE_AMATEUR = 3
    ROLES = (
        (ROLE_OWNER, 'Owner'),
        (ROLE_FOUNDER, 'Founder'),
        (ROLE_PROFESSIONAL, 'Professional'),
        (ROLE_AMATEUR, 'Amateur'),
    )
    club = models.ForeignKey(Club, null=True, blank=True, verbose_name='Club')
    first_name = models.CharField(max_length=30, verbose_name='First name')
    last_name = models.CharField(max_length=30, verbose_name='Last name')
    role = models.IntegerField(choices=ROLES, default=ROLE_PROMOTER, verbose_name='Member role')
    note = models.TextField(max_length=16384, blank=True, default='', verbose_name='Note')
    # Allows to have only one endorsed member via True, but multiple non-endorsed members via None.
    is_endorsed = models.NullBooleanField(default=None, verbose_name='Endorsed')

    # Complex nested str fields with foregin keys.
    # ClubMember.__str__() uses Club.get_str_fields() for DRY.
    def get_str_fields(self):
        # Nested formatting of foreign keys:
        parts = OrderedDict([
            ('club', self.club.get_str_fields()),
        ])
        return parts

    def __str__(self):
        str_fields = self.get_str_fields()
        join_dict_values(' / ', str_fields, ['club'])
        return ' › '.join(str_fields.values())
