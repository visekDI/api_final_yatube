from rest_framework.routers import SimpleRouter

from django.urls import include, path

from api.views import CommentViewSet, GroupViewSet, PostViewSet, FollowViewSet

router = SimpleRouter()
router.register('posts', PostViewSet, basename='posts')
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comments')
router.register('groups', GroupViewSet, basename='groups')
router.register('follow', FollowViewSet, basename='follows')

urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
]
