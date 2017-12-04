import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  { path: '/Home', component: 'Home' },
  { path: '/Project_Container', component: 'Project_Container' },
  { path: '/Task', component: 'Task' },
  { path: '/Instruction', component: 'Instruction' },
  {path:'/Login',component:"Login"}
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
