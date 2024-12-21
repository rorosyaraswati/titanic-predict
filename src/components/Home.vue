<template>
  <div>
    <!-- Header Image Section -->
    <div class="relative">
      <img :src="titanicImage" alt="Titanic" class="w-full h-64 object-cover" />
      <div class="absolute inset-0 bg-gradient-to-t from-black to-transparent opacity-70"></div>
      <h2 class="absolute bottom-4 left-4 text-white text-3xl font-bold">
        Welcome to Titanic Prediction App
      </h2>
    </div>

    <!-- Enhanced Model Information Section -->
    <div class="mt-10">
  <h3 class="text-2xl font-semibold text-center mb-6">Model Information: Logistic Regression Model</h3>
  
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-6xl mx-auto p-4">
      
        <!-- Model Parameters -->
        <div class="bg-white shadow rounded-lg p-6">
          <h4 class="text-xl font-semibold mb-4">Model Parameters</h4>
          <div v-if="modelInfo.model_parameters">
            <div v-for="(value, param) in modelInfo.model_parameters" :key="param" 
                 class="mb-2 flex justify-between">
              <span class="capitalize">{{ param }}:</span>
              <span>{{ typeof value === 'number' ? value.toFixed(4) : value }}</span>
            </div>
          </div>
          <div v-else>Loading parameters...</div>
        </div>

        <!-- Coefficients -->
        <div class="bg-white shadow rounded-lg p-6">
          <h4 class="text-xl font-semibold mb-4">Model Coefficients</h4>
          <div v-if="modelInfo.coefficients">
            <div v-for="(value, feature) in modelInfo.coefficients" :key="feature" 
                 class="mb-2 flex justify-between">
              <span>{{ feature }}:</span>
              <span>{{ value.toFixed(4) }}</span>
            </div>
          </div>
          <div v-else>Loading coefficients...</div>
        </div>
      </div>

      <!-- Feature Importance Visualization -->
      <div class="mt-10 mx-auto max-w-6xl p-4">
        <h4 class="text-xl font-semibold mb-4">Feature Importance</h4>
        <canvas ref="featureChart"></canvas>
      </div>

      <!-- Prediction Threshold -->
      <div class="mt-6 mx-auto max-w-6xl p-4">
        <div class="bg-white shadow rounded-lg p-6">
          <h4 class="text-xl font-semibold mb-4">Prediction Threshold</h4>
          <p>Current threshold: {{ modelInfo.threshold || 0.5 }}</p>
          <p class="text-sm text-gray-600 mt-2">
            This is the probability threshold used to classify predictions as survived (1) or not survived (0).
          </p>
        </div>
      </div>
    </div>

    <!-- Team Section -->
    <div class="mt-10">
      <h3 class="text-2xl font-semibold text-center mb-4">Meet Our Team</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-6xl mx-auto p-4">
        <div v-for="(member, index) in team" :key="index" 
             class="bg-white shadow rounded-lg p-6 text-center">
          <img :src="member.photo" 
               :alt="`Photo of ${member.name}`"
               class="rounded-full mx-auto mb-4 w-32 h-32 object-cover"
               @error="handleImageError($event)" />
          <h4 class="text-xl font-semibold">{{ member.name }}</h4>
          <p class="text-gray-600">{{ member.role }}</p>
          <div class="mt-4 space-x-4">
            <a :href="member.github" target="_blank" class="text-blue-500 hover:text-blue-700">
              GitHub
            </a>
            <a :href="member.linkedin" target="_blank" class="text-blue-500 hover:text-blue-700">
              LinkedIn
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'
import axios from 'axios'

export default {
  data() {
    return {
      titanicImage: new URL('@/assets/titanic.jpg', import.meta.url).href,
      modelInfo: {
        coefficients: null,
        n_features: 0,
        features: [],
        classes: []
      },
      featureChart: null,
      team: [
        {
          name: "Ananda Lestari",
          photo: new URL('@/assets/nanda.jpg', import.meta.url).href,
          github: "https://github.com/Anandalestari",
          linkedin: "https://www.linkedin.com/in/ananda-lestari-132342295/"
        },
        {
          name: "Roro Syaraswati",
          photo: new URL('@/assets/roro.jpg', import.meta.url).href,
          github: "https://github.com/rorosyaraswati",
          linkedin: "https://www.linkedin.com/in/roro-syaraswati-syafitri-6600442bb/"
        }
      ]
    }
  },
  methods: {
    async fetchModelInfo() {
      try {
        const response = await axios.get('http://localhost:5000/model-info')
        console.log('Model Info Response:', response.data) // Debugging
        this.modelInfo = response.data
        this.$nextTick(() => {
          this.createFeatureChart()
        })
      } catch (error) {
        console.error('Error fetching model info:', error)
      }
    },
    createFeatureChart() {
      if (!this.modelInfo.coefficients) return
      
      const ctx = this.$refs.featureChart.getContext('2d')
      if (this.featureChart) {
        this.featureChart.destroy()
      }

      const features = Object.keys(this.modelInfo.coefficients).filter(f => f !== 'Intercept')
      const values = features.map(f => Math.abs(this.modelInfo.coefficients[f]))

      this.featureChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: features,
          datasets: [{
            label: 'Feature Importance (Absolute Value of Coefficients)',
            data: values,
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgb(54, 162, 235)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      })
    },
    handleImageError(event) {
      event.target.src = 'https://via.placeholder.com/150'
    }
  },
  mounted() {
    this.fetchModelInfo()
  }
}
</script>