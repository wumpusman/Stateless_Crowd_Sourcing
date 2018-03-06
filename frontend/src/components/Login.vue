<template>

    <div id="Login_Section">
        <div id="explanation_location">
          <span class="explanation">Enter your Mturk workerID,
            <br> If you do not, a proper completion token cannot be guaranteed

        </span>

          </div>

          <div></div>

            <div >
                <div>
                        <label v-if="!logged_in" class="login"> WorkedID: </label>
                        <form v-if="!logged_in">
                            <input v-model="name" type="text"  name="name">
                        </form>

                </div>

            </div>
            <div><p></p></div>
            <div class="align_submit_buttons">

                <button v-if="!logged_in" v-on:click="submit">Submit</button>

            </div>
      </div>

</template>

<script>
import jquery from 'jquery'

/**
 <div v-if="!logged_in" class="login_section">
                        <label class="login">Password:</label>
                        <form >
                            <input v-model="password" type="text" name="password">
                        </form>

                    </div>

**/

export default {
  name: 'Login',
  props:{should_auto_login:{default:false}},
  data:function(){
    return {
      random_code:Math.round(Math.random()*1000000)+"C" +Math.round(Math.random()*10000000)+"LX",
      logged_in:false,
      password:"",
      name:""
    }
  },
  mounted:function(){
    window.onload = function () {
      console.log("GREAT stuff yee");
      console.log(this.is_auto_login);
      console.log("wtf this should log in huh");
      console.log(this.is_auto_login);
      if (this.is_auto_login == true) {
        this._show_everything_but_login();

        this.password = this.random_code;
        this.name = this.random_code;
        this.submit();
      }
      else {
        this._show_only_login()

      }

    }.bind(this);


  },
  computed:{
    is_auto_login:function(){
      return this.should_auto_login;

    }
  },

  methods:{
    logic:function(name,password,response){
      this.$root.$data.stored_state.clear_user_feedback();
      this.$root.$data.stored_state.setNameAndPassword(name,password);
      this.$root.$data.stored_state.setProjectState(response);
      this.$root.$data.stored_state.setTask(response);
      this.$root.$data.stored_state.setInstructions(response);
      this.$root.$data.stored_state.initialize_session_time_and_start_time(response);
    },
    logout: function(){
      this.$data.logged_in=false;

    },
    register_account:function(){},

    _show_only_login:function(){
       var $j = jquery.noConflict();
       $j("#app").css({"visibility":"hidden","display":"block"});
       $j("#Login_Section").css({"visibility":"visible","display":"block"});

    },

    _show_everything_but_login:function(){
      var $j = jquery.noConflict();
       $j("#app").css({"visibility":"visible","display":"block"});
       $j("#Login_Section").css({"visibility":"hidden","display":"none"});

    },

    submit: function (result_obj) {
            //Pass in the select of name and password specified by the user
            //this.$root.$data.stored_state.setNameAndPassword(this.name,this.password);
            if (this.name=="" || this.name == "Invalid Name"){
              this.name="Invalid Name";
              return
            }
            if (this.password=="Invalid Password" )
            {
              this.password = "Invalid Password";
              return;
            }

            console.log("password");
            console.log(this.password);

            console.log("name"+this.name)

            jquery.ajax({
                url: '/api/login',
                data: "jsonData=" + JSON.stringify({"name":this.name,"password":this.password}),
                type: 'POST',
                success: function (response) {
                  var response= JSON.parse(response);
                  console.log("login request");
                  console.log(response);
                  if (response["task"] =="failure") {

                    this.name="Wrong Code";
                    this.password="Wrong Code";
                    this.logged_in=false;
                  }
                  else {
                    this._show_everything_but_login()
                    this.logic(this.name,this.password,response);

                  }
                }.bind(this)

            });
        }
  }

}
</script>

<style>
  #explanation_location{
    display:flex;

    justify-content:center;
     padding-bottom: 10px;

  }
  .explanation{
    width: 300px;


  }


</style>
