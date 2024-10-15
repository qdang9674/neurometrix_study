<template>
  <div class="setup-wrapper">
    <div :class="['setup-container', { 'setup-centered': currentStepIndex === 0 }]">
      <h1>Setup</h1>
      <div class="content">
        <div class="step-content" v-if="currentStep">
          <!-- Step 1: ECG device selection -->
          <div style="margin-top: -32px; margin-bottom: 32px" v-if="currentStepIndex === 0"><p style="color: rgb(180, 180, 180)">Select the device being used for this study.</p></div>
          <div v-if="currentStepIndex === 0" class="device-instructions">
            
            <div @click="selectEcgDevice('arduino')" :class="['device', { 'grayed-out': selectedEcgDevice !== 'arduino' }]">
              <button  :class="{ active: selectedEcgDevice === 'arduino' }">3-Lead ECG</button>
              <img src="images/ecg-diagram.png" alt="3-Lead ECG Device Setup" class="step-image">
              <p style="color: rgba(80,80,80,1)">Attach the three electrodes as shown in the diagram.</p>
            </div>
            <div @click="selectEcgDevice('movesense')" :class="['device', { 'grayed-out': selectedEcgDevice !== 'movesense' }]">
              <button :class="{ active: selectedEcgDevice === 'movesense' }">Movesense MD Sensor</button>
              <img src="images/movesense.jpg" alt="Movesense ECG Device Setup" class="step-image">
              <p style="color: rgba(80,80,80,1)">Wrap the strap around your chest, ensuring the electrodes make firm contact with your skin.</p>
            </div>
            <!-- <div @click="selectEcgDevice('ecg3')" :class="['device', { 'grayed-out': selectedEcgDevice !== 'ecg3' }]">
              <button :class="{ active: selectedEcgDevice === 'ecg3' }">ECG Device 3</button>
              <img src="https://placehold.jp/500x500.png" alt="ECG Device 3" class="step-image">
              <p style="color: rgba(80,80,80,1)">(insert directions for ECG device here)</p>
            </div> -->
          </div>

          <!-- Step 2: signal quality check -->
          <div v-else-if="currentStepIndex === 1">
            <p style="margin-top: -16px; margin-bottom: 32px; color: rgb(180, 180, 180)">Please wait while a research assistant checks the signal quality.</p>
            <p style="color: #42b983" v-if="!renderConnectButton() && (this.eyeStatus === 'Eye tracker connected' && this.sensorStatus === 'ECG connected')"><i style="margin-right: 8px" class="fa-regular fa-circle-check"/>ECG and eye tracker connected successfully.</p>
            <p v-else-if="!renderRetryButton()"><i style="margin-right: 8px" class="fas fa-spinner fa-spin"/>Connecting devices...</p>
            <p style="color: #e9b453" v-else-if="renderRetryButton()"><i style="margin-right: 8px;" class="fas fa-exclamation-triangle"/>There was an error connecting one or more devices. Please try again.</p>
          </div>

          <!-- other steps -->
          <div v-else>
            <p>{{ currentStep.instructions }}</p>
            <div v-if="currentStep.image">
              <img :src="currentStep.image" alt="Step Image" class="step-image">
            </div>
          </div>

          <div class="navigation-buttons">
            <button v-if="currentStepIndex !== 0" @click="previousStep" :disabled="currentStepIndex === 0">Previous</button>
            <button class="connect-button" v-if="currentStepIndex === steps.length - 1" @click="nextStepOrComplete">Complete</button>
            <button v-else-if="currentStepIndex !== 1 || (currentStepIndex === 1 && !renderRetryButton())" @click="nextStepOrComplete" :disabled="!isNextButtonEnabled">Next</button>
            <button v-if="renderRetryButton() && currentStepIndex == 1" class="connect-button" @click="signalQualityCheck()">Retry</button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  data() {
    return {
      currentStepIndex: 0,
      steps: [
        {
          title: 'ECG Setup',
          instructions: ''
        },
        {
          title: 'Signal Quality Check',
          image: '',
          instructions: 'Please wait while a research assistant checks the signal quality.'
        },
        {
          title: 'Eye Tracking Calibration',
          image: '',
          instructions: 'A research assistant will guide you through the eye tracking calibration process.'
        }
      ]
    };
  },
  computed: {
    ...mapState({
      subjectId: state => state.subjectId,
      selectedEcgDevice: state => state.selectedEcgDevice,
      eyeStatus: state => state.eyeStatus,
      sensorStatus: state => state.sensorStatus
    }),
    currentStep() {
      return this.steps[this.currentStepIndex];
    },
    isNextButtonEnabled() {
      if (this.currentStepIndex === 0) {
        return this.selectedEcgDevice;
      }
      if (this.currentStepIndex === 1) {
        return this.sensorStatus === 'ECG connected' && this.eyeStatus === 'Eye tracker connected';
      }
      return true;
    }
  },
  watch: {
  currentStep() {
    switch (this.currentStepIndex) {
      case 0:
        this.disconnectDevices();
        break;
      case 1:
        this.signalQualityCheck();
        break;
    }
  }
},
  methods: {
    ...mapActions(['selectEcgDevice']),
    openStep(index) {
      this.currentStepIndex = index;
    },
    nextStep() {
      if (this.currentStepIndex < this.steps.length - 1) {
        this.currentStepIndex += 1;
      }
    },
    previousStep() {
      if (this.currentStepIndex > 0) {
        this.currentStepIndex -= 1;
      }
    },
    nextStepOrComplete() {
      if (this.currentStepIndex === this.steps.length - 1) {
        this.completeSetup();
      } else {
        this.nextStep();
      }
    },
    completeSetup() {
      this.$router.push('/baseline');
    },
    async signalQualityCheck() {
      const selectedEcgDevice = this.$store.state.selectedEcgDevice;
      const subjectId = this.$store.state.subjectId;
      // send a msg to main process to start processes
      window.api.send('toMain', { command: 'start-data-collection', subjectId, device: selectedEcgDevice, task: 'signal-quality-check' });

      // receive data from main - maybe some sort of indication of signal quality if possible?
      // update 9/20/24 this is being done in SignalQualityStatus.vue
      // await window.api.receive('fromMain', (data) => {
      //   console.log(data);
      // });
    },
    async disconnectDevices() {
      window.api.send('toMain', { command: 'stop-data-collection' });
    },
    renderConnectButton(){
      if (this.eyeStatus !== 'Eye tracker connected' && this.eyeStatus !== 'Connecting eye tracker...')
        if (this.sensorStatus !== 'ECG connected' && this.sensorStatus !== 'Connecting ECG sensor...')
          return true;
      return false;
    },
    renderRetryButton(){
      if ((this.eyeStatus !== 'Eye tracker connected' && this.eyeStatus !== 'Connecting eye tracker...') || (this.sensorStatus !== 'ECG connected' && this.sensorStatus !== 'Connecting ECG sensor...'))
        return true;
      return false;
    }
  },
  mounted() {
    this.disconnectDevices();
    this.openStep(0);
  }
};
</script>

