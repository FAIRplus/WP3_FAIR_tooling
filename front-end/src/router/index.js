import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Run from '../views/Run.vue'
import Help from '../views/Help.vue'
import FAIRification from '../views/FAIRification.vue'
import About from '../views/About.vue'


Vue.use(VueRouter)

const routes = [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/run',
      name: 'Run',
      component: Run,
    },
    {
      path: '/run/:run_id',
      name: 'Run',
      component: Run,
    },
    {
      path: '/help',
      name: 'Help',
      component: Help
    },
    {
      path: '/fairification',
      name: 'FAIRification',
      component: FAIRification
    },
    { 
      path: '/about',
      name: 'About',
      component: About
    }
  ]
  
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})


export default router
