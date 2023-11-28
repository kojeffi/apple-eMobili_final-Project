
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from . import views as my_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', my_views.dashbord, name='dashbord-url'),
    path('toggle_process/', my_views.toggle_process, name='toggle_process'),
    path('clear_word/', my_views.clear_word, name='clear_word'),
    path('video_feed/', my_views.video_feed, name='video_feed'),
    path('save_recognized_alphabets/', my_views.save_recognized_alphabets, name='save_recognized_alphabets'),
    path('clear_recognized_alphabets/', my_views.clear_recognized_alphabets, name='clear_recognized_alphabets'),
    path('download_pdf/', my_views.download_table_as_pdf, name='download_pdf'),
    path('delete/<id>/', my_views.delete, name='delete'),
    path('pay/<id>/', my_views.pay, name='pay'),
    path('recognize/', my_views.recognize_letters, name='recognize-url'),
    path('save_recognized_alphabets/', my_views.save_recognized_alphabets, name='save_recognized_alphabets'),
    path('pay/<int:id>/', my_views.pay, name='pay'),
    path('download/', my_views.download, name='download-url'),


]

# Serving static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
