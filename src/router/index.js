import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import Prediction from '../components/Prediction.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/predict', component: Prediction },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
