<template>
    <div>


            <radio_button name="options" label="Issue" :value="selectedValue" @change="changeValue"></radio_button>

            <radio_button name="options" label="1" :value="selectedValue" @change="changeValue"></radio_button>
            <radio_button name="options" label="2" :value="selectedValue" @change="changeValue"></radio_button>
            <radio_button name="options" label="3" :value="selectedValue" @change="changeValue"></radio_button>
            <radio_button name="options" label="4" :value="selectedValue" @change="changeValue"></radio_button>
            <radio_button name="options" label="5" :value="selectedValue" @change="changeValue"></radio_button>

        </div>

</template>

<script>
  import radio_button from './radio_button.vue'
  export default {
      name:"radio_list",
      components:{radio_button},
      props:['Is_Modifiable'],
      data: function() {
        return {
            selectedValue: this.$root.$data.stored_state.state.result
        }
      },
      methods: {
        changeValue: function(newValue) {

           this.$root.$data.stored_state.set_rating(newValue);
           this.$root.$data.stored_state.set_result(newValue);

        }

        }



  }



</script>
