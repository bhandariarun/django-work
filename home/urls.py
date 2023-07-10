from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name= "home"


urlpatterns = [
    path('', UploadView.as_view(), name='upload'),
    path('gallery/', UploadView.as_view(), name='gallery'),
    path('image/<int:image_id>/', ImageView.as_view(), name='image_detail'),
    path('download/', DownloadView.as_view(), name='download'),
]