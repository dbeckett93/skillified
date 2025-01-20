from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('terms_privacy/', views.terms_privacy, name='terms_privacy'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mentor_skills/', views.mentor_skills, name='mentor_skills'),
    path('mentor_add_skill/', views.mentor_add_skill, name='mentor_add_skill'),
    path('skill/<int:skill_id>/', views.skill_detail, name='skill_detail'),
    path('events/', views.events, name='events'),
    path('add_event/<int:skill_id>/', views.add_event, name='add_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('messages/', views.messages_view, name='messages'),
    path('settings/', views.settings, name='settings'),
    path('profile/', views.profile, name='profile'),
    path('add_skill/', views.add_skill, name='add_skill'),
    path('delete_skill/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    path('delete_skill_api/', views.delete_skill_api, name='delete_skill_api'),
    path('edit_skill/', views.edit_skill, name='edit_skill'),
    path('edit_skill_detail/', views.edit_skill_detail, name='edit_skill_detail'),
    path('delete_profile_picture/', views.delete_profile_picture, name='delete_profile_picture'),
    path('logout/', views.logout, name='logout'),
]