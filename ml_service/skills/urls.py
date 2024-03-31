from django.urls import path

from . import views

urlpatterns = [
    path("categories", views.category_list, name = "categories"),
    path('categories/<int:pk>', views.category_detail, name="category"),
    path('skills', views.skill_list, name = "skills"),
    path('skills/<int:pk>', views.skill_detail, name = "skill"),
    path("request-path", views.request_path, name = "request")
]
