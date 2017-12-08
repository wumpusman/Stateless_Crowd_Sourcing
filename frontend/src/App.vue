<template>
  <div id="app">


    <Login v-if="which_page('Login')"></Login>
    <Project v-if="which_page('Project')" :Has_Session_Expired="has_session_expired_function"></Project>
    <Finished v-if="which_page('Finished')" :Tasks_Completed="compute_submission_count" :Code="computed_name" ></Finished>

    <router-view/>
  </div>
</template>

<script>
  //<div id="user_name_box">{{computed_name}}</div>
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
  created:function(){
    console.log("WTF kfwefeillfefwew mfewfwee");

    window.beforeunload  =this.disconnect_user;
    document.beforeunload=this.disconnect_user;
    document.addEventListener('beforeunload', this.disconnect_user);
    window.onbeforeunload  =this.disconnect_user;
    window.onblur = this.refresh_page;
   // window.onmouseout = this.handler;  //window.addEventListener('beforeunload', this.handler);

  },

  methods: {
    refresh_page:function(event){
      window.location.reload(true)
    },

    which_page:function(value){

      if((value)==this.computed_project_state)return true;
      return false;
    },

    has_session_expired_function:function(){
      console.log("WHEN IS HTIS CHANGED");
      return this.$root.$data.stored_state.has_session_expired()
    },


    disconnect_user: function (event)  {
          console.log(event);
          //return "WAIT COLLOBARATE AND LISTEN";
          var name=this.$root.$data.stored_state.state.name;
          var password=this.$root.$data.stored_state.state.password;


          jquery.ajax({
              url: '/api/disconnect',
              data: "jsonData=" + JSON.stringify({"name":name,"password":password}),
              type: 'POST',
              async:false,
              success: function (response) {

                var response= JSON.parse(response);
                console.log("WE ARE STOPPED");
                window.location.reload();

              }.bind(this)

          });
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
        return this.$root.$data.stored_state.state.name;
      return "";
    },
    compute_submission_count:function(){

      return this.$root.$data.stored_state.state.amount_of_content_submitted;
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
