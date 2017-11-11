<template>


  <div class="Element">

    <div class="Prompt_Box">


         <b>Prompt: </b> <i> {{prompt}}. See <u>Content To Transform</u> </i>

    </div>

    <SuggestionList v-bind:suggestion_list="real_suggestions" ></SuggestionList>
    <Content v-bind="real_content"></Content>


  </div>
</template>
<script>
  import Content from './Content.vue'
  import SuggestionList from './SuggestionList.vue'

export default {
  name: 'Prompt',
  components: {
    Content, SuggestionList
  },
  props:["user_suggestions","is_modifiable","prompt_info","content"],
  data: function(){
    return {
      viewable_content:"example", //content, example, explanation Describes which version of the content is visible

      prompt:"Try to rewrite the following text to be about sports",

      real_suggestions: [
        {message:"Make this be more about the domain of sports"},
        {message:"Talk about lack of good products"}
      ],
      example_suggestions: [
              { message: 'Make this text talk about soldiers'}
            ],
      sample_suggestions_explained: [
        {message: 'Information to OPTIONALLY incorporate into your answer or response'},
        {message: 'Another piece of information to OPTIONALLY incorporate into your answer or response'}

      ],


      real_content:{
        Previous_Content:"love the virgin brand, I really do which is why i continue to use it despite a series of unfortunate",
        History:"A long complaint letter about the virgin brand"
      },

      example_content:{
        Content:"Rate this content: My brother and sister fought alot ",
        Previous_Content:"My brother and sister Jeane got in fights all the time. One day",
        History:""
      },

      explanatory_content:{
        Content:"Here is where you will provide content",
        Previous_Content:"The content you will be trying to account for",
        History:"Empty"
      }
    }
  }
}//:user_id="user_id"


  //Has Both instructions
  //Suggestions
  //Example
  //Explanation

</script>
