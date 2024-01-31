from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import permissions
from rest_framework import reverse
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Snippet
from .permisssions import IsOwnerOrReadOnly
from .serializers import SnippetSerializer, UserSerializer


@api_view
def api_root(request, format=None):
    return Response(
        {
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippets-list', request=request, format=format)
        }
    )
    
class SnippetList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

