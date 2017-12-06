<template>

  <div>

    <div id="prev_content" >  <span><b>{{computed_example_text}} Main Text To Evaluate</b></span>
          <div id="body_of_prev_content" v-bind:class="lower_opacity_if_example()">
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
          <div><b><u>{{computed_example_text}} Enter User Input Below</u></b></div>




        <textarea  class="text_area" v-model="user_input"></textarea>

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
      if (this.compute_is_example) {
         return ["background_red","text_area"];
       }
        return "text_area";
    }

  },

  computed:{

    user_input: { //if this is accessible and stored globally - not super clean tbh
      get(){


          return this.$root.$data.stored_state.state.current_result;

      },
      set(value){

            this.$root.$data.stored_state.set_result(value);


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
  .background_red {
    background-color:lightyellow;

    border: 10px solid black;
  }

  .low_opacity{
    opacity:.6;
    background-color: lightyellow;
  }
  #suggestion_list{
    display:flex;
    align-items: center;

    flex-direction: column;
    height: 90%;
    width:100%;
  }
  .high_opacity{
    opacity: 1;
  }

  #compare_respond{
    display:flex;

    justify-content: center;
    height:400px;
    text-align:justify;
  }

  #viewable_content{
    display:flex;
    flex-direction:column;
    justify-content: center;
    height: 90%;
    width:45%;
    padding:10px;
  }

  #context{
    display:flex;
    flex-direction: column;
    align-items: center;
    height: 90%;
    width:100%;
    text-align:justify;
  }

  #body_of_prev_content{
    display:flex;
    justify-content: center;
    width:50%;
  }
  #prev_content{
    display:flex;
    align-items: center;

    flex-direction: column;
    height: 90%;
    width:100%;
  }
  #text_box{
    margin-top:10px;
    width: 95%;
    height: 100%;
  }
  .text_area{
    margin-top:10px;
    width:95%;
    height:100%;
  }


  #rating {
    display:flex;
    align-content:flex-start;
    flex-direction: column;
  }
    #user_input{
    display:flex;
      flex-direction: column;
    height: 100%;
    width:45%;
      margin-top: 10px;
      text-align:center;
  }
</style>
