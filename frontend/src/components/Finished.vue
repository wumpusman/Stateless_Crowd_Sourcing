<template>
  <div>
    <p v-if="compute_flagged_user"> One of your answers was flagged or previously flagged. This relates to providing an answer that is several standard deviations from the norm.
    It will be verified and evaluated by other users. Use the code 'Review_Flag' </p>
    <p v-else-if= "compute_work_done">Thank you for your time. COPY AND USE the following code before <u>leaving or switching from the current
      page </u>: {{Code}}
    </p>
    <p v-else-if="compute_bad_user">One of your previous answers was flagged</p>

    <p v-else>   Currently there are no available queries to do at this time. Please come by at another time, no code will be provided</p>
  </div>
</template>

<script>

  export default {
    name: "Finished",
    props: {Tasks_Completed: {default: 0, type:Number}, Code: {default: "-1"}},


    computed: {
      compute_work_done: function () {
        if (this.Tasks_Completed >0) return true;
        return false;
      },
      compute_flagged_user:function(){
        if(this.Code == "Flagged")
          return true;
        return false;
      },
      compute_bad_user:function(){
        if(this.Code=="Bad_User")
          return true;
        return false;
      }

    }
  }
</script>
