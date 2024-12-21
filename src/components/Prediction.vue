<template>
  <div>
    <!-- Titanic Image with Background Gradient -->
    <div class="relative">
      <img :src="titanicImage" alt="Titanic" class="w-full h-64 object-cover" />
      <div class="absolute inset-0 bg-gradient-to-t from-black to-transparent opacity-70"></div>
    </div>

    <!-- Prediction Form Section -->
    <div class="max-w-md mx-auto p-4 bg-white shadow-md rounded-lg mt-6">
      <!-- Title Above Form -->
      <h2 class="text-2xl font-semibold text-center mb-6">Titanic Survival Prediction</h2>

      <form @submit.prevent="predictSurvival" class="space-y-4 mt-4">
        <div>
          <label for="pclass" class="block text-sm font-bold">Passenger Class</label>
          <select v-model="form.pclass" id="pclass" required class="w-full p-2 border rounded mt-1">
            <option value="1">1st Class</option>
            <option value="2">2nd Class</option>
            <option value="3">3rd Class</option>
          </select>
        </div>

        <div>
          <label for="sex" class="block text-sm font-bold">Sex</label>
          <select v-model="form.sex" id="sex" required class="w-full p-2 border rounded mt-1">
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>

        <div>
          <label for="age" class="block text-sm font-bold">Age</label>
          <input v-model="form.age" type="number" id="age" required class="w-full p-2 border rounded mt-1"/>
        </div>

        <div>
          <label for="fare" class="block text-sm font-bold">Fare</label>
          <input v-model="form.fare" type="number" id="fare" required class="w-full p-2 border rounded mt-1"/>
        </div>

        <div>
          <label for="embarked" class="block text-sm font-bold">Embarked</label>
          <select v-model="form.embarked" id="embarked" required class="w-full p-2 border rounded mt-1">
            <option value="C">Cherbourg</option>
            <option value="Q">Queenstown</option>
            <option value="S">Southampton</option>
          </select>
        </div>

        <div class="text-center">
          <button class="bg-blue-500 text-white px-4 py-2 rounded transition-transform transform hover:scale-105 active:scale-95">Predict</button>
        </div>
      </form>

      <!-- Chart Section -->
      <div v-if="result !== null" class="mt-6">
      
        <div class="chart-container mt-4">
          <BarChart :data="chartData" :options="chartOptions" />
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

// Register chart.js components
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  components: {
    BarChart: Bar, // Register the Bar chart component
  },
  data() {
    return {
      titanicImage: new URL('@/assets/titanic.jpg', import.meta.url).href, // Titanic image URL
      form: {
        pclass: '',
        sex: 'male',
        age: '',
        fare: '',
        embarked: '',
      },
      result: null,
      probability: null,
      chartData: {
        labels: ['Survived', 'Not Survived'],
        datasets: [{
          label: 'Survival Count',
          data: [0, 0], // default values
          backgroundColor: ['#28a745', '#dc3545'], // Green for Survived, Red for Not Survived
        }],
      },
      chartOptions: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Titanic Survival Prediction Results',
          },
        },
      },
    };
  },
  methods: {
    async predictSurvival() {
      try {
        // Send prediction data to the backend
        const response = await axios.post('http://localhost:5000/predict', this.form);

        // Update prediction result and probability
        this.result = response.data.result;
        this.probability = response.data.probability;

        // Update chart data based on the prediction result
        if (this.result === 'Survived') {
          this.chartData.datasets[0].data = [1, 0]; // Survived: 1, Not Survived: 0
        } else {
          this.chartData.datasets[0].data = [0, 1]; // Survived: 0, Not Survived: 1
        }
      } catch (error) {
        console.error('Error predicting survival:', error);
      }
    },
  },
};
</script>

<style scoped>
/* Style the Titanic Image and make sure it covers the full width */
h2 {
  display: none; /* Hide the title text in the Titanic background */
}

.chart-container {
  width: 100%;
  height: 300px;
}

/* Effect saat tombol ditekan */
button:active {
  transform: scale(0.95); /* Mengurangi ukuran tombol saat ditekan */
  transition: transform 0.1s ease-in-out; /* Haluskan transisi */
}

/* Efek hover tombol */
button:hover {
  transform: scale(1.05); /* Membesar sedikit saat hover */
  transition: transform 0.3s ease; /* Haluskan transisi */
}
</style>
