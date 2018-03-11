<template>
  <div>
      <div_block :has_header=true header_text='Hypothetical List of links' header_color='teal'><div slot="content"> ok</div></div_block>

    <div>
    <Content_Element_Redux_Input_Type></Content_Element_Redux_Input_Type>
    </div>
    </div>
</template>

<script>

    import Content_Element_Redux from './container_content_redux_folder/Content_Element_Redux.vue'
    import Content_Element_Redux_Input_Type from './container_content_redux_folder/Content_Element_Redux_Input_Type.vue'
    import div_block from './container_content_redux_folder/container_redux_elements/Div_Block.vue'

    export default {
        name: "a_place_for_testing",

      components: {
        Content_Element_Redux, Content_Element_Redux_Input_Type, div_block
      },
    }
</script>

<style scoped>

</style>
