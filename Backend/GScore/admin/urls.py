from django.urls import path
from admin.site import GScoreAdminSite



urlpatterns = [
    path('', GScoreAdminSite.urls),  
]