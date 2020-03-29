from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.funding_list, name="funding_list")
]
