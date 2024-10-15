<template>
  <div class="survey-wrapper">
    <p style="display: flex; justify-content: center; align-items: center; text-align:justify; max-width: 30vw">{{ instructions }}</p>
    <div v-if="currentQuestion">
      <div class="survey-card">
        <p>{{ currentQuestion.question_text }}</p>
        <div v-if="currentQuestion.question_type === 'multiple_choice'">
          <div v-for="(option, index) in currentQuestion.options" :key="index">
            <label>
              <input
                type="radio"
                :name="`question_${currentQuestion.question_id}`"
                :value="option"
                v-model="response"
                @change="handleOptionSelected"
              />
              {{ option }}
            </label>
          </div>
        </div>
        <div v-else-if="currentQuestion.question_type === 'textbox'">
          <input
            type="text"
            placeholder="Response"
            v-model="response"
          />
        </div>
        <div v-else-if="currentQuestion.question_type === 'slider'">
          <input
            type="range"
            :min="sliderMin"
            :max="sliderMax"
            :step="sliderStep"
            v-model="response"
          />
          <span>{{ response }}</span>
        </div>
      </div>
      <div class="navigation-buttons" v-if="showNextButton">
        <button style="width: 100px" @click="handleNext" :disabled="response === null || loading">
          <i v-if="loading" class="fas fa-spinner fa-pulse"></i>
          <span v-else>{{ remainingQuestions === 0 ? 'Submit' : 'Next' }}</span>
        </button>
      </div>
      <p style="color: gray">{{ remainingQuestions }} questions remaining</p>
    </div>
    <div v-else-if="remainingQuestions === 0">
      <p>Survey completed. Thank you!</p>
    </div>
    <div v-else>
      <p>Loading question...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from "vuex";

export default {
  data() {
    return {
      currentQuestion: null,
      response: null,
      loading: false,
      remainingQuestions: null,
      sliderMin: 0,
      sliderMax: 100,
      sliderStep: 1,
    };
  },
  props: {
    survey: String,
    instructions: String,
  },
  computed: {
    ...mapState({
      subjectId: (state) => state.subjectId,
    }),
    showNextButton() {
      return this.currentQuestion && this.currentQuestion.question_type !== 'multiple_choice';
    },
  },
  methods: {
    // POST to start survey and get first question
    async postFirstResponse() {
      try {
        this.loading = true;
        const surveyUrl = process.env.VUE_APP_SURVEY_API_URL + `/surveys/${this.survey}/responses`;
        const res = await axios.post(surveyUrl, {
          user_id: this.subjectId
        });

        if (res.data.question) {
          this.processQuestion(res.data.question);
          this.remainingQuestions = res.data.remaining_questions;
        } else {
          // No questions returned, survey might be complete
          this.currentQuestion = null;
          this.remainingQuestions = 0;
          this.$message.success('Survey submitted successfully');
          this.$emit('surveySubmitted');
        }
        this.response = null;
      } catch (error) {
        console.error('Failed to fetch the first question', error);
      } finally {
        this.loading = false;
      }
    },

    // PUT to submit answer and fetch next question
    async putNextResponse() {
      try {
        this.loading = true;
        const surveyUrl = process.env.VUE_APP_SURVEY_API_URL + `/surveys/${this.survey}/responses`;
        const res = await axios.put(surveyUrl, {
          user_id: this.subjectId,
          question_id: this.currentQuestion.question_id,
          answer: this.response
        });

        console.log(res)
        this.remainingQuestions = res.data.remaining_questions;

        if (res.data.question) {
          this.processQuestion(res.data.question);
          this.response = null;
        } else if (this.remainingQuestions === 0) {
          // Survey is complete
          this.currentQuestion = null;
          this.response = null;
          this.$message.success('Survey submitted successfully');
          this.$emit('surveySubmitted');
        } else {
          // Handle unexpected state
          console.warn('No more questions but remaining_questions is not zero.');
          this.currentQuestion = null;
        }
      } catch (error) {
        console.error('Failed to submit response and fetch the next question', error);
      } finally {
        this.loading = false;
      }
    },

    async handleNext() {
      if (this.response !== null && !this.loading) {
        await this.putNextResponse();
      }
    },

    async handleOptionSelected() {
      if (this.response !== null && !this.loading) {
        await this.putNextResponse();
      }
    },

    processQuestion(question) {
      if (!question) {
        return;
      }
      this.currentQuestion = question;
      if (question.question_type === 'slider') {
        // Parse options to numbers
        const options = question.options.map(opt => Number(opt));
        this.sliderMin = Math.min(...options);
        this.sliderMax = Math.max(...options);
        // Determine step if options are evenly spaced
        if (options.length > 1) {
          this.sliderStep = options[1] - options[0];
        } else {
          this.sliderStep = 1;
        }
        // Initialize response to min value
        this.response = this.sliderMin;
      } else {
        this.response = null;
      }
    },
  },
  watch: {
    currentQuestion(newQuestion) {
      if (newQuestion) {
        if (newQuestion.question_type === 'slider') {
          this.processQuestion(newQuestion);
        } else {
          this.response = null;
        }
      }
    }
  },
  async mounted() {
    await this.postFirstResponse();
  },
};
</script>

<style scoped>
  .survey-wrapper {
    margin: 20px;
  }

  .survey-card {
    width: 15vw;
    background-color: rgba(0,0,0,0.2);
    padding: 16px 32px 32px 32px;
    border-radius: 16px;
    margin: 16px;
  }

  .navigation-buttons {
    display: flex;
    justify-content: center;
    margin-top: 20px;
    margin-left: 12px;
    margin-right: 12px;
  }

  button {
    margin: 5px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    cursor: pointer;
    text-align: center;
    font-family: "Monda", sans-serif;
    transition: background-color 0.1s ease;
  }

  button:hover:not(:disabled) {
    background-color: rgb(200, 200, 200);
  }

  button:disabled {
    cursor: not-allowed;
  }
</style>
