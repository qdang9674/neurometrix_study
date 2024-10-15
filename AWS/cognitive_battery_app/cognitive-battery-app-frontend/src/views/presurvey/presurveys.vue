<template>
  <div class="presurvey-wrapper">
    <h1 style="text-align: center; cursor: pointer;">
      Surveys
    </h1>

    <p v-if="!this.currentSurvey">Please complete the following surveys.</p>
<!-- 
    <div class="survey-list" v-if="!this.currentSurvey">
      <div 
        class="survey-card" 
        v-for="survey in surveys" 
        :key="survey.survey_id"
        :class="{
          'survey-card--gray': !selectedSurveys.includes(survey.survey_id) && !completedSurveys.includes(survey),
          'survey-card--green': completedSurveys.includes(survey),
          'survey-card--white': selectedSurveys.includes(survey.survey_id) && !completedSurveys.includes(survey)
        }"
      >
        <div>
          <input 
            type="checkbox" 
            :id="`checkbox-${survey.survey_id}`" 
            :value="survey.survey_id" 
            v-model="selectedSurveys" 
            :disabled="completedSurveys.includes(survey)">
          <label :for="`checkbox-${survey.survey_id}`">{{ survey.title }}</label>
        </div>
        
        <button class="start-survey-button"
          style="margin-left: 16px; border-radius: 8px; border: none" 
          @click="startSurvey(survey)" 
          v-if="!completedSurveys.includes(survey) && selectedSurveys.includes(survey.survey_id)"
        >
          Start
        </button>
        
        <i 
          style="margin-left: 16px" 
          v-else-if="completedSurveys.includes(survey)" 
          class="fa-regular fa-circle-check"
          :class="{'icon--green': completedSurveys.includes(survey)}"
        ></i>
      </div>
    </div>

    <div v-else>
      <PreSurveyForm :survey="currentSurvey" :instructions="currentInstructions" @returnToSurveyList="handleReturnToSurveyList" @surveySubmitted="handleSurveySubmitted" />
    </div>
    -->

    <!-- START temporary block - this is for temporary qualtrics surveys -->
    <div class="survey-list" v-if="!this.currentSurvey">
      <div 
        class="survey-card" 
        v-for="survey in qualtricsSurveys" 
        :key="survey.survey_id"
        :class="{
          'survey-card--gray': !selectedSurveys.includes(survey.survey_id) && !completedSurveys.includes(survey),
          'survey-card--green': completedSurveys.includes(survey),
          'survey-card--white': selectedSurveys.includes(survey.survey_id) && !completedSurveys.includes(survey)
        }"
      >
        <div>
          <input 
            type="checkbox" 
            :id="`checkbox-${survey.survey_id}`" 
            :value="survey.survey_id" 
            v-model="selectedSurveys" 
            :disabled="completedSurveys.includes(survey)">
          <label :for="`checkbox-${survey.survey_id}`">{{ survey.title }}</label>
        </div>
        
        <button class="start-survey-button"
          style="margin-left: 16px; border-radius: 8px; border: none" 
          @click="startQualtricsSurvey(survey)" 
          v-if="!completedSurveys.includes(survey) && selectedSurveys.includes(survey.survey_id)"
        >
          Start
        </button>
        
        <i 
          style="margin-left: 16px" 
          v-else-if="completedSurveys.includes(survey)" 
          class="fa-regular fa-circle-check"
          :class="{'icon--green': completedSurveys.includes(survey)}"
        ></i>
      </div>
    </div>
    <!-- END temporary block -->

    <div v-if="!this.currentSurvey" class="survey-buttons">
      <button @click="performLogout" :disabled="!canContinue">Finish Study</button>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import { mapActions } from 'vuex';
//import PreSurveyForm from './components/PreSurveyForm.vue';

