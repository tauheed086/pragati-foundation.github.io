from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('about/',views.about, name="about" ),
        path('gallery/',views.gallery, name="gallery" ),
        path('person-gallery', views.person_gallery, name='person_gallery'),
        path('submit-valunteer',views.submit_valunteer, name="submit-valunteer" ),
        path('contact',views.contact, name="contact" ),
        path('contactus',views.contactus, name="contactus" ),
        path('history',views.history, name="history" ),
        path('donates',views.donates, name="donates" ),
        path('login/', views.login_view, name='login'),  
        path('add_event/', views.add_event, name='add_event'),
        path('add_cause/', views.add_cause, name='add_cause'),
        path('add_person/', views.add_person, name='add_person'),
        path('add_work/', views.add_work, name='add_work'),
]
