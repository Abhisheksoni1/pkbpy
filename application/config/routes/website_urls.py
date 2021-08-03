from django.contrib import admin
from django.urls import path, include, re_path
from website.views import AboutUs, ContactUs, MenuScreen, Review,HomeView,ErrorView
from django.conf.urls import handler404

# from import

app_name = "web"

urlpatterns = [
    path('', HomeView.as_view(), name='website_home'),
    path('about-us/', AboutUs.as_view(), name='website_about_us'),
    path('contact-us/', ContactUs.as_view(), name='website-contact-us'),
    path('menu-screen/', MenuScreen.as_view(), name='website-menu-screen'),
    path('review/', Review.as_view(), name='website-review'),
    path('home/', HomeView.as_view(), name= 'website_home')
]
