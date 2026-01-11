from unfold.sites import UnfoldAdminSite
from django.urls import path

class GScoreAdminSite(UnfoldAdminSite):
    site_header = "GScore Admin"
    site_title = "GScore Admin Portal"
    index_title = "Welcome to GScore Admin Portal"

gscore_admin_site = GScoreAdminSite(name="gscore_admin")