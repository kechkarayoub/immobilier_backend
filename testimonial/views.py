# -*- coding: utf-8 -*-
from .models import Testimonial
from .serializers import TestimonialSerializer
# from backend.project_conf import NBR_TESTIMONIALS_PER_PAGE
# from backend.utils import generate_random_color
# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# @api_view(['POST'])
# def create_testimonial(request):
#     """
#     create a testimonial.
#     """
#     if request.method == 'POST':
#         data = request.data.copy()
#         color, complementary_color = generate_random_color(with_complementary=True)
#         data["initials_color"] = color
#         data["initials_bg_color"] = complementary_color
#         serializer = TestimonialSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def testimonials_list(request):
    """
    List testimonials.
    """
    testimonials = Testimonial.objects.filter().order_by('-createdAt')
    # page = request.GET.get('page', 1)
    # if request.GET.get('test', False):
    #     paginator = Paginator(testimonials, 1)
    # else:
    #     paginator = Paginator(testimonials, NBR_TESTIMONIALS_PER_PAGE)
    # try:
    #     data = paginator.page(page)
    # except EmptyPage:
    #     data = paginator.page(paginator.num_pages)

    serializer = TestimonialSerializer(testimonials, context={'request': request}, many=True)
    # if data.has_next():
    #     next_page = data.next_page_number()
    # else:
    #     next_page = 0
    # if data.has_previous():
    #     previous_page = data.previous_page_number()
    # else:
    #     previous_page = 0

    return Response({
        # 'count': paginator.count,
        'data': serializer.data,
        # 'nextLink': '/api/testimonials/?page=' + str(next_page) if next_page else '',
        # 'numpages': paginator.num_pages,
        # 'prevLink': '/api/testimonials/?page=' + str(previous_page) if previous_page else ''
    })

