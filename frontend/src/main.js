// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

Vue.config.productionTip = false

function format_suggestions(task){

  if("task" in task) {
    if ("exit" == task["task"]) return;
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

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
  data: {
    stored_state: { //This will keep all information that I will need
      state: {
        name: "",
        password: "",
        current_result: "Enter Response Here", //the content being entered
        current_rating: "", //the rating for the current content
        current_task:{"instructions":{},"task":{"Prompt":"Take a gun and end it", "Suggestion":[{"message":"bahhh black wfwee"}],
          "Body_Of_Task":"fuck you","Context":"This is arbitrary","Type":"rate"}
        }
      },
      setNameAndPassword(value,password){
        this.state.name=value;
        this.state.password=password;
      },
      setTask(info){
        //format suggestion
        format_suggestions(info);
        this.state.current_task=info;
      },
      set_result(value){
        console.log("UPDATING" + value)
        this.state.current_result=value;
      },
      set_rating(value){
        this.state.current_rating=value;
      },
      clear_user_feedback(){
        this.state.current_result="";
        this.state.current_rating="";
      }

    }
  }
  });

