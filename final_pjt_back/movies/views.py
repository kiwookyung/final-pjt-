from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.core.paginator import Paginator
from django.db.models import Count, F, FloatField, ExpressionWrapper
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import (
    MovieListSerializer,
    ArticleSerializer,
    MovieSerializer,
    MovieGenreSerializer,
    UserArticleSerializer,
    CommentSerializer,
    GenreSerializer,
    CommunityPostSerializer, ##커뮤니티
    CommunityCommentSerializer, ##커뮤니티 댓글
)
from .models import Movie, Article, Comment, Genre

from openai import OpenAI
import os
from .models import Movie, Article, Comment, Genre, CommunityPost, CommunityComment

client = OpenAI(api_key=os.getenv("VITE_OPENAI_API_KEY"))

# 모든 영화
@api_view(["GET"])
def movie_list(request):
    sort = request.GET.get("sort")
    movies = Movie.objects.all()

    if sort == "release_date":
        movies = movies.exclude(release_date=None).order_by("-release_date")
    elif sort == "vote_count":
        movies = movies.order_by("-vote_count")
    elif sort == "vote_average":
        movies = movies.order_by("-vote_average")
    else:
        movies = movies.order_by("-id")  # 기본 정렬

    paginator = Paginator(movies, 20)
    page = request.GET.get("page", 1)
    page_movies = paginator.get_page(page)

    serializer = MovieListSerializer(page_movies, many=True)
    return Response(serializer.data)



# 각 영화별 detail 정보
@api_view(['GET'])
def movie_detail(request, movie_pk):
    try:
        # 먼저 TMDB ID로 조회
        movie = Movie.objects.get(tmdb_id=movie_pk)
    except Movie.DoesNotExist:
        # fallback: 기존 방식 (직접 저장한 id인 경우)
        movie = get_object_or_404(Movie, pk=movie_pk)
    
    serializer = MovieSerializer(movie)
    return Response(serializer.data, status=status.HTTP_200_OK)



# 해당하는 장르 찾기
@api_view(["GET"])
def recommended(request, genre_pk):
    if request.method == "GET":
        movies = get_list_or_404(Movie)
        serializer = MovieGenreSerializer(movies, many=True)

        comedyGenre = [
            5,
            13,
            68,
            71,
            75,
            90,
            96,
            99,
            100,
            107,
            109,
            114,
            115,
            137,
            153,
            164,
            177,
            194,
            219,
            239,
            243,
            245,
            248,
            252,
            262,
            284,
            287,
            290,
            292,
            306,
            310,
            321,
            338,
            342,
            350,
            378,
            392,
            401,
            433,
            439,
            452,
            455,
            458,
            464,
            480,
            492,
            496,
            508,
            509,
            512,
        ]
        actionGenre = [
            667,
            668,
            670,
            676,
            679,
            681,
            682,
            691,
            698,
            699,
            700,
            707,
            708,
            709,
            710,
            714,
            744,
            752,
            754,
            755,
            787,
            792,
            834,
            839,
            841,
            847,
            849,
            855,
            860,
            861,
            865,
            869,
            871,
            877,
            916,
            924,
            929,
            934,
            941,
            942,
            943,
            944,
            949,
            954,
            955,
            956,
            961,
            984,
            992,
            1051,
        ]
        thrillerGenre = [
            155,
            55,
            59,
            63,
            77,
            78,
            82,
            83,
            93,
            104,
            111,
            116,
            117,
            150,
            161,
            163,
            169,
            170,
            179,
            180,
            182,
            184,
            186,
            187,
            189,
            192,
            213,
            214,
            218,
            223,
            231,
            234,
            241,
            242,
            251,
            267,
            274,
            275,
            277,
            280,
            281,
            288,
            296,
            298,
            299,
            302,
            303,
            319,
            320,
            322,
        ]
        adventureGenre = [
            18,
            22,
            58,
            62,
            74,
            79,
            85,
            87,
            89,
            95,
            97,
            98,
            105,
            106,
            118,
            120,
            121,
            122,
            134,
            146,
            152,
            154,
            157,
            165,
            168,
            172,
            173,
            174,
            175,
            193,
            196,
            199,
            200,
            201,
            217,
            244,
            246,
            253,
            254,
            285,
            329,
            330,
            331,
            332,
            395,
            411,
            421,
            435,
            468,
        ]

        # 공포
        if genre_pk == 27:
            serializer = genre_serach(serializer.data, thrillerGenre)
        # 코미디
        if genre_pk == 35:
            serializer = genre_serach(serializer.data, comedyGenre)
        # 모험
        if genre_pk == 12:
            serializer = genre_serach(serializer.data, adventureGenre)
        # 액션
        if genre_pk == 28:
            serializer = genre_serach(serializer.data, actionGenre)
        return Response(serializer)


def genre_serach(lst, genre):
    fetch_data = []

    for data in lst:
        if data["pk"] in genre:
            tmp = {
                "pk": 0,
                "title": "",
                "overview": "",
                "poster_path": "",
                "release_date": "",
            }
            tmp["pk"] = data["pk"]
            tmp["title"] = data["title"]
            tmp["overview"] = data["overview"]
            tmp["poster_path"] = data["poster_path"]
            tmp["release_date"] = data["release_date"]
            fetch_data.append(tmp)

    return fetch_data


