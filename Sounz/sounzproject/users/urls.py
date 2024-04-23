
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.log),
    path('reg2',views.reg2,name='reg2'),
    path('homeCheck', views.homeCheck, name = 'homeCheck')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
