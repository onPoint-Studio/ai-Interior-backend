from django.urls import path
from .views import GenerateImageView, ImageStatusView, UploadPageView

urlpatterns = [
    path('generate/', GenerateImageView.as_view(), name='generate-image'),
    path('status/',   ImageStatusView.as_view(),    name='image-status'),
    path('upload/', UploadPageView.as_view(), name='image-upload'),

]
