<template>

  <Content_Element_Redux>
    <text_block_redux slot="input_type"></text_block_redux>

  </Content_Element_Redux>

</template>

<script>

    import Content_Element_Redux from './Content_Element_Redux'
    import text_block_redux from './text_block_redux'



    export default {
        name: "Content_Element_Redux_Input_Type",
        components: {
            Content_Element_Redux,text_block_redux
  },
    }

</script>

<style scoped>

</style>
