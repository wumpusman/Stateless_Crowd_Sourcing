<template>

  <div>

    <div id="prev_content" >  <span><b>{{computed_example_text}} Original Content </b></span>
          <div v-bind:class="lower_opacity_if_example()">
          {{Body_Of_Task}}
            </div>
        </div>
    <div id="compare_respond">


      <div id="viewable_content">
        <div id="suggestion_list">
        <SuggestionList :Suggestion_List="Suggestion_List"></SuggestionList>
        </div>

         <div id="context">
          <span v-if="Context != '' && Context != 'undefined'"><b>{{computed_example_text}} Context</b></span>
            {{Context}}
        </div>


      </div>
      <div id="user_input"    >
          <div><b><u>{{computed_example_text}} Content To Be Evaluated Below</u></b></div>



          <div v-bind:class="background_border_and_red()" >  <p>   {{Content}} </p>  </span></div>

          <div id="rating" > <b> Rate <u> Above </u> On Quality Of Achieving Prompt: </b>
                <radio_list :Is_Modifiable="Is_Modifiable"></radio_list>
            </div>
      </div>
      </div>

  </div>
</template>

<script>

    import radio_list from './radio_button_list/radio_list.vue'
    import SuggestionList from './SuggestionList.vue'
export default {
  props: ["Content", "Context","Body_Of_Task","Type","Is_Example","Is_Modifiable","Suggestion_List"],
  components:{radio_list,SuggestionList},
  data:function(){
      return {


        example_text:"THIS IS AN EXAMPLE FOR REFERENCE:",
        example_explained:" The following text written below is an example of a user taking the content highlighted yellow on the left and rewriting it here\r\n \r\n",
        user_feedback:"Enter Text Here"
      }
     },

  methods: {
     lower_opacity_if_example:function(){
       if (this.compute_is_example) {
         return "low_opacity";
       }
       return "high_opacity";
     },

    background_border_and_red:function(){

         return ["background_red","text_area"];

    }

  },

  computed:{

    user_input: { //if this is accessible and stored globally - not super clean tbh
      get(){

        if (this.compute_is_modifiable) {
          return this.$root.$data.stored_state.state.current_result;
        }
        return ""
      },
      set(value){

         if (this.compute_is_modifiable) {
            this.$root.$data.stored_state.set_result(value);
        }

        //return this.$root.$data.stored_state.state.current_result;



      }

    },
    compute_is_modifiable:function(){

      if(typeof this.Is_Modifiable == 'undefined') {
        return false;
      }
      return this.Is_Modifiable;
    },

    compute_is_example:function(){


      if(typeof this.Is_Example == 'undefined') {
        return true;
      }

      return this.Is_Example;
    },

    computed_example_text:function(){

        if (this.compute_is_example){
          return this.example_text ;
        }
          return "";
    },
    computed_explain_text:function(){
      if (this.compute_is_example){
          return this.example_explained ;
        }
          return "";
    }

  }

}
</script>


<style>

</style>
