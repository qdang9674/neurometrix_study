<template>
    <div class="status-container">
      <!-- conditionally render an icon - cant change class dynamically -->
      <i v-if="iotStatus === 'Online'" class="fa-solid fa-globe"></i>
      <i v-if="iotStatus === 'Reconnecting...'" class="fas fa-spinner fa-pulse"></i>
      <i v-if="iotStatus === 'Connection closed'" class="fa-solid fa-triangle-exclamation"></i>
      <i v-if="iotStatus === 'Offline'" class="fa-regular fa-moon"></i>
      <p class="status-text">{{ iotStatus }}</p>
      <i v-if="iotStatus === 'Offline'" class="retry fa-solid fa-rotate-right" @click="retryConnection"></i>
    </div>
  </template>
  
  <script>
  import { mapState } from 'vuex';
  
  export default {
    computed: {
      ...mapState(['iotStatus'])
    },
    methods: {
      isRouteInList(routeList) {
        return routeList.includes(this.$route.name);
      },
      retryConnection() {
        window.api.send('toMain', { command: 'setup-iot' });
      }
    }
  };
  </script>
  
  <style scoped>
  .status-container {
    display: flex;
    align-items: center;
  }
  
  .status-text {
    margin-left: 8px;
    margin-right: 16px;
  }

  .retry{
    margin-left: 0px;
    margin-right: 8px;
    transition: color 0.3s ease;
  }

  .retry:hover{
    cursor: pointer;
    color: rgba(230,230,230,0.5);
  }

  i{
    font-size: 18px;
  }


  </style>
  