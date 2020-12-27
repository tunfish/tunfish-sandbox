<template>
  <div>
    <div class="md-layout md-gutter">
      <div class="md-layout-item">
        <md-field>

          <label>Network</label>

          <md-select v-model="network" name="network" id="network">
            <md-option value="network">{{network}}</md-option>
          </md-select>

        </md-field>
        <md-button v-on:click='getNW'></md-button>
      </div>
    </div>
  </div>
</template>

<script>
  export default {

    name: 'dropdown',
    
    data: () => ({
      network: 'default',
    }),
    
    methods: {
      getNW: function (event) {
        console.log(event)
        console.log('before getNetworkList')
        //console.log(this.$tf_functions.getNetworkList())
        this.$store.commit('doConnection')
      } 
    }

  }
</script>
