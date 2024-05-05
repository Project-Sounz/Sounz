
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/',admin.site.urls),
    path('', views.log),
    path('', views.log,name='signin'),
    path('reg2',views.reg2,name='reg2'),
    path('home', views.homepage, name = 'home'),
    path('homeCheck', views.homeCheck, name = 'homeCheck'),
    path('profile', views.profile, name='profile'),
    path('editprofile',views.editprofile, name='editprofile'),
    path('my-profile-saved', views.nav_saved, name='nav-saved'),
    path('logout',views.logout,name='logout'),
    path('signout',views.signout,name='signout'),
    path('upload', views.upload, name='upload'),
    path('watch-profile', views.profile_tpv, name='watch-profile'),
    path('media', views.media, name='media'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