<style scoped>
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}

.setup-wrapper {
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.setup-container {
  padding: 1em;
  display: flex;
  flex-direction: column;
  margin-bottom: 10%;
}

.setup-centered {
  margin-bottom: 0%;
}

.content {
  display: flex;
  flex-grow: 1;
  margin-bottom: 20px;
}

.sidebar {
  width: 300px;
  background-color: #3f4346;
  color: white;
  padding: 1em;
  border-radius: 5px;
}

.step-list {
  list-style-type: none;
  padding: 0;
}

.step-list li {
  margin: 0.5em 0;
}

.step-list a {
  text-decoration: none;
  color: rgb(233, 180, 83);
}

.step-list li.active a {
  color: #fff;
}

.navigation-buttons {
  margin-top: 20px;
}

.navigation-buttons button {
  margin: 5px;
  padding: 10px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  width: 100px;
  text-align: center;
  font-family: "Monda", sans-serif;
  transition: background-color 0.2s ease;
}

.navigation-buttons button:hover:not(.connect-button) {
  background-color: #a3a3a3;
}

.navigation-buttons button:disabled {
  background-color: rgba(255, 255, 255, 0.3);
}

.navigation-buttons button:disabled:hover {
  cursor: not-allowed;
  background-color: rgba(255, 255, 255, 0.3);
}

.step-content {
  flex-grow: 1;
  width: 60vw;
}

.device-instructions {
  display: flex;
  justify-content: center;
  gap: 20px;
  font-size: 14px;
}

.device {
  flex: 1;
  padding: 10px;
  border: 6px solid #42b983;
  border-radius: 16px;
  text-align: center;
  background: white;
  transition: opacity 0.3s ease, border 0.3s ease;
  max-width: 500px;
}

.grayed-out:hover {
  cursor: pointer;
  opacity: 0.5;
}

.device button {
  margin-bottom: 10px;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
}

.device button.active {
  background-color: #42b983;
  color: white;
}

.grayed-out {
  border: 6px solid white;
  opacity: 0.35;
}

.step-image {
  max-width: 100%;
  height: auto;
}

button {
  font-family: "Monda", sans-serif;
}

.connect-button {
  margin: 5px;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100px;
  text-align: center;
  font-family: "Monda", sans-serif;
  background-color: #42b983;
  color: white;
  transition: background-color 0.3s ease;
}

.connect-button:hover {
  background-color: #339267;
  cursor: pointer;
}
</style>
