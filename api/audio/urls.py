from django.urls import path

from audio import views

urlpatterns = [
    path('upload/', views.upload_audio, name='upload_audio'),
    path('', views.audio_list, name='audio_list'),
]