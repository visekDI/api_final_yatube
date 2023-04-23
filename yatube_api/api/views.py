from django.shortcuts import get_object_or_404
from rest_framework import filters, pagination, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from posts.models import Group, Post

from .permissions import IsAuthorOrReadOnlyPermission


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author')
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnlyPermission,
                          IsAuthenticatedOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        """Сохраняет автора поста(авториз.пользователь)."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnlyPermission,
                          IsAuthenticatedOrReadOnly]

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Возвращает запрос, отфильтрованный по id поста,
           к которому написаны комментарии."""
        post = self.get_post()
        return post.comments

    def perform_create(self, serializer):
        """Сохраняет автора коммента(авториз.пользователь)."""
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)
