<template>

    <div id="Login_Section">
        <div id="explanation_location"><span class="explanation">If you already have a name/id/code enter it, and press login,
          otherwise either enter your own or use this code for name and password (Please remember it)</span>

          </div>

          <div><b>Optional Code: {{random_code}}</b></div>

            <div >
                <div>
                        <label v-if="!logged_in" class="login"> Name: </label>
                        <form v-if="!logged_in">
                            <input v-model="name" type="text"  name="name">
                        </form>
                        <label v-else>Logged in as: {{ name }}</label>
                </div>
                    <div v-if="!logged_in" class="login_section">
                        <label class="login">Password:</label>
                        <form >
                            <input v-model="password" type="text" name="password">
                        </form>

                    </div>

            </div>
            <div><p></p></div>
            <div class="align_submit_buttons">

                <button v-if="!logged_in" v-on:click="submit">login</button>

            </div>
      </div>

</template>

<script>
import jquery from 'jquery'



export default {
  name: 'Login',
  data:function(){
    return {
      random_code:Math.round(Math.random()*1000000)+"C" +Math.round(Math.random()*10000000)+"LX",
      logged_in:false,
      password:"",
      name:""
    }
  },
  mounted:function(){
     //this._show_only_login();

  },

  methods:{
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
            if ( this.password=="" || this.password=="Invalid Password" || this.password=="")
            {
              this.password = "Invalid Password";
              return;
            }



            jquery.ajax({
                url: '/api/login',
                data: "jsonData=" + JSON.stringify({"name":this.name,"password":this.password}),
                type: 'POST',
                success: function (response) {
                  var response= JSON.parse(response);
                  console.log(response);
                  if (response["task"] =="failure") {

                    this.name="Wrong Code";
                    this.password="Wrong Code";
                    this.logged_in=false;
                  }
                  else {
                    this._show_everything_but_login();
                    this.$root.$data.stored_state.setNameAndPassword(this.name,this.password);
                    this.$root.$data.stored_state.setTask(response);
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
