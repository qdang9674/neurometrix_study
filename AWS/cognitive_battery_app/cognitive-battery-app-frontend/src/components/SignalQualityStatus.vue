<template>
  <div class="status-container">
    <p v-if="sensorStatus === 'ECG connected' && signalStrength !== -1" :style="{ color: signalColor }" class="status-text">{{ signalStrength }} dB</p>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  data() {
    return {
      signalStrength: 0,
    };
  },
  computed: {
    ...mapState(['sensorStatus']),
    signalColor() {
      return this.interpolateColor(this.signalStrength);
    },
  },
  mounted() {
    if (window.api && window.api.receive) {
      window.api.receive('fromMain', (data) => {
        if (data.signalStrength) {
          this.signalStrength = data.signalStrength;
        }
      });
    }
  },
  methods: {
    interpolateColor(signalStrength) {
      const startColor = { r: 255, g: 0, b: 0 };
      const endColor = { r: 0, g: 255, b: 0 };

      const minStrength = 0;
      const maxStrength = 4;

      const ratio = (signalStrength - minStrength) / (maxStrength - minStrength);
      const clampedRatio = Math.max(0, Math.min(ratio, 1));

      const r = Math.round(startColor.r + clampedRatio * (endColor.r - startColor.r));
      const g = Math.round(startColor.g + clampedRatio * (endColor.g - startColor.g));
      const b = Math.round(startColor.b + clampedRatio * (endColor.b - startColor.b));

      return `rgb(${r},${g},${b})`;
    },
  },
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

i {
  font-size: 18px;
}
</style>
