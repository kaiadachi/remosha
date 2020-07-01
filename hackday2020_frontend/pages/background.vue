<template>
  <div class="content mt-10">
    <div id="app">
      <v-app-bar
        app
        class="header"
      >
        <v-toolbar-title class="center">REMOSHA!</v-toolbar-title>
      </v-app-bar>
    </div>
    <v-card id="outline" class="border">
      <div class="inline-content">
        <v-card-title class="headline center">
           <span class="center">
           STEP.1 背景にしたい写真をえらぼう！
           </span>
        </v-card-title>

        <v-row>
          <v-col cols="3"><div class="numberBtn numberBtn1"></div></v-col>
          <v-col cols="3"><div class="numberBtn numberBtn2"></div></v-col>
          <v-col cols="3"><div class="numberBtn numberBtn3"></div></v-col>
          <v-col cols="3"><div class="numberBtn numberBtn4"></div></v-col>
        </v-row>

        <v-row>
          <v-col
            v-for="background in backgrounds"
            :key="background.name"
            class="d-flex child-flex"
            cols="3"
          >
            <v-card flat tile class="d-flex border" v-on:click="pickUp(background.name)">
              <v-img
                :src="background.name"
                aspect-ratio="1"
                class="grey lighten-2"
              >
                <template v-slot:placeholder>
                  <v-row
                    class="fill-height ma-0"
                    align="center"
                    justify="center"
                  >
                    <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                  </v-row>
                </template>
              </v-img>
            </v-card>

          </v-col>
        </v-row>
      </div>
    </v-card>

    <div id="isDetail" class="isDetail" v-if="isDetail">
      <nuxt-link :to="toVideo(this.backgroundName)">
        <v-card flat tile class="border">
          <v-img
            :src="this.backgroundName"
            aspect-ratio="1"
          >
            <template v-slot:placeholder>
              <v-row
                class="fill-height ma-0"
                align="center"
                justify="center"
              >
                <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
              </v-row>
            </template>
          </v-img>
        </v-card>
      </nuxt-link>
    </div>

  </div>

</template>

<script>
  export default {
    data() {
      return {
        backgroundName: '',
        backgrounds: [
          {name: 'backgrounds/1-2.png'},
          {name: 'backgrounds/1-3.png'},
          {name: 'backgrounds/1-4.png'},
          {name: 'backgrounds/1-4.png'},
          {name: 'backgrounds/2-2.png'},
          {name: 'backgrounds/1-3.png'},
          {name: 'backgrounds/1-4.png'},
          {name: 'backgrounds/1-4.png'},
          {name: 'backgrounds/3-2.png'},
          {name: 'backgrounds/1-3.png'},
          {name: 'backgrounds/1-4.png'},
          {name: 'backgrounds/1-4.png'},
          {name: 'backgrounds/4-2.png'},
          {name: 'backgrounds/1-3.png'},
          {name: 'backgrounds/1-4.png'},
          {name: 'backgrounds/1-4.png'},
        ],
        isDetail: false
      }
    },
    methods: {
      pickUp(background) {
        this.isDetail = !this.isDetail
        this.backgroundName = background
        const el = document.getElementsByClassName("v-main__wrap")
        const outline = document.getElementById("outline")
        const boders = document.getElementsByClassName("v-responsive__content")
        if (this.isDetail) {
          el[0].style.backgroundColor = 'rgba(150,203,242,0.5)'

          outline.style.background = 'rgba(150,203,242,0.5)'

          for (let i = 0; i < boders.length; i++) {
            boders[i].style.background = 'rgba(150,203,242,0.5)'

          }
        } else {
          el[0].style.backgroundColor = ''

          outline.style.background = ''
          for (let i = 0; i < boders.length; i++) {
            boders[i].style.background = ''
          }
        }

      },
      toVideo(background) {
        return '/video?background=' + background.split('/')[1]
      }
    }
  }
</script>

<style lang="scss" scoped>
  .numberBtn{
    width: 100%;
    height:40px;
  }
  .numberBtn1{
    background: url(../assets/img_noBtn1.png);
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
  }
  .numberBtn2{
    background: url(../assets/img_noBtn2.png);
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
  }
  .numberBtn3{
    background: url(../assets/img_noBtn3.png);
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
  }
  .numberBtn4{
    background: url(../assets/img_noBtn4.png);
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
  }

  .images {
    margin: 0 auto;
  }

  .isDetail {
    width: 400px;
    height: 500px;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 999;
    opacity: 1 !important;
    margin: auto;
  }

  .content {
    width: 90%;
    margin: 0 auto;

    .inline-content {
      width: 90%;
      margin: 0 auto;
    }
  }

  .v-btn {
    background: $black !important;
  }


</style>
