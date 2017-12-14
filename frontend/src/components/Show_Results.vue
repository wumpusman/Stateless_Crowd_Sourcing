<template>
  <div class="flex_box_row ui container">

    <div class="ui pointing menu">
    <span  v-for="item in all_processes">

        <a class="item" id="process-item.process_id"  v-on:click="get_results(item.process_id)">{{item.process_id}}</a>
    </span>
</div>
    <div class="ui segment">
      <div id="prompt " v-on:click="get_results()"> <h3>Prompt </h3>{{prompt}} </div>
      <div id="body"><p>{{body}} </p></div>
      <div id="result"><b>{{result}} </b></div>

      <div id="user_inputs">
        <div v-for="item in user_inputs">
           <p> <i> {{item}} </i></p>
        </div>

       </div>
    </div>
  </div>


</template>

<script>
  import jquery from 'jquery'
export default {
  name:"Show_Results",
  data:function(){
    return {
      all_processes:[],
      prompt : "",
      result : "",
      body:"",
      user_inputs:[],
      is_finished : false,
      process_id:-1,

    json_one : {"process_id":1,"is_finished":true,"prompt":"Show me what you got let me see what you got","body":"","result":"I got riggity wrecked","user_input":["I like chewie", "fuck the police","I got riggity wrecked"]},
    json_two : {"process_id":2,"is_finished":false,"prompt":"Explain what you got","body":"I got riggity wrecked","result":"so muc ennui","user_input":["","I like me" +
    "fawefeffffffffffffffffffffffffff fffffffffffffffffff   fffffffffffffffff", "fuck the po po like rick would","so muc ennui","blaz blue"]}
  }
  },
  mounted:function(){
    this.get_results()
  },
  methods:{
    map_state:function(data){
      this.prompt=data["prompt"];
      this.result=data["result"];
      this.body=data["body"];
      this.user_inputs=data["user_input"];
      this.is_finished=data["is_finished"];
      this.process_id=data["process_id"];
      this.all_processes=data["processes_state"];

    },


    get_results: function (id) {

            //var current_process_id=this.process_id;
            var id = id;
            jquery.ajax({
                url: '/api/get_results',
                data: "jsonData=" + JSON.stringify({"id":id}),
                type: 'POST',
                success: function (response) {
                  console.log(response);
                  var response= JSON.parse(response);
                  var results=response["results"];


                  this.map_state(results);
                }.bind(this)

            });
        }

  },
  mounted:function(){
    this.get_results(-1);

  },

  computed:{

  }

}
</script>

<style>
 #user_inputs{
   display:flex;
   justify-content: space-between;
   padding-right: 40px;
   padding-left:40px;
 }
 .flex_box_row{
   display:flex;
   flex-direction:row ;
 }

</style>
