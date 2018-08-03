<template>
  <div>

    <div>
    <button v-on:click="get_results(0)">Request Results</button></div>
    <div><button>Update Task</button></div>
    <div><button>Request Work</button></div>

    <div><p> &nbsp</p></div>
    <div> Max History <input  v-model="var_history" placeholder="history"></input> </div>
    <div> Selected Task <input v-model="var_task_num" placeholder="current task #"></input></div>

    <div class="ui container segment">
      <div>

        <div class="ui segment" v-for="user in computed_results">

             <span class="item left aligned content"> <b>User:' </b>{{user.user}}'</span>  <span class=" item"> <b> Status</b> '{{user.user_quality}}'</span> <span> <b>Turk Submission Time</b> {{user.latest_turk_submission_time}} </span>

            <div class="ui segment left aligned content" v-for="user_results in user.results">
              <span> <b>Completion Time: </b> '{{user_results.relative_time}}' seconds </span>  <span>  <b>Result: </b> {{user_results.result}}</span>
            </div>
        </div>

      </div>



      </div>


    </div>



</template>

<script>
 import jquery from 'jquery'
//view users who have submitted and there work
//pointing menu
//Request Users Who Have submitted from mturk
//In the last X minutes, users who have not been unapproved
//List
 /*

 {"results":
 [{"user_quality": "acceptable", "results": [{"absolute_time": "2018-07-31 21:23:24.512271-04:00", "relative_time": "7.080301", "result": "They were very large boots her mother had previously worn so large that the girl lost them as she ran away across the street because of the two cars that had driven by incredibly fast. One of the boots was nowhere to be found the other had been laid hold of by a homeless man. And he ran off with it!"}, {"absolute_time": "2018-07-28 02:15:54.814937-04:00", "relative_time": "328056.777635", "result": "5"}],
  "user": "AX4COK9AJ0VTR", "latest_turk_submission_time": "2018-07-31 17:23:36-04:00", "user_exists": true}, {"user_quality": "acceptable", "results": [{"absolute_time": "2018-07-27 13:50:09.881245-04:00", "relative_time": "380576.711327", "result": "The young girls sat shivering in the woods. Her sneakers were soaked and her smartphone was nearly out of power. She thought about calling someone but it was Christmas. Who would come rescue her on Christmas. She thought of her loving Grandmother and the wonderful stories she told about the stars. In the last bit of light provided by her phone she sees the beauty of the woods around her and the stars in the sky. A vision of her beloved Grandmother welcomes her soul to heaven as her body freezes and dies."}, {"absolute_time": "2018-07-27 13:44:29.992306-04:00", "relative_time": "380916.600266", "result": "1"}], "user": "A30RLMU6S57XR0", "latest_turk_submission_time": "2018-07-31 19:33:11-04:00", "user_exists": true}, {"user_quality": "acceptable", "results": [{"absolute_time": "2018-07-31 23:37:32.874886-04:00", "relative_time": "11.717686", "result": "4"}, {"absolute_time": "2018-07-31 23:36:33.078500-04:00", "relative_time": "71.514072", "result": "They were very old sneakers that her mother had bought at the thrift store. They were worn out before she ever had a chance to wear them. Its a wonder they lasted this long. The soles gave out as she ran across the street trying to beat the light.  They were impossible to walk in anymore so she threw them in the nearest dumpster."}], "user": "A1JJNB108BPMRN", "latest_turk_submission_time": "2018-07-31 19:37:49-04:00", "user_exists": true}, {"user_quality": "acceptable", "results": [{"absolute_time": "2018-08-01 01:12:23.919453-04:00", "relative_time": "7.673119", "result": "2"}, {"absolute_time": "2018-08-01 01:11:53.310280-04:00", "relative_time": "38.282292", "result": "4"}], "user": "A3RCNWIPHVUNRZ", "latest_turk_submission_time": "2018-07-31 21:12:36-04:00", "user_exists": true}, {"user_quality": "acceptable", "results": [{"absolute_time": "2018-08-01 04:18:20.437560-04:00", "relative_time": "12.155012", "result": "4"}, {"absolute_time": "2018-08-01 04:18:11.557252-04:00", "relative_time": "21.03532", "result": "3"}], "user": "A1NT8BT94ME6F5", "latest_turk_submission_time": "2018-08-01 00:18:37-04:00", "user_exists": true}, {"user_quality": "acceptable", "results": [{"absolute_time": "2018-08-01 06:18:54.499628-04:00", "relative_time": "44.092944", "result": "4"}, {"absolute_time": "2018-07-28 03:58:51.493506-04:00", "relative_time": "354047.099066", "result": "5"}], "user": "A2DLH5XGBNYXWS", "latest_turk_submission_time": "2018-08-01 02:19:43-04:00", "user_exists": true}, {"user_quality": "acceptable", "results": [{"absolute_time": "2018-08-01 09:10:43.515088-04:00", "relative_time": "26.077484", "result": "He thought it would be perfect for a cradle if someday he decided to have children. The young girl walked on her scraped and bruised feet they were turning blue from the freezing weather. She had some matches in her dirt-stained cargo shorts and she was still holding a bunch of them in her hand. She had not been able to sell anything the whole day. She was broke no one had given her a single dime. "}, {"absolute_time": "2018-08-01 09:00:36.384604-04:00", "relative_time": "633.207968", "result": "4"}], "user": "A29GAVKOZCEEXL", "latest_turk_submission_time": "2018-08-01 05:11:14-04:00", "user_exists": true}, {"user_quality": "acceptable", "results": [{"absolute_time": "2018-08-01 17:14:05.783288-04:00", "relative_time": "5.809284", "result": "2"}, {"absolute_time": "2018-08-01 17:13:33.428575-04:00", "relative_time": "38.163997", "result": "He thought it would be good for a cradle when he had kids some day. So the little girl walked on with her bare feet that were freezing cold. She carried some matches in an old apron and she held a bundle of them in her hand. Nobody had bought anything from her all day. No one had given her a single penny."}], "user": "AJDS1Q0CF5HVM", "latest_turk_submission_time": "2018-08-01 13:14:16-04:00", "user_exists": true}, {"user_quality": "acceptable", "results": [{"absolute_time": "2018-08-01 19:10:06.129287-04:00", "relative_time": "23.463285", "result": "2"},
  {"absolute_time": "2018-08-01 19:09:34.612481-04:00", "relative_time": "54.980091", "result": "3"}],
  "user": "AD3176YJTD639", "latest_turk_submission_time": "2018-08-01 15:10:34-04:00",

  */

 //
export default {
 // components: {Text_block},
  name: "Control_Turk_State",
  data: function () {
    return {
      current_results:[{"user":"temp","latest_turk_submission_time":"bleh_date","user_quality":"acceptable","results":[{"result":"3","relative_time":"7","absolute_time":"date"}]}],
      var_history:2,
      var_task_num:0
    }
  },

  methods: {


    map_state: function (data) {

      this.current_results=data;



      //user_quality user latest_turk_submission_time
      //absolute_time,relative_time, result

    },


    get_results: function (number_of_elements) {
          console.log(this.var_history);
          //var current_process_id=this.process_id;
          var number_of_elements = number_of_elements;
          jquery.ajax({
              url: '/api/user_performance',
              data: "jsonData=" + JSON.stringify({"number_of_elements":number_of_elements}),
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
  computed:{
    computed_results:function(){
      return this.current_results
    },
    computed_history:function(){

    }
  }
}
</script>
