<template>
  <div id="app">
    <link href="https://fonts.googleapis.com/css2?family=Arimo:ital,wght@0,400..700;1,400..700&family=Dosis:wght@200..800&family=Inter:wght@100..900&family=Monda:wght@400..700&family=Montserrat:ital,wght@0,100..900;1,100..900&family=Red+Hat+Display:ital,wght@0,300..900;1,300..900&display=swap" rel="stylesheet">
    <transition name="fade">
      <Navbar v-if="showNavbarFooter && $route.name !== 'Sign In'" />
    </transition>
    <transition name="fade">
      <AdminSettings v-if="$route.name === 'Sign In'"/>
    </transition>
    <div :class="layoutClass">
      <Sidebar v-if="$route.name !== 'Sign In'" />
      <div class="content">
        <router-view @toggle-navbar-footer="toggleNavbarFooter"></router-view>
      </div>
    </div>
    <transition name="fade">
      <Footer v-if="showNavbarFooter && $route.name !== 'Sign In'" />
    </transition>
  </div>

  <div class="gradient-bg">
    <svg xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="goo">
          <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
          <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8" result="goo" />
          <feBlend in="SourceGraphic" in2="goo" />
        </filter>
      </defs>
    </svg>
    <div class="gradients-container">
      <div class="g1"></div>
      <div class="g2"></div>
      <div class="g3"></div>
      <div class="g4"></div>
      <div class="g5"></div>
      <div class="interactive"></div>
    </div>
  </div>
</template>

<script>
import Navbar from './components/navbar.vue';
import Sidebar from './components/Sidebar.vue';
import Footer from './components/Footer.vue';
import AdminSettings from './components/AdminSettings.vue';

export default {
  name: 'App',
  data() {
    return {
      showNavbarFooter: true
    };
  },
  components: {
    Sidebar,
    Navbar,
    Footer,
    AdminSettings
  },
  methods: {
    toggleNavbarFooter(show) {
      this.showNavbarFooter = show;
    }
  },
  computed: {
    layoutClass() {
      return this.$route.name === 'Sign In' ? 'layout signin-layout' : 'layout';
    }
  }
};
</script>

<style scoped>
#navbar, #footer {
  position: fixed;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0,0,0,0.2);
  backdrop-filter: blur(50px);
  font-size: 12px;
  height: 60px;
  filter: drop-shadow(2px 1px 2px rgba(0,0,0,0.1));
  z-index: 99;
}

#footer{
  bottom: 0px;
}

.layout {
  display: flex;
  height: 100vh;
}

.signin-layout {
  height: 100vh;
}

.content {
  flex: 1;
  overflow: auto;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
