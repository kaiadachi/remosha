<template>
  <div class="wrapper">
    <div class="innner">
      <v-row>
        <div class="mainTtl">
          <h1 class="mainTtl_h1">REMOSHA!</h1>
          <div class="mainTtl_txt">
          </div>
          <v-btn class="mainTtl_btn" nuxt to="/background">
            <span class="v-btn__content"></span>
          </v-btn>
        </div>
        <div class="mainImg">
        </div>
      </v-row>
    </div>
    <div class="a">
      <div class="ex">
        <p class="exTtl">REMOSHA!とは</p>
        <p class="exTtl_txt">オンラインイベントでも、<br>
          みんなと一緒に素敵な写真を撮りたい！<br>
          そんな気持ちに答えるwebサービスです。
        </p>
      </div>
      <div class="howTo">
        <div class="howTo_box"></div>
        <v-btn class="mainTtl_btn mainTtl_btnLower" nuxt to="/background">
          <span class="v-btn__content start"></span>
        </v-btn>
      </div>
    </div>
    <div>
      <div class="mt-5 center">
      </div>
    </div>
  </div>
</template>

<script>
  import Logo from '~/components/Logo.vue'
  import VuetifyLogo from '~/components/VuetifyLogo.vue'

  export default {
    components: {
      Logo,
      VuetifyLogo
    }
  }
</script>

<style lang="scss" scoped>
  .wrapper {
    margin: 0 auto;
  }

  .container {
    padding: 0;
    width: 100%;
  }

  .inner {
    max-width: 1400px;
    display: flex !important;
  }

  .mainTtl {
    position: relative;
    width: 330px;
    height: 800px;
    min-width: 330px;
    background: url(../assets/img_logo.png), $yellow;
    background-size: 250px auto;
    background-repeat: no-repeat;
    background-position: center 100px;
    &_h1 {
      text-indent: -9999px;
      width: 0;
      height: 0;
    }

    &_txt {
      position: absolute;
      top: 300px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 999;

      text-align: center;
      width: 100%;
      height: 100%;
      background: url(../assets/img_h1.png);
      background-size: 250px auto;
      background-repeat: no-repeat;
      background-position: center 100px;
    }

    .mainTtl_btn {
      position: absolute;
      z-index: 999;
      bottom: 150px;
      left: 50%;
      transform: translateX(-50%);
      width: 270px;
      height: 60px;
      margin-top: 0px;
      background-color: #272369;
    }
  }
  .v-btn__content {
    width: 88px;
    height: 32px;
    background: url(../assets/img_START.png);
    background-repeat: no-repeat;
    background-size: contain;
    background-position: center;
  }

  .mainTtl_btnLower {
    margin: 10px auto;
  }

  .mainImg {
    margin: auto 10px;
    padding: 20px;
    background-color: #fff;
    border: 3px solid $black;
    width: calc(100% - 370px);
    height: 506px;
    background: url(../assets/img_main.png), $yellow;
    background-repeat: no-repeat;
    background-size: contain;
    background-position: center;
  }

  .demo {
    width: 100%;
    height: 100px;
    // background-color: $yellow;
  }

  .ex {
    margin-top: 50px;

    .exTtl {
      text-align: center;
      font-size: 32px;
      font-weight: bold;

      &_txt {
        text-align: center;
        width: 700px;
        margin: 0 auto;
        padding: 10px 100px;
        font-size: 24px;
        font-weight: bold;
        line-height: 2;
      }
    }
  }

  .leftCol {
    background: $yellow;
    width: 330px;
    heihgt: 100%;
  }

  .howTo {
    width: 100%;
    margin-top: 50px;
    padding: 50px;
    background-color: $yellow;
    text-align: center !important;

    .howTo_box {
      margin: 0 auto;
      width: 800px;
      height: 300px;
      background: url(../assets/img_howtoUse.png), #fff;
      background-size: 780px auto;
      background-repeat: no-repeat;
      background-position: 50px center;
      border: 3px solid $black;
    }
  }


</style>
