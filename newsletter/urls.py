from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^subscribe$', views.newsletter_create, name="newsletter_create"),
    url(r'^unsubscribe$', views.newsletter_unsubscribe, name="newsletter_unsubscribe"),
    url(r'^resubscribe$', views.newsletter_resubscribe, name="newsletter_resubscribe"),
]
