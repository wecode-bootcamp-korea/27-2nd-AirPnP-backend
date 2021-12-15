from django.urls    import path

from users.views    import KakaoLoginView

urlpatterns = [
    path('/signin', KakaoLoginView.as_view()) 
]