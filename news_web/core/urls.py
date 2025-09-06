from django.urls import path
from . import views
from .views import AdminLoginView

urlpatterns = [
    # Public views
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path("", views.home, name="home"),
    path("news/<slug:slug>/", views.news_detail, name="news_detail"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("categories/", views.category_list, name="category_list"),
    # Admin views
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
     # Admin authentication
    path("admin/login/", AdminLoginView.as_view(), name="admin_login"),
    path("admin/logout/", views.admin_logout, name="admin_logout"),

    # Admin News CRUD
    path("admin/news/", views.admin_news_list, name="admin_news_list"),
    path("admin/news/create/", views.admin_news_create, name="admin_news_create"),
    path("admin/news/edit/<slug:slug>/", views.admin_news_edit, name="admin_news_edit"),
    path("admin/news/delete/<slug:slug>/", views.admin_news_delete, name="admin_news_delete"),

    # Admin Category CRUD
    path("admin/categories/", views.admin_category_list, name="admin_category_list"),
    path("admin/categories/create/", views.admin_category_create, name="admin_category_create"),
    path("admin/categories/edit/<slug:slug>/", views.admin_category_edit, name="admin_category_edit"),
    path("admin/categories/delete/<slug:slug>/", views.admin_category_delete, name="admin_category_delete"),
]
