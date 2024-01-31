from rest_framework import viewsets
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import permissions
from rest_framework import reverse
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.decorators import api_view, action

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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):
   
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
