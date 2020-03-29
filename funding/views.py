# -*- coding: utf-8 -*-
from .models import Funding
from .serializers import FundingSerializer
from admin_data.models import AdminData
from backend.utils import send_email, get_list_social_links_images
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from email.mime.image import MIMEImage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from settings_db.models import SettingsDb
from sociallink.views import get_list_social_links


@api_view(['GET'])
def funding_list(request):
    """
    List funding.
    """
    funding = Funding.objects.filter().order_by('-createdAt')
    serializer = FundingSerializer(funding, context={'request': request}, many=True)
    return Response({
        'data': serializer.data
    })
