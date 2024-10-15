<template>
  <div id="navbar" v-if="subjectId">
    <button @click="toggleSidebar" id="toggle-sidebar-button">
        <i class="fas fa-bars"></i>
      </button>
    <span>Subject ID: <strong>{{ subjectId }}</strong></span>
    <div class="button-group">
      <SignalQualityStatus></SignalQualityStatus>
      <IotStatus></IotStatus>
      <button @click="goToHome" id="home-button">
        <i class="fas fa-house"></i>
      </button>
      <button @click="performLogout" id="logout-button">
        <i class="fas fa-sign-out-alt"></i>
      </button>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import SignalQualityStatus from './SignalQualityStatus.vue';
import IotStatus from './IotStatus.vue';
import '@fortawesome/fontawesome-free/css/all.css';

export default {
  components: {
    IotStatus,
    SignalQualityStatus
  },
  computed: {
    ...mapState(['subjectId'])
  },
  methods: {
    ...mapActions(['logout', 'goToHome', 'toggleSidebar']),
    performLogout() {
      this.logout();
    },
    goToHome() {
      this.$router.push('/');
    },
    toggleSidebar() {
      this.$store.commit('toggleSidebar')
    }
  }
};
</script>

<style scoped>
span {
  flex: 1;
  margin-left: 16px;
}

.button-group {
  display: flex;
  flex: 1;
  justify-content: flex-end;
  margin-right: 16px;
}

#toggle-sidebar-button, #logout-button, #home-button {
  padding: 0.5em 1em;
  color: rgba(200,200,200,1);
  background-color: rgba(255,255,255,0);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  margin-left: 8px;
  transition: background-color 0.3s ease;
}

#toggle-sidebar-button:hover, #logout-button:hover, #home-button:hover {
  background-color: rgba(255,255,255,0.3);
}
</style>
