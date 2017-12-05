<template>
  <div>


  <div id="page">

    <div id="header">
      <div class="header_element" v-on:click="set_page('Instruction')">  <b><button >Instruction Page</button> </b></div>
      <div class="header_element" v-on:click="set_page('Task')">  <b><button >Current_Task</button> </b></div>


    </div>

    <div id="hint">Use Example for help or Click Current_Task to return to the current task </div>

    <div id="project">

      <Task v-if="which_page('Task')" :Is_Example="test_example" v-bind="computed_task"  :Is_Modifiable="can_modify"></Task>
      <Instruction v-if="which_page('Instruction')" :Instructions="computed_instructions" :Supplemental="computed_instruction_examples"></Instruction>

      <div class="pad_top">
        <button v-if="which_page('Instruction')" v-on:click="set_page('Task')"> Click To Begin Task </button>
        <button v-if="which_page('Task')" v-on:click="submit_response"> Click To Submit </button>
      </div>
    </div>


    </div>


     </div>
  </div>
</template>


<script>
import jquery from 'jquery'
import Content_Element from './Content_Element.vue'
import Finished from './Finished.vue'
import Task from './Task.vue'
import Instruction from './Instruction.vue'
import Login from './Login.vue'



export default {
  name: 'Project_Container',
  components: {
    Content_Element,
    Task,
    Instruction,
    Finished

  },

  data:function(){
      return {
        current_page:"Instruction", //Instruction,Example,Task,Login
        last_task_type:"", //For handling local state
        can_modify:true,
        test_example: false
      }
    },
  props:["Has_Session_Expired"],
  methods:{
    logic:function(json_response){
      //set_page if relevant page is set set by clicking on link above - implicitely in html above
      this.$root.$data.stored_state.clear_user_feedback();
      this.set_page_from_server(json_response);
      this.$root.$data.stored_state.setTask(json_response);
      this.$root.$data.stored_state.setProjectState(json_response);
      this.$root.$data.stored_state.setInstructions(json_response);

    },


    which_page:function(value){

      if((value)==this.current_page)return true;
      return false;
    },
    set_page:function(value){

      this.current_page=value;
    },

    set_page_from_server:function(value){
      if("task" in value){
        if("Type" in value["task"]){
          var new_task_type=value["task"]["Type"];
          if (new_task_type!=this.last_task_type){
            this.current_page="Instruction";
            this.last_task_type=new_task_type;
          }
        }
      }
    },

    submit_response: function ()  {

          console.log(this.Has_Session_Expired());
          var name=this.$root.$data.stored_state.state.name;
          var password=this.$root.$data.stored_state.state.password;
          var results=this.$root.$data.stored_state.state.current_result;
          var session_expired=this.Has_Session_Expired();

          jquery.ajax({
              url: '/api/submit',
              data: "jsonData=" + JSON.stringify({"name":name,"password":password,"results":results,"session_expired":session_expired}),
              type: 'POST',
              success: function (response) {

                var response= JSON.parse(response);
                this.logic(response);


              }.bind(this)

          });
      }





  },
  computed:{

      computed_instructions:function(){

        return this.$root.$data.stored_state.state.current_instructions["Explanation"];
      },

      computed_instruction_examples:function(){
        return this.$root.$data.stored_state.state.current_instructions["Examples"];
      },

      computed_task:function(){


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
