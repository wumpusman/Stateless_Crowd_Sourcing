

<template>
  <div class="ui segment">
   <div class="ui top attached label">
    <a class="item">
      Home
    </a>



   </div>
     <div>
     <div class="ui segment">
          <p>wog charlie bit me ahhh</p>

      </div>

       <div class="ui divider"></div>

        <div class="ui primary button" v-on:click="send_edit('promote')">Keep</div>
         <div class="ui button" v-on:click="send_edit('remove')">Negate</div>





     </div>

  </div>

</template>

<script>
   import jquery from 'jquery';
export default {
  name:"text_block",

  methods:{

       send_edit: function (edit_type) {
            console.log(edit_type);
            //var current_process_id=this.process_id;
            var id = id;
            jquery.ajax({
                url: '/api/edit',
                data: "jsonData=" + JSON.stringify({"edit_type":edit_type}),
                type: 'POST',
                success: function (response) {
                  console.log(response);
                  var response= JSON.parse(response);
                  var results=response["results"];



                }.bind(this)

            });
        }
  }
}
  //header
//text body
//Select - Chosen = True - Upvote User, select content for propogation
//Negate - Unwanted = This Content is garbage - Downvote User
//Json Associate Content

</script>
