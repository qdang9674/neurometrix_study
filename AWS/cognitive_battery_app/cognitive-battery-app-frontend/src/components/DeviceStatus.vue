<template>
  <div class="status-container" v-if="isRouteInList(['Setup', 'Baseline Instructions', 'Baseline', 'Instructions', 'Game'])">

    <!-- ecg icons and status message -->
    <i v-if="statusMessageECG === 'ECG connected'" class="fa-solid fa-heart-pulse"></i>
    <i v-else-if="statusMessageECG === 'Connecting ECG sensor...'" class="fa-solid fa-spinner fa-spin"></i>
    <i v-else-if="statusMessageECG === 'ECG disconnected'" class="fa-solid fa-heart-circle-xmark"></i>
    <i v-else class="fa-solid fa-heart-circle-exclamation" style="color: #ff5b5b"></i>
    <p :class="{'status-text': true, 'error-text': statusMessageECG !== 'ECG connected' && statusMessageECG !== 'Connecting ECG sensor...' && statusMessageECG !== 'ECG disconnected'}">{{ statusMessageECG }}</p>

    <!-- eye tracker icons and status message -->
    <i v-if="statusMessageEye === 'Eye tracker connected'" class="fa-regular fa-eye"></i>
    <i v-else-if="statusMessageEye === 'Connecting eye tracker...'" class="fa-solid fa-spinner fa-spin"></i>
    <i v-else-if="statusMessageEye === 'Eye tracker disconnected'" class="fa-solid fa-eye-low-vision"></i>
    <i v-else class="fa-regular fa-eye-slash" style="color: #ff5b5b"></i>
    <p :class="{'status-text': true, 'error-text': statusMessageEye !== 'Eye tracker connected' && statusMessageEye !== 'Connecting eye tracker...' && statusMessageEye !== 'Eye tracker disconnected'}">{{ statusMessageEye }}</p>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';

const retryTasks = ['Baseline Instructions', 'Baseline', 'Instructions', 'Game'];
const retryInterval = 3000;

export default {
  computed: {
    ...mapState({
      statusMessageEye: state => state.eyeStatus,
      statusMessageECG: state => state.sensorStatus,
      currentTask: state => state.currentTask
    })
  },
  watch: {
  // trigger eye tracker retry
  statusMessageEye(newStatus) {
    if (newStatus != 'Eye tracker connected' && newStatus != 'Connecting eye tracker...') {
      if (retryTasks.includes(this.currentTask)) {
        setTimeout(() => {
          this.statusMessageEye += 'Retrying';
          window.api.send('toMain', { command: 'setup-eye-tracker' });
        }, retryInterval);
      }
    }
  },
  // trigger ecg sensor retry
  statusMessageECG(newStatus) {
    if (newStatus != 'ECG connected' && newStatus != 'Connecting ECG sensor...') {
      if (retryTasks.includes(this.currentTask)) {
        setTimeout(() => {
          window.api.send('toMain', { command: 'setup-sensor' });
        }, retryInterval);
      }
    }
  }
},

  mounted() {
    if (window.api && window.api.receive) {
      window.api.receive('fromMain', (data) => {
        if (data.eyeStatus) {
          this.setEyeStatus(data.eyeStatus);
        } else if (data.eyeError) {
          this.setEyeStatus(`Error: ${data.eyeError}`);
        }

        if (data.sensorStatus) {
          this.setSensorStatus(data.sensorStatus);
        } else if (data.sensorError) {
          this.setSensorStatus(`Error: ${data.sensorError}`);
        }
      });
    }
  },
  methods: {
    ...mapMutations(['setEyeStatus', 'setSensorStatus']),
    isRouteInList(routeList) {
      return routeList.includes(this.$route.name);
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

.error-text {
  color: #ff5b5b;
}

i {
  font-size: 18px;
}
</style>
