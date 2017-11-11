import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  { path: '/Home', component: 'Home' },
  { path: '/Task', component: 'Task' },
  { path: '/Prompt', component: 'Prompt' }
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router);

export default new Router({
  routes,
  mode: 'history'
})
