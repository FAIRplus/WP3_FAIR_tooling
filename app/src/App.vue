<template>
  <v-app>
  <head>
    <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css" rel="stylesheet">
  </head>
  <div id='app'>
  <body>
    <NavBar />
    <div class="main">
      <router-view/>
    </div>
  </body>
  <Footer />
  </div>
  </v-app>

</template>
<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100%;
  display: flex;
  min-height: 100vh;
  flex-direction: column;
  justify-content: space-between;
}

body{
  display: flex;
  flex-direction: column;
  height: 100%;
}

main{
  display:flex;
  flex-direction:column;
  width: 100%;
}


</style>
<script>
import NavBar from './components/NavBar.vue'
import Footer from './components/Footer.vue'
export default {
  name: 'Home',
  components: {
    NavBar,
    Footer
  }
}
</script>