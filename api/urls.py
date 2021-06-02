from django.urls import path, include
from rest_framework import routers
from .views import TaskViewSet, CategoryViewSet, CreateUserView, ListUserView,\
    LoginUserView, ProfileViewSet


router = routers.DefaultRouter()
#  routerに登録するのはModelViewSetを継承したものという決まり
#  例 TaskViewSet(viewsets.ModelViewSet):
router.register('category', CategoryViewSet)
router.register('tasks', TaskViewSet)
router.register('profile', ProfileViewSet)


#  urlpatternsはgenericsを継承しているのを記載する。
#  例 generics.RetrieveUpdateAPIView
#  ※genericsを継承したものは末尾に.as_view()をつける必要がある。
urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('users/', ListUserView.as_view(), name='users'),
    path('loginuser/', LoginUserView.as_view(), name='loginuser'),
    path('', include(router.urls)),
]
