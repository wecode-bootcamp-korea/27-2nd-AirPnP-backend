from django.urls    import path

from users.views    import KakaoLoginView, ImageUploader, HostListView, HostView

urlpatterns = [
    path('/signin', KakaoLoginView.as_view()),
    path('/imageUploader', ImageUploader.as_view()),
    path('/hosts', HostListView.as_view()),
    path('/host', HostView.as_view()),
]
