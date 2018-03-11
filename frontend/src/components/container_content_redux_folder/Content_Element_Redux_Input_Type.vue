<template>
<div>

  <Content_Element_Redux>


    <div slot="feedback">

            <div >
              <div v-if="test_this==='haah'"> {{test_this}}</div>
            <button style="margin: 5px;" class="ui mini basic compact button">
          <i class="question green circle icon"></i>
          Examples
        </button>
        <div class="ui divider"></div>

      </div>

      <input_text_block :parent_element=this></input_text_block>

    </div>
    <div slot="input_type">


    </div>


  </Content_Element_Redux>
</div>
</template>

<script>

    import Content_Element_Redux from './Content_Element_Redux'
    import input_text_block from './container_redux_elements/input_text_block_redux'



    export default {
        name: "Content_Element_Redux_Input_Type",
        components: {
            Content_Element_Redux,input_text_block
        },
        data:function(){
          return {
            test_this:"haah"
          }
        }
    }

</script>

<style scoped>

</style>
