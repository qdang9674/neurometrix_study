<template>
  <div class="home-wrapper">
    <div :class="homeContainerClass">
      <h1>Welcome</h1>
      <p>Welcome to the study, and thank you for your participation.</p>
      <p>You will be guided through various preliminary steps before beginning the main experiment.</p>
      <router-link to="/setup" class="start-button">Start</router-link>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      homeContainerClass: 'home-container-hidden'
    };
  },
  mounted() {
    setTimeout(() => {
      this.homeContainerClass = 'home-container';
    }, 500);
  }
};
</script>

<style scoped>
.home-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.home-container {
  text-align: center;
  margin-bottom: 10%;
  opacity: 1.0;
  transition: opacity 2s ease;
}

.home-container-hidden {
  opacity: 0;
}

.start-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.start-button:hover {
  background-color: #339267;
}
</style>
