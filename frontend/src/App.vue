<template>
  <div id="app">
    <div id="user_name_box">{{computed_name}}</div>


    <form> Fake Result
      <input  v-model="fake_result" type="text" >
    </form>
      <button v-on:click="submit_response">Fake Result Submit {{fake_result}}</button>
    <Login></Login>
    <Project></Project>
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





export default {
  name: 'app',
  components: {
    Content_Element, SuggestionList, Prompt, Project,Login
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

    submit_response: function () {
            var name=this.$root.$data.stored_state.state.name;
            var password=this.$root.$data.stored_state.state.password;

            //Pass in the select of name and password specified by the user
            console.log(this.fake_result);
            jquery.ajax({
                url: '/api/submit',
                data: "jsonData=" + JSON.stringify({"name":name,"password":password,"results":this.fake_result}),
                type: 'POST',
                success: function (response) {
                  console.log(response );
                  var response= JSON.parse(response);
                  this.$root.$data.stored_state.setTask(response);
                }.bind(this)

            });
        }

    },
  computed:{
    task:function(){
      return this.$root.$data.stored_state.state.current_task
    },

    computed_name:function(){

        return "User_Name/ID: "+this.$root.$data.stored_state.state.name

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
