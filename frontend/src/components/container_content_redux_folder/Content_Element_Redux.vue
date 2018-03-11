<template >

  <div class="ui grid column container row ui ">

    <div id="Header_Part" class="sixteen row">



        <Div_Block class=" eight wide  column  " has_header=true :header_text=header_overview header_color="grey">
      <div >
           <div class="ui divider"></div>
        <div class="ui segment">  <i> Here is your basic overview  </i></div>

      </div>
    </Div_Block>

        <div class="two wide column"></div>

      <Div_Block class="  five wide  column  "  has_header="true" :header_text=header_legend>
        <div class="ui segment">Here is the legend </div>
      </Div_Block>
    </div>




       <div class="ui divider"></div>


    <div id="full_body" class="ui grid column row">



      <div id="Task_And_Input" class="eight wide column">
            <Div_Block has_header=true :header_text=header_instructions header_color="black">
              <div >
                   <div class="ui divider"></div>
                    <div class="ui segment inverted">  <i> Here are your instructions </i></div>
              </div>
           </Div_Block>


        <Div_Block has_header=true :header_text=header_user_feedback header_color="orange">

                 <slot name="feedback"> </slot>

        </Div_Block>


      </div>

      <div class="two wide column"> </div>

      <div id="information_blocks" class="five wide column ui grid container">

          <Div_Block has_header=true :header_text=header_main_info >
            <div> The end is nigh</div>
          </Div_Block>
          <Div_Block has_header=true :header_text=header_info_b >
             <div>Finally</div>
          </Div_Block>

          <Div_Block has_header=true :header_text=header_info_c >
              <div>Curse you james</div>
          </Div_Block>

        </div>


    </div>





  </div>


</template>

<script>

import Div_Block from './container_redux_elements/Div_Block'

export default {

  components: {
    Div_Block
  },
  props:{
    header_user_feedback:{default:"User Input"}, header_legend:{default:"Legend"}, header_overview:{default:"Overview"},
    header_instructions:{default:"Instructions"},
    header_main_info:{default:"A"}, header_info_b:{default:"B"},
    header_info_c:{default:"C"}

  }
}

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
