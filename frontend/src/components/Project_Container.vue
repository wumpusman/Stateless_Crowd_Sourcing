<template>
  <div id="page">

    <div id="header">
      <div class="header_element" v-on:click="set_page('Instruction')">  <b><button >Instruction Page</button> </b></div>
      <div class="header_element" v-on:click="set_page('Task')">  <b><button >Current_Task</button> </b></div>
      <div class="header_element" v-on:click="set_page('Example')">  <b> <button >Example</button></b></div>

    </div>

    <div id="hint">Use Example for help or Click Current_Task to return to the current task </div>

    <div id="project">

      <Task v-if="which_page('Task')" :Is_Example="test_example" v-bind="computed_task"  :Is_Modifiable="can_modify"></Task>
      <Task v-if="which_page('Example')"></Task>
      <Instruction v-if="which_page('Instruction')"></Instruction>

      <div class="pad_top">
        <button v-if="which_page('Instruction')" v-on:click="set_page('Task')"> Click To Begin Task </button>
        <button v-if="which_page('Task')"> Click To Submit </button>
      </div>
    </div>


    </div>


     </div>
</template>


<script>
import Content_Element from './Content_Element.vue'

import Task from './Task.vue'
import Instruction from './Instruction.vue'
import Login from './Login.vue'



export default {
  name: 'Project_Container',
  components: {
    Content_Element,
    Task,
    Instruction

  },
  data:function(){
      return {
        current_page:"Task", //Instruction,Example,Task,Login

        can_modify:true,
        test_example: false
      }
    },
  methods:{
    which_page:function(value){

      if((value)==this.current_page)return true;
      return false;
    },
    set_page:function(value){

      this.current_page=value;
    }


  },
  computed:{

      computed_task:function(){
        console.log("CALL ME MAYBE fwefew");
        console.log(this.$root.$data.stored_state.state.current_task['task']["Body_Of_Task"]);
        return this.$root.$data.stored_state.state.current_task['task'];
      },

      computed_prompt:function(){
          var all_info=this.computed_task;
          console.log(all_info);

          if (prompt in all_info["task"]){
            return all_info["task"]["prompt"];
          }
          return null;

      },

      computed_body_of_task:function(){
          var all_info=this.computed_task;
          console.log(all_info);

          if (prompt in all_info["task"]){
            return all_info["task"]["body_of_task"];
          }
          return null;
      },

      computed_suggestions:function(){
         var all_info=this.computed_task;
          console.log(all_info);

          if (prompt in all_info["task"]){
            return all_info["task"]["suggestions"];
          }
          return null;
      }

  }

}
</script>

<style>

  #header{
    display:flex;
    flex-direction:row;
    justify-content: center;
    padding:10px;

  }

  .pad_top{
    margin-top:10px;
  }
  #task{
    display:flex;
    flex-direction:column;

  }
  #prompt_segment{
    padding:10px;
  }
  #hint{
    display:flex;
    flex-direction:column;
    padding-bottom:10px;
    border-bottom: 2px solid black;
  }
  .header_element{
    padding:10px;
  }

</style>
