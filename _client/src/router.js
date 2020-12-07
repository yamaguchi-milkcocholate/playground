import Vue from 'vue';
import Router from 'vue-router';
import Mnist from './components/Mnist.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/mnist',
      name: 'Mnist',
      component: Mnist,
    },
  ],
});