export default {
  components: {
    //PreSurveyForm
  },
  data() {
    return {
      surveys: [],
      completedSurveys: [],
      selectedSurveys: [],
      currentSurvey: null,
      currentInstructions: '',

      // temporary hardcoded qualtrics surveys, can be deleted later
      qualtricsSurveys: [
        {
          survey_id: 0,
          title: "The Resilience Scale",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_dhC8Z81ZMRdCmzk"
        },
        {
          survey_id: 1,
          title: "The Perceived Stress Scale",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_bNpQASxWd39gsBg"
        },
        {
          survey_id: 2,
          title: "Stress Reducing Activities Inventory Neurometryx",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_0ILDLifRR3k1tum"
        },
        {
          survey_id: 3,
          title: "State-Trait Anxiety Questions 2024",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_6mJwEoXCAmv1ZpY"
        },
        {
          survey_id: 4,
          title: "Positive and Negative Affect Scale",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_ddtEPJESds5BTUi"
        },
        {
          survey_id: 5,
          title: "Pittsburgh Sleep Quality Index",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_39mmQ0OrUAVg2lU"
        },
        {
          survey_id: 6,
          title: "PATIENT HEALTH QUESTIONNAIRE (PHQ-9)",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_8laphUHrWVqyQh8"
        },
        {
          survey_id: 7,
          title: "Neurometryx Video Feedback",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_2a9ubKGNhE2X7ds"
        },
        {
          survey_id: 8,
          title: "Multidimensional Assessment of Interoceptive Awareness",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_6Ejla27SN8FtRQi"
        },
        {
          survey_id: 9,
          title: "Kessler Psychological Distress Scale (K10)",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_6YIU0fOkSg6D3nw"
        },
        {
          survey_id: 10,
          title: "Generalized Anxiety Disorder GAD-7",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_3pGfpc8x1sZT7Nk"
        },
        {
          survey_id: 11,
          title: "Effort Reward Imbalance Scale",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_8um9E8nJU3s9Cdg"
        },
        {
          survey_id: 12,
          title: "Demographic Inventory Neurometryx",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_3UdRUSatk9TZEfY"
        },
        {
          survey_id: 13,
          title: "Copenhagen Burnout Inventory (CBI)",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_77i4stDeoH6mlQG"
        },
        {
          survey_id: 14,
          title: "Contemplative Practices Behavior Inventory Neurometryx",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_9REdJ1YLGu4S6iy"
        },
        {
          survey_id: 15,
          title: "Cognitive and Affective Mindfulness Scale Revised",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_d0SbU9RASldqA86"
        },
        {
          survey_id: 16,
          title: "Barratt Impulsiveness Scale - 11",
          url: "https://umbc.co1.qualtrics.com/jfe/form/SV_bskPaoMoOSdD34a"
        }
      ]
    }
  },
  computed: {
    canContinue() {
      return this.selectedSurveys.every(surveyId => 
        this.completedSurveys.some(completedSurvey => completedSurvey.survey_id === surveyId)
      );
    }
  },
  methods: {
    ...mapActions(['logout']),
    performLogout() {
      this.$message.success("Thank you for your participation.")
      this.logout();
    },
    async fetchAllSurveys() {
      try {
        const res = await axios.get(process.env.VUE_APP_SURVEY_API_URL + '/surveys');
        console.log(res.data);
        this.surveys = res.data.filter(survey => survey.active === true && survey.order === 'Pre-Assessment');
      } catch (error) {
        console.error(error);
        this.$message.error('Failed to fetch surveys');
      }
    },
    startSurvey(survey) {
      this.currentSurvey = survey.survey_id;
      this.currentInstructions = survey.instructions;
    },
    handleReturnToSurveyList() {
      this.currentSurvey = null;
      this.currentInstructions = '';
    },
    handleSurveySubmitted() {
      const completedSurvey = this.surveys.find(survey => survey.survey_id === this.currentSurvey);
      if (!this.completedSurveys.includes(completedSurvey)) {
        this.completedSurveys.push(completedSurvey);
      }
      this.currentSurvey = null;
      this.currentInstructions = '';
    },

    //temp function for qualtrics - can be deleted later
    startQualtricsSurvey(survey) {
      const surveyWindow = window.open(survey.url, "_blank");
      const checkWindowClosed = setInterval(() => {
        if (surveyWindow.closed) {
          clearInterval(checkWindowClosed);
          if (!this.completedSurveys.includes(survey)) {
            this.completedSurveys.push(survey);
          }
        }
      }, 500); // check every 500ms if the window closed
    }
  },
  async mounted() {
    await this.fetchAllSurveys();
  }
};
</script>

<style scoped>
.presurvey-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.survey-buttons button {
  margin: 5px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  font-family: "Monda", sans-serif;
  transition: background-color 0.3s ease;
}

.survey-buttons button:disabled {
  cursor: not-allowed;
  background-color: #ddd;
}

button {
  font-family: "Monda", sans-serif;
}

.survey-list {
  max-width: 30vw;
  background-color: rgba(0,0,0,0.2);
  padding: 16px;
  border-radius: 16px;
  margin: 16px;
}

.survey-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 8px 0;
  transition: all 0.3s ease;
}

.survey-card--gray {
  color: gray;
}

.survey-card--green {
  color: #42b983;
}

.survey-card--white {
  color: white;
}

.icon--green {
  color: #42b983;
}

.start-survey-button{
  transition: background-color 0.1s ease;
}

.start-survey-button:hover{
  cursor: pointer;
  background-color: rgb(200,200,200);
}
</style>
