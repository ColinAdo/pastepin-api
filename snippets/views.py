from rest_framework import mixins
from rest_framework import generics

from .models import Snippet
from .serializers import SnippetSerializer

    
class SnippetList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):

    snippets = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kw):
        
        return self.list(request, *args, **kw)

    def post(self, request, *args, **kw):
        return self.create(request, *args, **kw)


class SnippetDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    snippets = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def retrieve(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kw):
        return self.update(request, *args, **kw)

    def delete(self, request, *args, **kw):
        return self.destroy(request, *args, **kw)
