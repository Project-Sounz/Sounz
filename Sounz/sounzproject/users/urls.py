
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.conf.urls import handler404
from users.views import custom_404

handler404 = custom_404

urlpatterns = [
    # path('admin/',admin.site.urls),
    # path('', views.log),
    path('', views.log_new,name='log-in'),
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
    
    # path('404-not-found',views.notfound, name='404-not-found'),
    path("save-collab", views.save_collab, name="save-collab"),
    path('toggle-like/', views.toggle_like, name='toggle_like'),
    path('notifications/', views.notifications, name='notifications'),
    path('toggle-save/', views.toggle_save, name='toggle_save'),
    path('search',views.search,name='search'),
    path('edit-post', views.editpost, name='edit-post'),
    path('delete-post/<uuid:post_id>/', views.delete_post, name='delete-post'),
    path("report-copyright/", views.report_copyright, name="report_copyright"),
    path("get-user-posts/", views.get_user_posts, name="get_user_posts"),
    path("report-offensive/", views.report_offensive, name='report_offensive'),
    path("toggle-follow/", views.toggle_follow, name="toggle-follow"),
    path('collab-request/<uuid:collab_id>/', views.collaboration_request, name='collab_request'),
    path('update-collab-status/<uuid:collab_id>/', views.update_collab_status, name='update-collab-status'),
    path('workspace',views.collab_workspace,name='collab-workspace'),
    path("upload-sync-audio/", views.upload_sync_audio, name="upload_sync_audio"),
    path("delete-audio", views.delete_audio, name="delete-audio"),
     path('chat/send/<uuid:collab_id>/', views.send_chat_message, name='send_chat_message'),
     path('chat/history/<uuid:collab_id>/', views.get_chat_history, name='get_chat_history'),
    path("approval-update", views.approve_button, name="approval-update"),
    path("get-approval-status/", views.get_approval_status, name="get-approval-status"),
    path('get-audio-files/', views.get_audio_files, name='get-audio-files'),
    path("upload-mixed-audio/", views.upload_mixed_audio, name="upload-mixed-audio"),
    path("end-collab", views.end_collab, name="end-collab"),
    path("update-collab-post/", views.update_collab_post, name="update-collab-post"),
    path("fetch-temp-data", views.fetch_temp_data, name="fetch-temp-data"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
