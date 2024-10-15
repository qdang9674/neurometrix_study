import { createRouter, createWebHistory } from 'vue-router';
import Signin from '@/views/signin/signin.vue';
import Home from '@/views/home/home.vue';
import Presurvey from '@/views/presurvey/presurveys.vue';
import Setup from '@/views/setup/setup.vue';
import Baseline from '@/views/baseline/baseline.vue';
import Video from '@/views/baseline/video.vue';
import Instructions from '@/views/game/instructions.vue';
import GameView from '@/views/game/game.vue';
import store from '@/store/store.js';

const routes = [
  {
    path: '/',
    name: 'Welcome',
    component: Home,
    meta: { requiresAuth: true, icon: 'fas fa-house' }
  },
  {
    path: '/signin',
    name: 'Sign In',
    component: Signin,
    meta: { hidden: true }
  },
  {
    path: '/setup',
    name: 'Setup',
    component: Setup,
    meta: { requiresAuth: true, icon: 'fas fa-sliders' }
  },
  {
    path: '/baseline',
    name: 'Baseline Instructions',
    component: Baseline,
    meta: { requiresAuth: true, icon: 'fas fa-chart-line' }
  },
  {
    path: '/video',
    name: 'Baseline',
    component: Video,
    meta: { requiresAuth: true, hidden: true }
  },
  {
    path: '/instructions',
    name: 'Instructions',
    component: Instructions,
    meta: { requiresAuth: true, hidden: true }
  },
  {
    path: '/game',
    name: 'Game',
    component: GameView,
    meta: { requiresAuth: true, icon: 'fas fa-gamepad' }
  },
  {
    path: '/surveys',
    name: 'Surveys',
    component: Presurvey,
    meta: { requiresAuth: true, icon: 'fas fa-square-poll-horizontal' }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const loggedIn = !!localStorage.getItem('user');
  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/signin');
  } else {
    store.commit('setCurrentTask', to.name);
    next();
  }
});

export default router;
