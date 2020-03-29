# -*- coding: utf-8 -*-
from .models import SocialLink
from .serializers import SocialLinkSerializer


def get_list_social_links():
    """
    Get social links list.
    """
    data = SocialLink.objects.filter(is_active=True)
    serializer = SocialLinkSerializer(data, many=True)
    return serializer.data
