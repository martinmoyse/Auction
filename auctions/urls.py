from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("listings/<str:listing>", views.display_listing, name="display_listing"),
    path("add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove_from_watchlist", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("categories", views.categories, name="categories"),
    #path("display_category", views.display_category, name="display_category"),
    path("categories/<str:category>", views.display_category, name="display_category")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
