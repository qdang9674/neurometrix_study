<template>
    <div class="survey-wrapper">
      <div v-if="questions.length > 0">
        <div class="survey-card">
            <p>{{ currentQuestion.question_text }}</p>
            <div v-if="currentQuestion.question_type === 'multiple_choice'">
            <div v-for="(option, index) in currentQuestion.options" :key="index">
                <label>
                <input type="radio" :name="`question_${currentQuestion.question_id}`" :value="option" v-model="responses[currentQuestion.question_id]">
                {{ option }}
                </label>
            </div>
            </div>
            <div v-else-if="currentQuestion.question_type === 'textbox'">
            <input type="text" :placeholder="currentQuestion.question_text" v-model="responses[currentQuestion.question_id]" />
            </div>
        </div>
        <div class="navigation-buttons">
          <button @click="handlePrevious">
            {{ currentQuestionIndex === 0 ? 'Return to Survey List' : 'Previous' }}
          </button>
          <button @click="handleNext">
            {{ currentQuestionIndex === questions.length - 1 ? 'Submit' : 'Next' }}
          </button>
        </div>
      </div>
      <div v-else>
        <p>Loading questions...</p>
      </div>
    </div>
  </template>
  
  <script>
  // NOTE - this form is not used for the game surveys, thus difficulty is unused here.
  // game surveys are handled as an overlay dialog in game.vue
  import axios from 'axios';
  import { mapState } from "vuex";
  
  export default {
    data() {
      return {
        questions: [],
        currentQuestionIndex: 0,
        responses: {}
      };
    },
    props: {
      survey: String,
    },
    computed: {
      ...mapState({
        subjectId: (state) => state.subjectId,
        selectedEcgDevice: (state) => state.selectedEcgDevice,
      }),
      currentQuestion() {
        return this.questions[this.currentQuestionIndex];
      }
    },
    methods: {
      async fetchSurveyQuestions() {
        try {
          const res = await axios.get(process.env.VUE_APP_SURVEY_API_URL + '/surveys/' + this.survey + '/questions');
          this.questions = res.data
            .filter(question => question.active === true)
            .sort((a, b) => a.order - b.order);
        } catch (error) {
          console.error(error);
          this.$message.error('Failed to fetch survey questions');
        }
      },
      async handleNext() {
        if (this.currentQuestionIndex < this.questions.length - 1) {
          this.currentQuestionIndex++;
        } else {
          await this.submitSurvey();
        }
      },
      handlePrevious() {
        if (this.currentQuestionIndex === 0) {
          this.$emit('returnToSurveyList');
        } else {
          this.currentQuestionIndex--;
        }
      },
      async submitSurvey() {
        console.log('submitting survey')
        try {
          const answers = Object.keys(this.responses).map(questionId => ({
            question_id: questionId,
            answer: this.responses[questionId]
          }));
  
          const requestPayload = {
            user_id: this.subjectId,
            answers,
            difficulty_level: null // unused for presurveys
          };
  
          const res = await axios.post(process.env.VUE_APP_SURVEY_API_URL + '/surveys/' + this.survey + '/responses', requestPayload);
          console.log(res);
          this.$message.success('Survey submitted successfully');
          this.$emit('surveySubmitted');
        } catch (error) {
          console.error(error);
          this.$message.error('Failed to submit survey');
        }
      }
    },
    async mounted() {
      await this.fetchSurveyQuestions();
    }
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
    justify-content: space-between;
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
    transition: background-color 0.3s ease;
  }
  </style>
  