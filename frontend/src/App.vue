<template>
  <div id="app">
    <button v-on:click="getRandom(1)">HI</button>
  <Task></Task>
    <router-view/>
  </div>
</template>

<script>
  import jquery from 'jquery'
  import Content from './components/Content.vue'
  import SuggestionList from './components/SuggestionList.vue'
  import Prompt from './components/Prompt.vue'
  import Task from './components/Task.vue'
export default {
  name: 'app',
  components: {
    Content, SuggestionList, Prompt, Task
  },
  data: function() {
    return {
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

    getRandom: function (result_obj) {
            //Pass in the select of name and password specified by the user
            console.log("YAY");
            console.log(this.how_are_you);
            console.log(this.$data.how_are_you);
            console.log(jquery);
            console.log("BLAH");
            jquery.ajax({
                url: '/api/random',
                data: "jsonData=" + JSON.stringify({"val":1}),
                type: 'POST',
                success: function (response) {
                    //Update the image


                  console.log("KHANNN");

                }.bind(this)

            });
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
  margin-top: 60px;
}
</style>
