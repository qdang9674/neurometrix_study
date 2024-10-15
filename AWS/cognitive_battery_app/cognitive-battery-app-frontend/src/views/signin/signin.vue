<template>
  <div class="signin-wrapper">
    <div :class="signinContainerClass">
      <h1>Hello</h1>
      <p>Please enter your subject ID.</p>
      <input v-model="subjectId" type="text" id="subject-id" placeholder="Subject ID">
      <button @click="signIn" class="signin-button">Sign In</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      subjectId: '',
      errorMessage: '',
      signinContainerClass: 'signin-container-hidden'
    };
  },
  mounted() {
    setTimeout(() => {
      this.signinContainerClass = 'signin-container';
    }, 100);
  },
  methods: {
    ...mapActions(['login']),
    signIn() {
      if (this.subjectId.trim() === '') {
        this.errorMessage = 'Subject ID cannot be empty';
      } else {
        this.errorMessage = '';
        this.signinContainerClass = 'signin-container-hidden';
        setTimeout(() => {
          this.login(this.subjectId).then(() => {
            window.api.send('toMain', { command: 'setup-iot' });
            this.$router.push('/');
          });
        }, 1000); // delay pushing to home route. allows fadeout to finish
      }
    }
  }
};
</script>

<style scoped>
.signin-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.signin-container-hidden {
  text-align: center;
  margin-bottom: 10%;
  opacity: 0;
  transition: opacity 0.5s ease-in-out;
}

.signin-container {
  text-align: center;
  margin-bottom: 10%;
  opacity: 1;
  transition: opacity 0.5s ease-in-out;
}

.signin-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
  border: none;
  font-family: "Monda", sans-serif;
}

input {
  width: 120px;
  margin-right: 8px;
  font-family: "Monda", sans-serif;
  background-color: rgba(0,0,0,0.1);
  color: rgba(215,215,215,1);
  outline: none;
  border: none;
  height: 28px;
  padding: 8px;
  border-radius: 8px;
}

.signin-button:hover {
  background-color: #339267;
  cursor: pointer;
}

.error {
  color: red;
}
</style>
