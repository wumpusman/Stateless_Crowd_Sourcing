
<template>
<div class="list_alignment">

<ul class="list_element"  >
  <span> <b><i> {{computed_header}}</i></b></span>
  <li v-for="item in computed_suggestions">
    {{ item.message }}
  </li>
</ul>

</div>
</template>

<script>
export default {

  props: ["Suggestion_List"],
  data:function(){
      return {
        sample_suggestions: [
          {message: 'THIS SHOULD NOT SHOW Suggestion one to help advise your modifications'},
          {message: 'THIS SHOULD NOT SHOW Suggestion two to help advise your modifications'}
        ]
        }
     },
  computed:{
    computed_suggestions:function(){

      if (typeof this.Suggestion_List =='undefined')
        return this.sample_suggestions;
      return this.Suggestion_List;
    },

    computed_header:function(){
      if(this.computed_suggestions.length==0) return "";
      return "Info";
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
