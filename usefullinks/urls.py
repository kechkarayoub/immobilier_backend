from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.links_list, name="links_list"),
]
