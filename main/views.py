from django.shortcuts import render
# from django_geoip.models import IpRange

from django.views.generic import TemplateView,View
from.models import Hotel, Menu, OperatingCity, CATEGORY_CHOICES
# Create your views here.

class HomeView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self,**kwargs):
        context = super(HomeView,self).get_context_data(**kwargs)
        hotels = Hotel.objects.all()
        cities = OperatingCity.objects.all()
        context['all']=hotels
        context['cities']=cities
        return context

class CityView(TemplateView):

    template_name = 'hotel-list.html'

    def get_context_data(self,**kwargs):
        context = super(CityView,self).get_context_data(**kwargs)
        list = Hotel.objects.filter(location=kwargs['pk'])
        context['list'] = list
        return context

class HotelMenuView(TemplateView):
    template_name = 'hotel-menu.html'

    def get_menu(self):
        return Menu.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HotelMenuView,self).get_context_data(**kwargs)
        menu = Menu.objects.filter(hotel=kwargs['pk'])
        for each in menu:
            print "Inside it"
            if each.get_category() in CATEGORY_CHOICES:
                print "++++++++++",each

        hotel = Hotel.objects.get(id = kwargs['pk'])

        context['menu'] = menu
        context['hotel'] = hotel
        return context
