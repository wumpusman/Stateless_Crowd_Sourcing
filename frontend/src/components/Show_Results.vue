<template>
  <div class="flex_box_row ui container">

    <div class="ui pointing menu add_wrap">
    <span  v-for="item in all_processes">

        <a class="item"  v-on:click="get_results(item.process_id)">

          <i v-if="item.is_locked" class="green check icon"></i>
          <i v-else-if="item.in_progress" class="yellow circle check outline icon"></i>
          <i v-else-if="item.is_ready" class="yellow  circle outline icon"></i>
          <i v-else-if="item.is_ready==false" class="red minus square outline icon"></i>


          {{item.process_id}}</a>
    </span>
</div>
    <div class="ui segment">
      <div id="prompt " v-on:click="get_results()"> <h3>Prompt </h3>{{prompt}} </div>
      <div id="body"><p>{{body}} </p></div>
      <div id="result"><b>{{result}} </b></div>

      <div id="user_inputs" class="add_wrap">
        <div  v-for="item in content">
             <text_block :Text="item[1]" :Associated_Content_ID="item[0]" :Associated_User_ID="item[2]" :Associated_Score="item[3]" :Associated_Process_ID="process_id" ></text_block>
           <p> <i></i></p>
        </div>

       </div>
    </div>
  </div>


</template>

<script>
  import jquery from 'jquery'
  import text_block from './text_block.vue'
  import Text_block from "./text_block";

export default {
  components: {Text_block},
  name:"Show_Results",
  data:function(){
    return {
      all_processes:[],
      prompt : "",
      result : "",
      body:"",
      is_finished : false,
      process_id:-1,
      content:[] //Identical to user_inputs, but in addition, has


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

      this.is_finished=data["is_finished"];
      this.process_id=data["process_id"];
      this.all_processes=data["processes_state"];
      this.content=data["content"]

    },

    copy_value:function(val) { //just a test
      console.log(val);
      console.log("WTF");
      return val;
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
.add_wrap{
  display:flex;
  flex-wrap:wrap;
  flex-direction:row ;
}

</style>
