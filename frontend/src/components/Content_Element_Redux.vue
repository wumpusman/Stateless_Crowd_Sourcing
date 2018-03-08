<template class="main_container">

  <div class="ui main_container column_like OVERVIEW_AND_ALT">

    <div class="ui segment">
         <div class="ui top attached label">

      <h3> Overview </h3>
   </div>
      <div> what </div>
    </div>


    <div class="row_like INSTRUCTION AND FIRST ACTION">
      <div class="ui segment"> Instruction


      </div>

       <div class="ui segment">  <a class="item">
        <div class="ui green horizontal label">A</div>

          </a> </div>
    </div>

    <div class="row_like INPUTBOX_AND_SECOND_ACTION">
      <div class="ui segment">Input and Example Box s
        <slot name="input_type"></slot>

      </div>
      <div class="ui segment">
        <a class="item">
        <div class="ui blue horizontal label">B</div>

          </a> </div>
    </div>

    <div class="row_like THIRD_ACTION">

      <div class="ui segment">Empty</div>
      <div class="ui segment">

        <a class="item">
          <div class="ui red horizontal label">C</div>

          </a>
       </div>
    </div>

  </div>


</template>

<script>

    import radio_list from './radio_button_list/radio_list.vue'
    import SuggestionList from './SuggestionList.vue'
export default {}

</script>


<style>
  .main_container{
    width:100%;
    height:100%;
  }
  .row_like{
    display:flex;

    justify-content:space-between;
    align-content: space-between;

  }

  .column_like{
    display:flex;
    flex-direction: column;

    justify-content: space-between;

  }

  .background_red {
    background-color:lightyellow;

    border: 10px solid black;
  }

  .low_opacity{
    opacity:.6;
    background-color: lightyellow;
  }
  #suggestion_list{
    display:flex;
    align-items: center;

    flex-direction: column;
    height: 90%;
    width:100%;
  }
  .high_opacity{
    opacity: 1;
  }

  #compare_respond{
    display:flex;

    justify-content: center;
    height:400px;
    text-align:justify;
  }

  #viewable_content{
    display:flex;
    flex-direction:column;
    justify-content: center;
    height: 90%;
    width:45%;
    padding:10px;
  }

  #context{
    display:flex;
    flex-direction: column;
    align-items: center;
    height: 90%;
    width:100%;
    text-align:justify;
  }

  #body_of_prev_content{
    display:flex;
    justify-content: center;
    width:50%;
  }
  #prev_content{
    display:flex;
    align-items: center;

    flex-direction: column;
    height: 90%;
    width:100%;
  }
  #text_box{
    margin-top:10px;
    width: 95%;
    height: 100%;
  }
  .text_area{
    margin-top:10px;
    width:95%;
    height:100%;
  }


  #rating {
    display:flex;
    align-content:flex-start;
    flex-direction: column;
  }
    #user_input{
    display:flex;
      flex-direction: column;
    height: 100%;
    width:45%;
      margin-top: 10px;
      text-align:center;
  }
</style>
