from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("", include("habit_tracker.urls")),
    path("quotes/", include("quotes.urls")),
    path("admin/", admin.site.urls),
]
