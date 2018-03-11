<template>

      <div>
         <textarea id="Text_Result" v-model="message" :placeholder="default_prompt" class="ui segment focus input_box"></textarea>


       <div class="ui divider"></div>

        <div class="ui primary button" v-on:click="bleh"> submit</div>
        <slot name="secondary_button"></slot>
      </div>
</template>

<script>
    export default {
        name: "input_text_block",
        props:{
          default_prompt:{default:"enter input here..."}, parent_element:{default:null}
        },
        data :function() {
            return {
              message:""

            }
        },
      methods:{

          bleh:function(){
            console.log("BLEH BLEH BLEH");
            if(this.parent_element!=null)
              console.log(this.parent_element.test_this);
              this.parent_element.test_this="no";
          }
      }

    }

</script>

<style scoped>

</style>
