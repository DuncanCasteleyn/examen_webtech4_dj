from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^post', views.post, name='add movie'),
    url(r'^init', views.init, name='init movies'),
    url(r'^', views.index, name='index'),
]
