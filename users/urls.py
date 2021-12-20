from django.urls    import path

from users.views    import KakaoLoginView, ImageUploader, HostListView, HostView, HostDetailView

urlpatterns = [
    path('/signin', KakaoLoginView.as_view()),
    path('/imageUploader', ImageUploader.as_view()),
    path('/hosts', HostListView.as_view()),
    path('/host', HostView.as_view()),
    path('/hosts/detail/<int:host_id>', HostDetailView.as_view()),
]

