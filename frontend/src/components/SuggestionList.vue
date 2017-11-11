
<template>
<div class="list_alignment">

<ul class="list_element"  >
  <span> <b><i> Suggestions</i></b></span>
  <li v-for="item in suggestion_list">
    {{ item.message }}
  </li>
</ul>

</div>
</template>

<script>
export default {

  props: ["suggestion_list"],
  data:function(){
      return {

        }
     }

  }

</script>

<style>

  .list_element {
    display:flex;
    flex-direction: column;
    justify-content: center;
    align-items: baseline;
  }

  .list_alignment {
    display:flex;
    justify-content: center;
  }
</style>
