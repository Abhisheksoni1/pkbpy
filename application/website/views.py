from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from django.shortcuts import render_to_response
from django.template import RequestContext


# from articles.models import Article


class AboutUs(TemplateView):
    template_name = "website/about-us.html"


class ContactUs(TemplateView):
    template_name = "website/contact-us.html"


class MenuScreen(TemplateView):
    template_name = "website/menu-screen.html"


class Review(TemplateView):
    template_name = "website/review.html"


class HomeView(TemplateView):
    template_name = "website/index.html"


class ErrorView(TemplateView):
    template_name = "website/404.html"

def handeler404(request, *args, **kwargs):
    response = render_to_response("website/404.html")
    response.status_code = 404
    return response
