<template>
  <div id="app">


    <System_Container :should_auto_login="should_create_auto_login" v-if="compute_is_main_page"></System_Container>

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
  import Show_Results from './components/Show_Results.vue'

  import System_Container from './components/System_Container.vue'




export default {
  name: 'app',
  components: {
    System_Container
  },
  data: function(){
    return {
      should_create_auto_login:true

    }
  },
  mounted:function(){

    this.compute_is_main_page;
  },
  computed:{
    compute_is_main_page:function(){
      var address=window.location.href.split("/");
      if (address[address.length-1]=="") return true;
      return false
    }
  }
}
  </script>
