import { createRouter, createWebHistory } from "vue-router";

// 프로필 페이지
import UserInfo from "@/components/user/UserInfo.vue";
import UserPick from "@/components/user/UserPick.vue";
import UserArticle from "@/components/user/UserArticle.vue";
import UserFollower from "@/components/user/UserFollower.vue";
import CommunityView from "@/views/CommunityView.vue";
import CommunityCreateView from "@/views/CommunityCreateView.vue";
import CommunityDetailView from "@/views/CommunityDetailView.vue";
import CommunityEditView from "@/views/CommunityEditView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/views/IndexView.vue"),
    },
    {
      path: "/user/login",
      name: "userLogin",
      component: () => import("@/views/UserLoginView.vue"),
    },
    {
      path: "/user/signup",
      name: "userSignup",
      component: () => import("@/views/UserSignupView.vue"),
    },
    {
      path: "/user/profile/:userId",
      name: "userProfile",
      component: () => import("@/views/UserProfileView.vue"),
      beforeEnter: (to, from, next) => {
        const isCurrentUser =
          to.params.userId === window.localStorage.getItem("userPk");

        if (
          to.path.endsWith("info") ||
          to.path.endsWith("pick") ||
          to.path.endsWith("article") ||
          to.path.endsWith("follower")
        ) {
          next();
          return;
        }

        next(
          isCurrentUser
            ? `/user/profile/${to.params.userId}/info`
            : `/user/profile/${to.params.userId}/pick`
        );
      },
      children: [
        { path: "info", name: "userInfo", component: UserInfo },
        { path: "article", name: "UserArticle", component: UserArticle },
        { path: "pick", name: "UserPick", component: UserPick },
        { path: "follower", name: "UserFollower", component: UserFollower },
      ],
    },

    {
      path: "/logout",
      name: "logout",
      component: () => import("@/views/UserLogoutView.vue"),
    },
    // {
    //   path: '/movies',
    //   name: 'movies',
    //   component: () => import('@/views/MovieListView.vue')
    // },
    // {
    //   path: '/movies/recommended',
    //   name: 'recommended',
    //   component: () => import('@/views/RecommendedView.vue')
    // },
    {
      path: "/movies/:moviePk",
      name: "MovieDetailView",
      component: () => import("@/views/MovieDetailView.vue"),
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: () => import("@/views/NotFoundView.vue"),
    },
    {
      path: "/genre/:genreId",
      name: "GenreMoreView",
      component: () => import("@/views/GenreMoreView.vue"),
    },
    {
      path: "/search",
      name: "SearchView",
      component: () => import("@/views/SearchView.vue"),
    },
    {
      path: "/user/profile/:userId/edit",
      name: "userEdit",
      component: () => import("@/views/UserEditProfileView.vue"),
      beforeEnter: (to, from, next) => {
        // 본인만 접근 가능하도록 체크
        if (to.params.userId === window.localStorage.getItem("userPk")) {
          next();
        } else {
          alert("본인만 수정할 수 있습니다.");
          next(false);
        }
      },
    },

    // 비밀번호 변경
    {
      path: "/user/profile/:userId/change-password",
      name: "changePassword",
      component: () => import("@/components/user/PasswordChange.vue"),
      beforeEnter: (to, from, next) => {
        if (to.params.userId === window.localStorage.getItem("userPk")) {
          next();
        } else {
          alert("본인만 비밀번호를 변경할 수 있습니다.");
          next(false);
        }
      },
    },

    {
      path: "/community",
      name: "CommunityView",
      component: CommunityView,
    },
    // 커뮤니티 게시글 생성
    {
      path: "/community/create",
      name: "CommunityCreateView",
      component: CommunityCreateView,
    },
    // 커뮤니티 좋아요
    {
      path: "/community/:postId",
      name: "CommunityDetailView",
      component: CommunityDetailView,
      props: true,
    },
    // 커뮤니티 수정
    {
      path: "/community/edit/:postId",
      name: "CommunityEditView",
      component: CommunityEditView,
      props: true,
    },
  ],
});

export default router;
