from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.testimonials_list, name="testimonials_list"),
    # url(r'^create$', views.create_testimonial, name="create_testimonial"),
]
