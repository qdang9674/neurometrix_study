<template>
  <div>
    <div class="sidebar-container" :class="{ collapsed: isSidebarCollapsed }">
      <ul :class="{ collapsed: isSidebarCollapsed }">
        <li
          v-for="route in filteredRoutes"
          :key="route.path"
          :class="{ active: isActiveRoute(route) }"
          @click="navigateTo(route.path)"
        >
        <i style="margin-left: 20px; margin-right: 32px" :class="route.meta.icon"></i>
          {{ capitalize((route.name === "Baseline Instructions" ? "Baseline" : route.name) || route.path) }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  data() {
    return {
      routes: [],
    };
  },
  computed: {
    ...mapState(['isSidebarCollapsed']),
    filteredRoutes() {
      return this.routes.filter(route => !route.meta.hidden);
    }
  },
  mounted() {
    this.routes = this.$router.getRoutes().filter(route => route.name);
  },
  methods: {
    isActiveRoute(route) {
      return this.$route.path === route.path;
    },
    navigateTo(path) {
      this.$router.push(path);
    },
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
    capitalize(str) {
      return str.charAt(0).toUpperCase() + str.slice(1);
    }
  }
};
</script>

<style scoped>
.sidebar-container {
  height: calc(100vh - 120px);
  top: 59px;
  width: 200px;
  background-color: rgba(0,0,0,0.4);
  backdrop-filter: blur(50px);
  position: absolute;
  transition: width 0.3s ease;
  margin-top: 1px;
  font-size: 12px;
  z-index: 1000;
}

.sidebar-container.collapsed {
  width: 0px;
}

ul {
margin-top: 0px;
  list-style-type: none;
  padding: 0;
  margin-left: 0;
  transition: margin-left 0.3s ease;
  background-color: rgba(255,255,255,0.1);
}

ul.collapsed {
  margin-left: -200px;
}

li {
  height: 60px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: left;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
  color: #b2b2b2;
}

li:hover {
  background-color: #42b98371;
}

li.active {
  background-color: #42b983;
  color: white;
}

</style>
