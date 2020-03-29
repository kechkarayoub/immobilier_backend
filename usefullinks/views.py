# -*- coding: utf-8 -*-
from .models import LinkCategory
from .serializers import LinkSerializer
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.translation import ugettext as _
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def links_list(request):
    """
    List links.
    """
    categories_ = {}
    categories = LinkCategory.objects.all()
    for category in categories:
        if category.links.all().exists():
            serializer = LinkSerializer(category.links.all(), context={'request': request}, many=True)
            categories_[category.label] = serializer.data
    guides = [
        {
            "label": _("The Buyer's Guide (PDF)"),
            "url": settings.BACKEND_URL_ROOT + static("usefullinks/docs/en/buyers-guide.pdf" if True else "usefullinks/docs/fr/guide-acheteur.pdf")
        },
        {
            "label": _("The Seller's Guide (PDF)"),
            "url": settings.BACKEND_URL_ROOT + static("usefullinks/docs/en/sellers-guide.pdf" if True else "usefullinks/docs/fr/guide-vendeur.pdf")
        }
    ]

    return Response({
        'categories': categories_,
        'guides': guides
    })

