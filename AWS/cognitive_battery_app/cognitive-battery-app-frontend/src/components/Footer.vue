<template>
    <div id="footer">
      <Status class="status" />
    </div>
  </template>
  
  <script>
  import { mapState } from 'vuex';
  import Status from './DeviceStatus.vue'
  import '@fortawesome/fontawesome-free/css/all.css';
  
  export default {
    components: {
      Status
    },
    computed: {
      ...mapState(['subjectId', 'steps', 'currentStepIndex']),
    },
  };
  </script>
  
  <style scoped>
  #footer {
    align-items: center;
  }
  </style>
  