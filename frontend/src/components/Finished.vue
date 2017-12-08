<template>
  <div>
    <p v-if="compute_work_done">Thank you for your time. COPY AND USE the following code before <u>leaving or switching from the current
      page </u>: {{Code}}
    </p>
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
      }

    }
  }
</script>
