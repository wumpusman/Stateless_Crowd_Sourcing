

<template>
  <div class="ui segment">
   <div class="ui top attached label">
    <a class="item">
      Result
    </a>



   </div>
     <div>

       <div>
         <textarea id="Text_Result" ref="Text_Result" class="ui segment focus input_box" :value="computed_text"  ></textarea>
      </div>
        <div class="ui segment">
         <br>content_id {{Associated_Content_ID}}  process_id {{Associated_Process_ID}} score {{Associated_Score}}
          <br> user {{Associated_User_ID}}

      </div>
       <div class="ui divider"></div>

        <div class="ui primary button" v-on:click="send_edit(Associated_Process_ID,Associated_Content_ID,promote_enum,compute_text_area_input_value)">Keep</div>
         <div class="ui button" v-on:click="send_edit(Associated_Process_ID,Associated_Content_ID,remove_enum,compute_text_area_input_value)">Negate</div>





     </div>

  </div>

</template>

<script>
   import jquery from 'jquery';
export default {
  name:"text_block",
   props: {Text:{default:"Default_Text Placed Here"}, Associated_User_ID:{default:"NA"}, Associated_Score:{default:-1.0},
     Associated_Content_ID: {default: 39},Associated_Process_ID:{default:1}}, //FOr testing purposes, I'll change this later
   data:function(){
      return {
        remove_enum:"remove",
        promote_enum:"promote",
        place_holder:this.Text
      }
   },

  watch: {
    place_holder: function(val, oldVal) {
      // change of userinput, do something
      console.log("WTF");
      return "777"
    }
  },


  methods:{

       send_edit: function (process_id,content_id,edit_type,optional_result) {
            console.log(edit_type);
            //var current_process_id=this.process_id;
            console.log(process_id);
            console.log(content_id);
            jquery.ajax({
                url: '/api/edit',
                data: "jsonData=" + JSON.stringify({"process_id":process_id,"content_id":content_id,"edit_type":edit_type,"result":optional_result}),
                type: 'POST',
                success: function (response) {
                  console.log(response);
                  var response= JSON.parse(response);
                  var results=response["results"];



                }.bind(this)

            });
        }
  },
  computed:{
    computed_text:function(){
      console.log("AGRO NOW");
      if (this.place_holder!=this.Text) return this.Text;
      return this.place_holder;
    },

    compute_text_area_input_value:function(){
      console.log("WTF");
      console.log(this.$refs.Text_Result.value);
      return this.$refs.Text_Result.value;
    }

  }

}
  //header
//text body
//Select - Chosen = True - Upvote User, select content for propogation
//Negate - Unwanted = This Content is garbage - Downvote User
//Json Associate Content

</script>
<style>

  .input_box{
    resize:both;
    width:100%;
  }

</style>
