<template>
  <div class="baseline-wrapper">
    <div class="baseline-container">
      <h1>Baseline</h1>
      <p>We will now record five minutes of resting activity. </p>
      <p>During this time, please sit comfortably and remain still. Ensure you sit up straight and avoid crossing your legs.</p>
      <router-link to="/video" class="baseline-button">Begin</router-link>
    </div>
  </div>
</template>

<style scoped>
.baseline-container {
  text-align: center;
  margin-bottom: 10%;
}
.baseline-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}
.baseline-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.baseline-button:hover {
  background-color: #339267;
}
</style>
