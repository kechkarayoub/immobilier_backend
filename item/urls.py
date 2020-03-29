from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.items_list, name="items_list"),
    url(r'^item/(?P<pk>[\w\-]+)$', views.item_details, name="item_detail"),
]
