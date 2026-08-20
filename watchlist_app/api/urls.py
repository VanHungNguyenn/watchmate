from django.contrib import admin
from django.urls import include, path

from watchlist_app.api.views import StreamPlatformAV, StreamPlatformDetailAV, WatchListAV, WatchDetailAV

urlpatterns = [
    path("list/", WatchListAV.as_view(), name="watchlist-list"),
    path("<int:pk>/", WatchDetailAV.as_view(), name="watchlist-details"),
    path("stream/", StreamPlatformAV.as_view(), name="streamplatform-list"),
    path("stream/<int:pk>/", StreamPlatformDetailAV.as_view(), name="streamplatform-details"),
]
