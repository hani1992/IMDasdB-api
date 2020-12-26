from django.shortcuts import render
from django.http import JsonResponse
from pytz import unicode

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from .serlializer import *

# Create your views here.

@api_view(['GET'])
def movieList(request):
    movies = Movies.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def topRates(request):
    movies = Movies.objects.values_list('id', 'title', 'tag__name')
    print(movies)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def topFeatured(request):
    movies = Movies.objects.filter(IsFeatured=True)
    print(movies)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes((IsAuthenticatedOrReadOnly,))
# def example_view(request, format=None):
#     content = {
#         'user': unicode(request.user),  # `django.contrib.auth.User` instance.
#         'auth': unicode(request.auth),  # None
#     }
#     return Response(content)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
        })
