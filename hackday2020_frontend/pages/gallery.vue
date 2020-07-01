<template>
  <v-container>
    <v-row>
      <v-col
        v-for="(image,index) in images"
        :key="index"
        class="d-flex child-flex"
        cols="3"
      >
        <a :href="setImage(image)">
        <v-card flat tile class="d-flex border">
          <v-img
            :src="setImage(image)"
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
        </a>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import axios from "axios"

  export default {
    data: function(){
      return{
        images: []
      }
    },
    created() {
      axios.get('/list')
      .then(response => {
        this.images = response.data.image[0]
        console.log(this.images)
      })
      .catch(error => {
        console.log(error);
      })
    },
    methods:{
      setImage(imageName){
        return "http:34.84.177.20:9000/image/" + imageName
      }
    }
  }
</script>

<style lang="scss" scoped>

</style>

