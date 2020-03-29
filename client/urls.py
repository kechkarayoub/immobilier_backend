from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^import$', views.import_clients, name="import_clients")
]