# user가 add list 한 목록
@api_view(["POST"])
def add_list(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    else:
        movie.like_users.add(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


# 영화 평론 create
@api_view(["GET", "POST"])
def article_list_or_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    def article_list():
        sort = request.GET.get('sort', 'popular')
        articles = Article.objects.filter(movie_id=movie_pk)
        # 최신순 또는 인기순으로 구분 코드 추가
        if sort == 'recent':
            articles = articles.order_by('-created_at')
        else:
            articles = articles.annotate(likes_count=Count("like_users")).order_by('-likes_count')

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def create_article():
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == "POST":
        return create_article()
    elif request.method == "GET":
        return article_list()


@api_view(["GET", "POST", "PUT", "DELETE"])
def articles_get_or_update_or_delete(request, movie_pk, article_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    article = get_object_or_404(Article, pk=article_pk)

    def update_rating():
        if request.user == article.user:
            serializer = ArticleSerializer(instance=article, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                articles = movie.articles.all()
                serializer = ArticleSerializer(articles, many=True)
                return Response(serializer.data)

    def delete_rating():
        if request.user == article.user:
            article.delete()
            articles = movie.articles.all()
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data)

    def get_article():
        serializer = UserArticleSerializer(article)
        return Response(serializer.data)

    def like_article():
        if article.like_users.filter(pk=user.pk).exists():
            article.like_users.remove(user)
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        else:
            article.like_users.add(user)
            serializer = ArticleSerializer(article)
            return Response(serializer.data)

    if request.method == "PUT":
        return update_rating()
    elif request.method == "DELETE":
        return delete_rating()
    elif request.method == "GET":
        return get_article()
    elif request.method == "POST":
        return like_article()


@api_view(["GET", "POST"])
def get_create_comment(request, movie_pk, article_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == "GET":
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article, user=user)
            comments = article.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def delete_comment(request, movie_pk, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user == comment.user:
        comment.delete()
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_article(request, movie_pk, article_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    article = get_object_or_404(Article, pk=article_pk)

    if article.like_users.filter(pk=user.pk).exists():
        article.like_users.remove(user)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    else:
        article.like_users.add(user)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def genre_movies(request, genre_id):
    limit = request.GET.get('limit')  # 쿼리 파라미터로 limit 받기
    movies = Movie.objects.filter(genres__id=genre_id)
    if limit:
        movies = movies[:int(limit)]
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def all_movies(request):
    movies = Movie.objects.all()
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def chatbot(request):
    user_message = request.data.get('message')

    if not user_message:
        return Response({'error': '메시지를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': user_message}],
            temperature=0.7,
        )
        bot_reply = response.choices[0].message.content
        return Response({'reply': bot_reply})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# ✅ 커뮤니티 게시글 목록 조회 & 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def community_post_list_create(request):
    if request.method == 'GET':
        posts = CommunityPost.objects.all().order_by('-created_at')
        serializer = CommunityPostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommunityPostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ 커뮤니티 게시글 수정 & 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def community_post_update_delete(request, post_pk):
    post = get_object_or_404(CommunityPost, pk=post_pk)

    if request.method == 'GET':
        serializer = CommunityPostSerializer(post, context={'request': request})
        return Response(serializer.data)

    if post.user != request.user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = CommunityPostSerializer(post, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

## 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like_post(request, post_pk):
    post = get_object_or_404(CommunityPost, pk=post_pk)
    user = request.user

    if user in post.like_users.all():
        post.like_users.remove(user)
        liked = False
    else:
        post.like_users.add(user)
        liked = True

    return Response({
        'liked': liked,
        'like_count': post.like_users.count()
    })



# ✅ 커뮤니티 게시글 좋아요 토글
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def community_comment_list_create(request, post_pk):
    post = get_object_or_404(CommunityPost, pk=post_pk)

    if request.method == 'GET':
        comments = post.comments.all().order_by('created_at')
        serializer = CommunityCommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommunityCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def community_comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(CommunityComment, pk=comment_pk)

    if comment.user != request.user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def save_recommended_movies(request):
    saved = []

    for movie_data in request.data:
        tmdb_id = movie_data.get("id")
        if Movie.objects.filter(tmdb_id=tmdb_id).exists():
            continue

        movie = Movie.objects.create(
            tmdb_id=tmdb_id,
            title=movie_data.get("title", ""),
            overview=movie_data.get("overview", ""),
            budget=0,
            popularity=movie_data.get("popularity", 0),
            poster_path=movie_data.get("poster_path", ""),
            release_date=movie_data.get("release_date", None),
            revenue=0,
            runtime=None,
            tagline="",
            vote_average=movie_data.get("vote_average", 0),
            vote_count=movie_data.get("vote_count", 0),
        )
        saved.append(tmdb_id)

    return Response({"saved": saved})


@api_view(['GET'])
def top_rated_movies(request):
    k = 100  # 평점 참여 수 기준 (튜닝 가능)

    weighted_expr = ExpressionWrapper(
        (F('vote_average') * F('vote_count')) / (F('vote_count') + k),
        output_field=FloatField()
    )

    movies = (
        Movie.objects.annotate(weighted_score=weighted_expr)
        .order_by('-weighted_score')[:20]
    )

    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)