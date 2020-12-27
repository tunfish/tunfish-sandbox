<template>
  <div id="app">
    <Navbar></Navbar>
  </div>
</template>

<script>

import Navbar from './components/NavBar';
  
export default {
  name: 'App',
  components: {
    Navbar
  },
}
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.4;
}
</style>
