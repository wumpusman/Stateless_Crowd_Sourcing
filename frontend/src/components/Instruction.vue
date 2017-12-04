<template>
  <div id="instruction_section">
      <div class="instruction_body">

        <div id="type"> <u> Instructions for <span v-html="computed_task_type"> </span></u></div>
        <div id="instruction"> <p class="align_left"> {{computed_instructions}} </p></div>
        <div></div>
        <div id="supplemental" v-html="computed_supplemental"></div>

       </div>
  </div>

</template>



<script>
  //Header
export default {
  props: ["Instruction","Task_Type","Supplemental"],

  data:function(){
      return {
        example_task_type:"Rewriting content <b>(This is an example)</b>",
        example_instructions:"This Is Example - You will be shown text and be asked to rewrite it the best of your ability. Make modifications as best you can. Make what changes you can," +
        " but do not overthink it. This is only meant to take a few minutes",
        example_supplemental:"<b>This is an EXAMPLE </b> For example, you might be asked to rewrite a few sentences from an article, but make it more suspenseful, or change the context. " +
        "<p>'<b>More suspenseful</b>: The man walked to the store' -> 'The man frantically hurried to the shop'</p>"+
        "<p>'<b>Make about food at store</b>: I thought those pizzas at the party were disgusting' -> 'I couldn't stand the burgers at Burger King'</p>"
      }
     },

  computed: {
    computed_task_type:function(){
      if (typeof this.Task_Type =='undefined')
        return this.example_task_type;
      return this.Task_Type;
    },
    computed_instructions:function(){
      if (typeof this.Instructions =='undefined')
        return this.example_instructions;
      return this.Instructions ;
    },
    computed_supplemental:function(){
      if (typeof this.Instructions =='undefined') //Supplemntal is optional, but if instructions are not seen
        return this.example_supplemental;
      return this.Supplemental  ;
    }

  },
  methods: {


  }
}
//add top padding
  //center
  //

</script>

<style>
  #instruction_section{
    display:flex;


    justify-content: center;
    align-items: center ;


  }

  .instruction_body {
    width: 700px;
    display:flex;
    flex-direction:column;
    align-items: center;
  }

  #instruction {
    padding-bottom:5px;
    display:flex;

    text-align:justify;
  }
  #supplemental{
    padding-top:5px;
    border-top: 2px solid black;
  }
</style>
