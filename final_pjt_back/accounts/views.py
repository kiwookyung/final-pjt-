from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated


# from django.db.models import Count

from .serializers import (
    ArticleMovieSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer,
    PasswordChangeSerializer,
)


User = get_user_model()


@api_view(["GET"])
def profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)

    articles = ProfileSerializer(user)

    return Response(articles.data)


@api_view(["GET"])
def like_num_of_article(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)

    articles = ProfileSerializer(user)
    like_count = 0
    for data in articles.data["articles"]:
        like_count += data["like_user_count"]

    print(like_count)
    return Response(like_count)


@api_view(["GET"])
def article_movie(request, movie_pk):
    movie = get_object_or_404(movie, pk=movie_pk)
    serializer = ArticleMovieSerializer(movie)
    return Response(serializer.data)


@api_view(["POST"])
# @permission_classes([AllowAny])
def follow(request, user_pk):
    profile_user = get_object_or_404(get_user_model(), pk=user_pk)
    me = request.user
    if me != profile_user:
        if me.followings.filter(pk=profile_user.pk).exists():
            me.followings.remove(profile_user)
        else:
            me.followings.add(profile_user)

    serializer = ProfileSerializer(profile_user)
    return Response(serializer.data)


#회원정보 수정
@api_view(["PUT"])
def update_profile(request, user_pk):
    profile_user = get_object_or_404(get_user_model(), pk=user_pk)
    me = request.user

    if me != profile_user:
        return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    serializer = ProfileUpdateSerializer(instance=profile_user, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)

#회원탈퇴
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    me = request.user

    if me != user:
        return Response({"detail": "본인만 탈퇴할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

    # 실제 삭제 대신 비활성화 처리
    user.is_active = False
    user.save()

    return Response({"detail": "회원 탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)


#비밀번호 변경
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "비밀번호가 성공적으로 변경되었습니다."})
    else:
        print(serializer.errors)  # 여기 추가
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['GET'])
def follow_status(request, user_pk):
    profile_user = get_object_or_404(get_user_model(), pk=user_pk)
    me = request.user
    if me.is_authenticated:
        is_following = me.followings.filter(pk=profile_user.pk).exists()
    else:
        is_following = False
    return Response({'is_following': is_following})