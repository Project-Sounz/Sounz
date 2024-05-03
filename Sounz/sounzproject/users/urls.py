
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
<<<<<<< HEAD
    path('fpv_profile', views.profile_fpv, name='fpv-profile'),
    path('editprofile',views.editprofile,name='editprofile')
    
=======
    path('editprofile',views.editprofile, name='editprofile'),
    path('my-profile-saved', views.nav_saved, name='nav-saved'),
>>>>>>> 11d1af0daf39ac8e67b635e6b484d6aed413bc80
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
