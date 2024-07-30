
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    # path('admin/',admin.site.urls),
    # path('', views.log),
    path('', views.log,name='signin'),
    path('log-new', views.log_new,name='log-in'),
    path('reg2',views.reg2,name='reg2'),
    path('registration-new',views.registration_new,name='registration-new'),
    path('home', views.homepage, name = 'home'),
    path('homeCheck', views.homeCheck, name = 'homeCheck'),
    path('my-profile-old', views.profile_fpv, name = 'my-profile-old'),
    path('my-profile', views.profile_new, name = 'my-profile'),
    path('watch-profile', views.profile_tpv, name = 'watch-profile'),
    path('upload', views.upload, name = 'upload'),
    # path('profile', views.profile, name='profile'),
    path('editprofile',views.editprofile, name='editprofile'),
    path('my-profile-saved', views.nav_saved, name='nav-saved'),
    path('logout',views.logout,name='logout'),
    path('signout',views.signout,name='signout'),
    path('upload', views.upload, name='upload'),
    path('watch-profile', views.profile_tpv, name='watch-profile'),
    path('media', views.media, name='media'),
    path('watch-profile#ed-media', views.media_controll, name='sh-media'),
    path('e-mail',views.mailtemplate, name='email'),
    path('send-mail',views.sendemail, name='send-email'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
