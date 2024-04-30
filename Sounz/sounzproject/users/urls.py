
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/',admin.site.urls),
    path('', views.log),
    path('reg2',views.reg2,name='reg2'),
    path('home', views.homepage, name = 'home'),
    path('homeCheck', views.homeCheck, name = 'homeCheck'),
    path('my-profile', views.profile_fpv, name = 'my-profile'),
    path('watch-profile', views.profile_tpv, name = 'watch-profile'),
    path('upload', views.upload, name = 'upload'),
    path('profile/<str:username>/', views.profile, name='profile'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
