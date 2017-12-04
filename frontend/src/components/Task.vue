<template>


  <div class="Element">

    <div class="Prompt_Box">


         <b>Prompt: </b> <i> {{computed_prompt}}. </u> </i>

    </div>


    <Content_Rate_Element v-if="compute_view_type" :Content="Previous_Result" :Body_Of_Task="Body_Of_Task" :Type="Type" :Context="Context" :Is_Example="Is_Example" :Suggestion_List="computed_suggestions"></Content_Rate_Element>

    <Content_Element v-else :Body_Of_Task="Body_Of_Task" :Type="Type" :Context="Context" :Is_Example="Is_Example" :Suggestion_List="computed_suggestions"></Content_Element>



  </div>
</template>
<script>
  import Content_Rate_Element from './Content_Rate_Element.vue'
  import Content_Element from './Content_Element.vue';
  import SuggestionList from './SuggestionList.vue';

export default {
  name: 'Prompt',
  components: {
    Content_Element, SuggestionList,Content_Rate_Element
  },
  props:["Suggestion","Previous_Result","Prompt","Context","Body_Of_Task","Type","Is_Example","Is_Modifiable"],
  data: function(){
    return {

      example_prompt:"Try to rewrite the following text to be about sports",

      example_suggestions: [
              { message: 'Make this text talk about soldiers'},
              {message:'the brother and sister could be soldiers '}
            ],

      example_content:{
        Content:"My brother and sister fought alot ",
        Previous_Content:"My brother and sister Jeane got in fights all the time. One day",
        History:"Sample context to help impact decision",
        Type:"rewrite",
        Is_Modifiable:this.Is_Modifiable

      }


    }
  },

  computed:{

    compute_view_type(){

      if(this.Type=="Rate") {
        return true;
      }
      return false;
    },

    computed_prompt:function(){
      if (typeof this.Prompt =='undefined') {
        return this.example_prompt;
      }
        return this.Prompt
    },

    computed_task_type:function(){
      if (typeof this.Type =='undefined') {
        return "_Placeholder_";
      }
        return this.Type
    },
    computed_suggestions:function(){
       if (typeof this.Suggestion =='undefined') {
        return this.example_suggestions;
      }

        return this.Suggestion;


    },
    computed_task_content:function(){

      if (typeof this.Content =='undefined') {

        return this.example_content;
      }

      return this.Content;
    }

  }

}//:user_id="user_id"


  //Has Both instructions
  //Suggestions
  //Example
  //Explanation

</script>

<style>
  .Prompt_Box {
    margin-bottom: 10px;
  }

</style>
