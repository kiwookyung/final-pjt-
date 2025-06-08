from django.urls import path
from . import views


app_name = "movies"
urlpatterns = [
    path("", views.movie_list),
    path("<int:movie_pk>/", views.movie_detail),
    path("recommended/<int:genre_pk>/", views.recommended),
    path("<int:movie_pk>/addlist/", views.add_list),
    path("<int:movie_pk>/articles/", views.article_list_or_create),
    path(
        "<int:movie_pk>/articles/<int:article_pk>/",
        views.articles_get_or_update_or_delete,
    ),
    path(
        "<int:movie_pk>/articles/<int:article_pk>/comments/",
        views.get_create_comment,
    ),
    path(
        "<int:movie_pk>/articles/<int:article_pk>/comments/<int:comment_pk>",
        views.delete_comment,
    ),
    path(
        "<int:movie_pk>/articles/<int:article_pk>/comments/like/",
        views.like_article,
    ),
    path("genres/", views.genre_list),
    path("genres/<int:genre_id>/movies/", views.genre_movies),

    path("<int:movie_pk>/addlist/", views.add_list),

    path('all/', views.all_movies),

    path('chatbot/', views.chatbot, name='chatbot'),

    
     # ✅ 커뮤니티 게시글 목록 & 생성
    path("community/", views.community_post_list_create, name="community-list-create"),

    # ✅ 커뮤니티 게시글 수정 & 삭제
    path("community/<int:post_pk>/", views.community_post_update_delete, name="community-update-delete"),

    # ✅ 커뮤니티 게시글 좋아요 토글
    path("community/<int:post_pk>/like/", views.toggle_like_post, name="community-like"),
     # ✅ 커뮤니티 댓글 작성 & 조회
    path("community/<int:post_pk>/comments/", views.community_comment_list_create, name="community-comment-list-create"),

    # ✅ 커뮤니티 댓글 삭제
    path("community/<int:post_pk>/comments/<int:comment_pk>/", views.community_comment_delete, name="community-comment-delete"),

    path("recommended/save/", views.save_recommended_movies),

    path("top-rated/", views.top_rated_movies),


]

