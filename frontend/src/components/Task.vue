<template>
  <div id="task">

    <div id="header">

      <div class="header_element">  <b><a href>Current_Prompt</a> </b></div>
      <div class="header_element">  <b> <a href>Example</a></b></div>

    </div>
    <div id="hint">Use Example for help or Click Current_Prompt to return to the current task </div>
    <div id="prompt_segment">
    <Prompt></Prompt>
    </div>


     </div>
</template>


<script>
import Content from './Content.vue'
import Prompt from './Prompt.vue'

export default {
  name: 'Task',
  components: {
    Content,
    Prompt
  }
}
</script>

<style>

  #header{
    display:flex;
    flex-direction:row;
    justify-content: center;
    padding:10px;

  }

  #task{
    display:flex;
    flex-direction:column;

  }
  #prompt_segment{
    padding:10px;
  }
  #hint{
    display:flex;
    flex-direction:column;
    padding-bottom:10px;
    border-bottom: 2px solid black;
  }
  .header_element{
    padding:10px;
  }

</style>
