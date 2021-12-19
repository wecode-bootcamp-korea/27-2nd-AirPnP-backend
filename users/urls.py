from django.urls    import path

from users.views    import KakaoLoginView, ImageUploader, HostListView

urlpatterns = [
    path('/signin', KakaoLoginView.as_view()),
    path('/imageUploader', ImageUploader.as_view()),
    path('/hosts', HostListView.as_view()),
]