from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('intern/', views.internshipdetails, name='intern'),
]

from django.views.generic import RedirectView

urlpatterns += [
    path('about', RedirectView.as_view(url='/about/', permanent=True)),
    path('contact', RedirectView.as_view(url='/contact/', permanent=True)),
    path('services', RedirectView.as_view(url='/services/', permanent=True)),
    path('intern', RedirectView.as_view(url='/intern/', permanent=True)),
    path('blog', RedirectView.as_view(url='/blog/', permanent=True)),
]
