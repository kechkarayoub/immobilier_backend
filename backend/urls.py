"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from . import views
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = i18n_patterns(
    url(r'^', admin.site.urls, name="root"),
    # url(r'^admin/', admin.site.urls, name="admin_root"),
    url(r'^api/global_params/', views.global_params, name="global_params"),
    url(r'^api/items/', include('item.urls')),
    url(r'^api/client/', include('client.urls')),
    url(r'^api/contact/', include('contact.urls')),
    url(r'^api/testimonials/', include('testimonial.urls')),
    url(r'^api/funding/', include('funding.urls')),
    url(r'^api/newsletter/', include('newsletter.urls')),
    url(r'^api/usefullinks/', include('usefullinks.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

