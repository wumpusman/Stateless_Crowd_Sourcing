<template>

  <div>

    <div id="compare_respond">



      <div id="viewable_content">

        <div id="prev_content">  <span><b>Content To Transform</b></span>
          {{Previous_Content}}
        </div>
         <div id="history">
          <span><b>Context</b></span>
            {{History}}
        </div>
      </div>
      <div id="user_input">

          <textarea id="text_area">Enter Text Here: {{Content}}</textarea>
          <div id="rating"> <b> Rate Text On Quality Of Achieving Prompt Goal: </b>
                <radio_list></radio_list>
            </div>
      </div>
      </div>

  </div>
</template>

<script>
    import radio_list from './radio_button_list/radio_list.vue'
export default {
  props: ["hello","Content", "History","Previous_Content"],
  components:{radio_list},
  data:function(){
      return {

      }
     },

  methods: {


  }
}
</script>


<style>

  #compare_respond{
    display:flex;

    justify-content: center;
    height:400px;

  }

  #viewable_content{
    display:flex;
    flex-direction:column;
    justify-content: center;
    height: 90%;
    width:45%;
    padding:10px;
  }

  #history{
    display:flex;
    flex-direction: column;
    align-items: center;
    height: 90%;
    width:100%;
  }

  #prev_content{
    display:flex;
    align-items: center;

    flex-direction: column;
    height: 90%;
    width:100%;
  }

  #text_area{
    width:90%;
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
  }
</style>
