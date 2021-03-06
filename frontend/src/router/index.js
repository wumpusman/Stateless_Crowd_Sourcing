import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  { path: '/Home', component: 'Home' },
  { path: '/Project_Container', component: 'Project_Container' },
  { path: '/Task', component: 'Task' },
  { path: '/Instruction', component: 'Instruction' },
  {path:'/Login',component:"Login"},
  {path:'/Finished',component:"Finished"},
  {path:'/Content_Element',component:"Content_Element"},
  {path:'/Show_Results',component:"Show_Results"},
  {path:'/User_Results',component:"Control_Turk_State"},
  {path:'/System_Container',component:"System_Container"},
  {path:'/text_block',component:"text_block"},
  {path:'/A_Place_For_Testing',component:"A_Place_For_Testing"}
   //#console.log(window.location.href);
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
