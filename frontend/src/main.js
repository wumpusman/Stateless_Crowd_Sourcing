// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

Vue.config.productionTip = false

function format_suggestions(task){

  if("task" in task) {
    if ("project_state" in task["task"]) {
      if (task["task"]["project_state"] == "Finished") return;
    }
    if ("Suggestion" in task["task"]){
      var suggestions=task["task"]["Suggestion"];

      if (typeof(suggestions)==typeof("")) {
        if (suggestions=="") suggestions=[]
        else suggestions = [suggestions];
      }
      for(var i=0;i<suggestions.length;i++){
        suggestions[i]={"message":suggestions[i]}

      }

      task["task"]["Suggestion"]=suggestions;
    }

  }

}

function extractInstructions(info){
  var default_instructions={"Explanation":"","Examples":[]};
  if ("task" in info){
    if ("instructions" in info["task"])
      default_instructions=info["task"]["instructions"];

  }
  return default_instructions;
}

function keepAscii(value){
  return value.replace(/[^\x00-\x7F]/g, "");
}

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: {App},
  data: {
    stored_state: { //This will keep all information that I will need that is specified and determined by the backend
      state: {
        name: "",
        password: "",
        amount_of_content_submitted:0,
        current_project_state: "Login",
        current_result: "Enter Response Here", //the content being entered
        current_rating: "", //the rating for the current content
        current_task: {
          "task": {
            "Prompt": "Take a gun and end it", "Suggestion": [{"message": "bahhh black wfwee"}],
            "Body_Of_Task": "fuck you", "Context": "This is arbitrary", "Type": "rate", "instructions": []
          }
        },
        current_instructions: {"Explanation": "", "Examples": []},
        max_session_time: 7 * 60,
         _start_time: new Date().getTime() / 1000
      },
      setNameAndPassword(value, password){

        this.state.name = value;
        this.state.password = password;
      },

      initialize_session_time_and_start_time(info){

        if ("task" in info) {
          if ("Session_Time" in info["task"]) {
            console.log("YAY")
            this.state.max_session_time = info["task"]["Session_Time"];
            this.state._start_time = new Date().getTime() / 1000;

          }
        }
      },
      setProjectState(info){

        if ("task" in info) {

          if ("Project_State" in info["task"]) {

            this.state.current_project_state = info["task"]["Project_State"];


          }
        }
      },
      setTask(info){
        //format suggestion

        format_suggestions(info);
        this.state.current_task = info;

      },
      setInstructions(info){
        this.state.current_instructions = extractInstructions(info);
        console.log("CURRENT INSTRUCTIONS");
        console.log(this.state.current_instructions);
      },
      set_result(value){
        value=keepAscii(value);
        console.log("UPDATING" + value)
        this.state.current_result = value;
      },
      set_rating(value){
        this.state.current_rating = value;
      },
      clear_user_feedback(){
        this.state.current_result = "";
        this.state.current_rating = "";
        console.log("THE USER INPUT HAS CHANGE IT SHOULD BE UPDATED EVERYWHERE")
        console.log(this.state.current_result);
      },
      increment_submissions(){
        var prev=this.state.amount_of_content_submitted
        this.state.amount_of_content_submitted=prev+1;
      },

      has_session_expired(){ //Check if the session should be stopped


        var start_time=this.state._start_time;
        var current_time=new Date().getTime() / 1000;
        var max_time=this.state.max_session_time;

        if((current_time-start_time)<max_time) return false;
        return true;

    }
    }
  }
});




/**
 ,,



    }**/
