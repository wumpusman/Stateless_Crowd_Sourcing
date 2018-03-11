<template>
    <div class="ui segment">
   <div v-if="has_header" class="ui top attached label" v-bind:class='header_color' >

    <a class="item">
      <h3>       {{header_text }} </h3>

    </a>

    </div>

       <slot></slot>

   </div>
</template>

<script>
    export default {
      name: "div_block",
      props:{header_text:{default:'empty'}, header_color:{default:"grey"}, has_header:{default:false}, parent_element:{default:null}},
      data: function (){
        return {


        }

      },
      methods:{},
      computed:{}
      }


</script>

<style scoped>

</style>
