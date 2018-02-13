from __future__ import unicode_literals

from django.contrib.auth.models import User
# from django.contrib.gis.geoip2.resources import City
from django.db.models.signals import post_save
from django.dispatch import receiver
from random import randint
from django.db import models
from django.contrib.gis.db import models
# Create your models here.

CATEGORY_CHOICES = (
    (0, "None"),
    (1, "Tandoori Platter"),
    (2, "Soups"),
    (3, "Chats"),
    (4, "Special Eco Meals"),
    (5, "Thali"),
    (6, "Chinese"),
    (7, "Chinese Platter"),
    (8, "Sizzler (Chinese)"),
    (9, "Continental"),
    (10, "South Indian"),
    (11, "Snacks & Dhokla"),
    (12, "Winter Special"),
    (13, "Kulfi / Chuski"),
    (14, "Beverages"),
    (15, "Sandwich Spl"),
    (16, "North Indian Cuisine"),

)
TIME_SLOT = (
    (0, "00:00"),
    (1, "01:00"),
    (2, "02:00"),
    (3, "03:00"),
    (4, "04:00"),
    (5, "05:00"),
    (6, "06:00"),
    (7, "07:00"),
    (8, "08:00"),
    (9, "09:00"),
    (10, "10:00"),
    (11, "11:00"),
    (12, "12:00"),
    (13, "13:00"),
    (14, "14:00"),
    (15, "15:00"),
    (16, "16:00"),
    (17, "17:00"),
    (18, "18:00"),
    (19, "19:00"),
    (20, "20:00"),
    (21, "21:00"),
    (22, "22:00"),
    (23, "23:00"),
)

OPERATING_CITIES = (
    ('DL', "DELHI/NCR"),
    ('CHE', "CHENNAI"),
    ('BLR', "BANGALORE"),
    ('CH', "CHANDIGARH"),
)

# class Location(models.Model):
#     name = models.CharField(max_length = 100, blank = True)
#     coords = models.PointField()

# class HotelRegistration(models.Model):
#     restaurant_name = models.CharField(max_length=400, null=True, blank=True)
#     location = models.CharField(max_length=400)
#     city = models.CharField(max_length=300, null=True, blank=True)
#     state = models.CharField(max_length=300, null=True, blank=True)
#     owner_name = models.CharField(max_length=400, null=True, blank=True)
#     restaurant_gst_number = models.IntegerField(default=0, null=True, blank=True)
#     opening_time = models.TimeField(null=True)
#     closing_time = models.TimeField(null=True)
#
#     def __unicode__(self):
#         return self.restaurant_name
#
# class Profile(models.Model):
#     user = models.OneToOneField(User)
#     hotel = models.ForeignKey('HotelRegistration', null=True, blank=True)
#     contact_number = models.CharField(max_length=15, null=True, blank=True)
#
#     def __unicode__(self):
#         if self.hotel:
#             return u'%s < %s >' % (self.hotel, self.user.username)
#         else:
#             return self.user.username
#
#
#
# class Order(models.Model):
#     user = models.ForeignKey(User)
#     hotel = models.ForeignKey(HotelRegistration)
#     amount = models.CharField(max_length=200, null=True, blank=True)
#
#     def __unicode__(self):
#         return u'Order for %s by %s' % (self.hotel.restaurant_name, self.user)
#
#
# class OrderDetails(models.Model):
#     order = models.ForeignKey(Order)
#     name = models.CharField(max_length=300, null=True, blank=True)
#     price = models.IntegerField(default=0, null=True, blank=True)
#
#     def __unicode__(self):
#         return u'%s ordered at %s by %s' % (self.name, self.order.hotel.restaurant_name, self.order.user)


class Location(models.Model):
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    # pop2005 = models.IntegerField('Population 2005')
    # fips = models.CharField('FIPS Code', max_length=2)
    # iso2 = models.CharField('2 Digit ISO', max_length=2)
    # iso3 = models.CharField('3 Digit ISO', max_length=3)
    # un = models.IntegerField('United Nations Code')
    # region = models.IntegerField('Region Code')
    # subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

class OperatingCity(models.Model):
    city = models.CharField(choices=OPERATING_CITIES, max_length=20)

    def get_city(self):
        return dict(OPERATING_CITIES).get(self.city)

    def __unicode__(self):
        return self.city


class Hotel(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    # location  = models.ForeignKey(Location)
    owner_name = models.CharField(max_length=300, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    opening_time = models.TimeField(null=True)
    closing_time = models.TimeField(null=True)
    location = models.ForeignKey(OperatingCity)

    def __unicode__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=25, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

class Order(models.Model):
    customer = models.ForeignKey(Customer)
    order_id = models.CharField(max_length=32, unique=True)
    hotel = models.ForeignKey(Hotel)
    total_amount = models.CharField(max_length=50, null=True)
    time_slot = models.IntegerField(choices=TIME_SLOT, null=True)
    accepted = models.BooleanField(default=False)

    def get_time_slot(self):
        return dict(TIME_SLOT).get(self.time_slot)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = get_unique_id(self)
        super(Order, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.order_id

class OrderDetails(models.Model):
    order = models.ForeignKey(Order)
    name = models.CharField(max_length=300, null=True)
    amount = models.CharField(max_length=250, null=True)

    def __unicode__(self):
        return u'%s <%s> ' % (self.name, self.order.hotel)

class Menu(models.Model):
    hotel = models.ForeignKey(Hotel)
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=0)
    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s < %s, %s >' % (self.name, self.get_category() ,self.price)

    def get_category(self):
        return dict(CATEGORY_CHOICES).get(self.category)


def get_unique_id(instance):
    unique_id = "{0:10d}".format(randint(1, 10000000000)).replace(" ", "0")

    if Order.objects.filter(order_id=unique_id).exists():
        get_unique_id(instance)
    # elif instance.__class__.__name__ == "Refund":
    #     if Refund.objects.filter(refund_id=unique_id).exists():
    #         get_unique_id(proifle, instance)
    return unique_id
