<template>
  <v-app class="bg">
      <v-main>
        <nuxt/>
      </v-main>

      <v-footer
        class="footer"
        app
      >
        <span>&copy; {{ new Date().getFullYear() }} REMOSHA</span>
      </v-footer>

  </v-app>
</template>

<script>
  export default {
    head() {
      return {
        script: [
          {src: "jquery.min.js"},
          {src: "materialize.min.js"},

          {src: "pico.js"}
        ],
      }
    }
  }
</script>
<style lang="scss">
  html, .theme--light{
    color: $black !important;
  }
  .center {
    width: 100%;
    text-align: center;
  }
  .header{
    background: $yellow !important;
    width:100% !important;
  }

  .footer {
    absolute: fixed !important;
  }
  .v-btn{
    width: 270px !important;
    height: 60px !important;
    background-color: $black !important;
  }
  .v-btn__content{
    // color: white !important;
  }
  // .v-toolbar__title{
  //   width: 100%;
  //   text-align: center;
  // }
  .border {
    border: 3px solid !important;
  }

  .v-application--wrap {
    background-image: url("/bg_yellow.png");
    background-size: cover;
    background-repeat: repeat;
  }
</style>
