from django.urls    import path

from users.views    import KakaoLoginView, ImageUploader

urlpatterns = [
    path('/signin', KakaoLoginView.as_view()),
    path('/imageUploader', ImageUploader.as_view()),
]