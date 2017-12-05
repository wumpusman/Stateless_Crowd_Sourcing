<template>
  <div id="app">
    <div id="user_name_box">{{computed_name}}</div>

    <Login v-if="which_page('Login')"></Login>
    <Project v-if="which_page('Project')" :Has_Session_Expired="has_session_expired_function"></Project>
    <Finished v-if="which_page('Finished')"></Finished>

    <router-view/>
  </div>
</template>

<script>
  import jquery from 'jquery'
  import Content_Element from './components/Content_Element.vue'
  import SuggestionList from './components/SuggestionList.vue'
  import Prompt from './components/Task.vue'
  import Project from './components/Project_Container.vue'
  import Login from './components/Login.vue'
  import Finished from './components/Finished.vue'





export default {
  name: 'app',
  components: {
    Content_Element, SuggestionList, Prompt, Project,Login, Finished
  },
  data:function() {
    return {

      fake_result:"",
      how_are_you: "hello how are you tryfwefefewin",
      default_statement: "Write Text Here",
      items: [
        {message: 'ffefew ffdsf'},
        {message: 'Bfar'},
        {message: 'Bar'}
      ]

    }
  },

  methods: {

    which_page:function(value){

      if((value)==this.computed_project_state)return true;
      return false;
    },

    has_session_expired_function:function(){
      console.log("WHEN IS HTIS CHANGED");
      return this.$root.$data.stored_state.has_session_expired()
    }

    },
  computed:{

    computed_task:function(){
      return this.$root.$data.stored_state.state.current_task;
    },
    computed_project_state:function(){
      return this.$root.$data.stored_state.state.current_project_state;
    },
    computed_name:function(){
      if(this.$root.$data.stored_state.state.name !="")
        return "User_Name/ID: "+this.$root.$data.stored_state.state.name;
      return "";
    }
  }

}//:user_id="user_id"
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}

#user_name_box{
  display:flex;

  justify-content: flex-start;


}

</style>
