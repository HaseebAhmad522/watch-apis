from django.urls import path
from .viewsets import CSVUploadView, FilterView, WatchFilter,WatchListAPIView, RecommendationAPI

urlpatterns = [
    # Other URL patterns
    path('upload_csv/', CSVUploadView.as_view(), name='upload-csv'),
    path('filter/', FilterView.as_view(), name='filter'),
    path('watch_filter/', WatchFilter.as_view(), name='watch-filter'),
    path('watch_list/', WatchListAPIView.as_view(), name='watch-list'),
    path('recommendation/', RecommendationAPI.as_view(), name='recommendation'),
]
