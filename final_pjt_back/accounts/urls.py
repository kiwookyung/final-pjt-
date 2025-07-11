from django.urls import path
from . import views


app_name = "profile"
urlpatterns = [
    path("<int:user_pk>/", views.profile),
    path("<int:user_pk>/like/", views.like_num_of_article),
    path("<int:user_pk>/follow/", views.follow),
    path("<int:movie_pk>/article/", views.article_movie),
    path("<int:user_pk>/update/", views.update_profile),
    path("<int:user_pk>/delete/", views.delete_profile),
    path('change-password/', views.change_password, name='change_password'),
    path('<int:user_pk>/follow/status/', views.follow_status),
]
