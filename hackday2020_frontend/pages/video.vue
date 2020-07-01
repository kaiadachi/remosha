<template>
  <div id="wrapper">
    <div id="app">
      <v-app-bar
        app
        class="header"
      >
        <v-toolbar-title class="center">REMOSHA!</v-toolbar-title>
      </v-app-bar>
    </div>
    <div>
      <div class="videoBox">
        <div>
          <div id="video-1" class="video"/>
          <div id="video-2" class="video"/>
          <div id="video-3" class="video"/>
          <div id="video-4" class="video"/>
        </div>
        <div id="canvas-wrapper">
          <canvas id="canvas-bg" class="canvasBg" ref="canvasBg"/>
          <canvas id="canvas-1" class="canvas" ref="canvas1"/>
          <canvas id="canvas-2" class="canvas" ref="canvas2"/>
          <canvas id="canvas-3" class="canvas" ref="canvas3"/>
          <canvas id="canvas-4" class="canvas" ref="canvas4"/>
        </div>
      </div>
      <div class="mb-10 videoBox_btn">
        <button class="videoBox_btnContent" olor="info" id="snap" v-on:click="capture()">SAVE</button>
      </div>
      <div class="linkBox">
        共有リンク | {{this.getUrl()}}
      </div>

    </div>
  </div>
</template>

<script>
  import AgoraRTC from 'agora-rtc-sdk';
  import axios from "axios"
  import pico from 'pico-face-detect';

  export default {
    data: function () {
      return {
        video: {},
        resCanvas: {},
        canvas: {},
        canvasBg: {},
        canvasRefs: {},
        captures: [],
        rtc: {},
        videoSource: {},
        context: {},
        facefinder_classify_region: {},
        client: {},
        update_memory: {},
        dets_memory: {},
        streamList: [],
        uidList: [],
        index: 1,
        detectCount: {},
        selfInitialized: false,
        readyState: false,
      }
    },

    created: function () {
      // リロードで同じクライアントを作らないようにする
      if (this.selfInitialized) {
        return;
      }
      const appId = "dccc7d43a4c8416e8e56e97572a40edf";
      // 一旦同じチャンネルにするが、部屋番号などを渡してあげるのが望ましい
      const channel = "remosha-jusato";
      const streamID = "remosha-jusato";

      this.client = AgoraRTC.createClient({mode: `live`, codec: `vp8`});
      this.client.init(appId, () => {
        this.subscribeStreamEvents();
        this.client.join(appId, channel, null, uid => {
          console.log("User " + uid + " join channel successfully");
          console.log("At " + new Date().toLocaleTimeString());
          this.localStream = this.streamInit(streamID);
          this.localStream.init(
            () => {
              this.addStream(this.localStream, true);
              this.client.publish(this.localStream, err => {
                console.log("Publish local stream error: " + err);
              });
              this.readyState = true;
              const domId = "video-" + this.index;
              console.log(`domId: ${domId}, uid: ${uid}`);
              this.uidList.push(uid);
              this.localStream.play(domId, {fit: `cover`, muted: true});
              // uidごとに物体検出のメモリを保持する
              this.update_memory[uid] = pico.instantiate_detection_memory(5);
              this.crop(uid, this.index)
              this.index += 1;
              this.selfInitialized = true;
            },
            err => {
              console.log("getUserMedia failed", err);
              this.readyState = true;
            }
          );
        })
      })
    },

    mounted() {
      this.canvasRefs = [this.$refs.canvas1, this.$refs.canvas2, this.$refs.canvas3, this.$refs.canvas4]

      // pico
      this.facefinder_classify_region = function (r, c, s, pixels, ldim) {
        return -1.0;
      };
      let cascadeurl = 'https://raw.githubusercontent.com/nenadmarkus/pico/c2e81f9d23cc11d1a612fd21e4f9de0921a5d0d9/rnt/cascades/facefinder';
      fetch(cascadeurl).then((response) => {
        console.log(response);
        response.arrayBuffer().then((buffer) => {
          let bytes = new Int8Array(buffer);
          this.facefinder_classify_region = pico.unpack_cascade(bytes);
        })
      });

      this.canvasBg = this.$refs.canvasBg;
      const url = "backgrounds/" + this.$route.query.background
      this.canvasBg.style.backgroundImage = `url(${url})`;
      this.canvasBg.height = 720;
      this.canvasBg.width = 1280;
      this.canvasBg.className = `canvas`;
    },

    methods: {
      getUrl: function () {
        return location.href;
      },
      drawLoop: function (uid, video, canvas, context) {
        let qthresh = 10.0;

        let radius, dx, dy;
        context.globalCompositeOperation = 'source-over';
        context.drawImage(video, 0, 0, video.width, video.height);

        let detectEnable = false;
        let date = new Date();
        let millisec = date.getTime();
        // 初期化
        if (this.detectCount[uid] === undefined) {
          this.detectCount[uid] = millisec;
        } else {
          if (millisec - this.detectCount[uid] > 1000) {
            detectEnable = true;
            this.detectCount[uid] = millisec;
          } else {
            detectEnable = false;
          }
        }

        if (detectEnable) {
          // rgbaの値を取る
          let rgba = context.getImageData(0, 0, video.width, video.height).data;
          let image = {
            "pixels": this.rgba_to_grayscale(rgba, video.height, video.width),
            "nrows": video.height,
            "ncols": video.width,
            "ldim": video.width
          }
          let params = {
            "shiftfactor": 0.1,
            "minsize": 100,
            "maxsize": 1000,
            "scalefactor": 1.1
          }
          let dets = pico.run_cascade(image, this.facefinder_classify_region, params);
          // uidごとに物体検出のメモリを保持している
          dets = this.update_memory[uid](dets);
          dets = pico.cluster_detections(dets, 0.2);
          // 推定に成功した時だけ顔検出部分を更新する
          if (dets.length >= 1 && dets[0][3] > qthresh) {
            this.dets_memory[uid] = dets
          }
        }

        let dets = this.dets_memory[uid];
        if (dets !== undefined && dets.length >= 1 && dets[0][3] > qthresh) {
          context.globalCompositeOperation = 'destination-in';
          const dx = dets[0][1];
          const dy = dets[0][0];
          const radius = dets[0][2] / 2 * 1.2;
          context.beginPath();
          context.arc(dx, dy, radius, 0, Math.PI * 2, false);
          context.fill();
        }

        requestAnimationFrame(this.drawLoop.bind(null, uid, video, canvas, context));
      },

      rgba_to_grayscale: function (rgba, nrows, ncols) {
        var gray = new Uint8Array(nrows * ncols);
        for (var r = 0; r < nrows; ++r) {
          for (var c = 0; c < ncols; ++c) {
            gray[r * ncols + c] = (2 * rgba[r * 4 * ncols + 4 * c] + 7 * rgba[r * 4 * ncols + 4 * c + 1] + 1
              * rgba[r
              * 4 * ncols + 4 * c + 2]) / 10;
          }
        }
        return gray;
      },

      streamInit(streamID) {
        // 一旦streamIDをremoshaで固定（誰でも同じ部屋になる）
        return AgoraRTC.createStream({
          streamID: streamID,
          audio: true,
          video: true,
          screen: false,
        });
      },

      addStream(stream, push = false) {
        let repeatition = this.streamList.some(item => {
          return item.getId() === stream.getId();
        });
        if (repeatition) {
          return;
        }
        if (push) {
          this.streamList = this.streamList.concat([stream]);
        } else {
          this.streamList = [stream].concat(this.streamList);
        }
      },

      subscribeStreamEvents() {
        this.client.on("stream-added", (evt) => {
          console.log("stream-added was called")
          let stream = evt.stream;
          console.log("New stream added: " + stream.getId());
          console.log("At " + new Date().toLocaleTimeString());
          console.log("Subscribe ", stream);
          this.client.subscribe(stream, (err) => {
            console.log("Subscribe stream failed", err);
          });
        });

        this.client.on("peer-leave", (evt) => {
          console.log("peer-leave was called")
          console.log("Peer has left: " + evt.uid);
          console.log(new Date().toLocaleTimeString());
          console.log(evt);
          this.removeStream(evt.uid);
        });

        this.client.on("stream-subscribed", (evt) => {
          console.log("streamd-subscribed was called")
          let stream = evt.stream;
          if (this.uidList.length === 4) {
            console.warn("cannot subscribed, max 4 people");
            return
          }
          console.log("Got stream-subscribed event");
          console.log(new Date().toLocaleTimeString());
          console.log("Subscribe remote stream successfully: " + stream.getId());
          console.log(evt);
          const domId = "video-" + this.index;
          console.log(`domId: ${domId} is played`)
          stream.play(domId, {conver: "cover", muted: false})
          const uid = evt.stream.params.uintUID;
          this.uidList.push(uid);
          // uidごとに物体検出のメモリを保持する
          console.log(`uid: ${uid} was given`);
          this.update_memory[uid] = pico.instantiate_detection_memory(5);
          this.crop(uid, this.index);
          this.index += 1;
          this.addStream(stream);
        });

        this.client.on("stream-removed", (evt) => {
          console.log("streamd-removed was called")
          let stream = evt.stream;
          console.log("Stream removed: " + stream.getId());
          console.log(new Date().toLocaleTimeString());
          console.log(evt);
          this.removeStream(stream.getId());
        });
      },

      capture() {
        let fields = []
        for (let i = 0; i < this.index; i++) {
          const uid = this.uidList[i];
          if (uid === undefined) {
            // ないのに参照してることがあるので
            continue;
          }
          const base64image = this.canvasRefs[i].toDataURL('image/png')
          fields.push({"image": base64image, "uid": uid});
        }
        const images = {
          "images": fields,
          "background": this.$route.query.background,
        }
        console.log(`images: ${fields.length}`)

        axios.post('/getImage', images)
          .then(response => {
            window.open('/gallery', '_blank');
          })
          .catch(error => {
            console.log(error);
          })
      },

      crop: function (uid, index) {
        console.log(`crop was called, index: ${index}, uid: ${uid}`);
        // uidから描画すべきdomを選択する
        let video = document.getElementById(`video${uid}`);
        video.width = 1280;
        video.height = 720;
        video.className = "video";

        let canvas = document.getElementById(`canvas-${index}`);
        canvas.height = video.height;
        canvas.width = video.width;
        canvas.className = `canvas`;
        let context = canvas.getContext('2d');

        video.onloadedmetadata = () => {
          this.drawLoop(uid, video, canvas, context);
        };
      },

    }
  }
</script>

<style lang="scss" scoped>
  #videos {
    padding: 0 0;
  }

  #canvas-wrapper {
    position: relative;
  }

  .canvas {
    position: absolute;
    transform: scale(-1, 1);
    border-radius: 10px;
  }

  .video {
    width: 0%;
    height: 0%;
    visibility: hidden;
  }

  li {
    list-style-type: none;
  }

  button {
    z-index: 10;
    position: absolute;
  }

  .center {
    font-weight: bold;
  }

  .videoBox {
    margin: 0 auto;
    // 枠の太さで6px足す
    width: 1286px;
    height: 726px;
    background-color: #fff;
    border: 3px solid $black;
    border-radius: 10px;
    padding-top: 0px;
  }

  .videoBox_btn {
    position: relative;

    .videoBox_btnContent {
      width: 80px;
      height: 80px;
      position: absolute;
      top: -40px;
      left: 50%;
      transform: translateX(-50%);
      background-color: #fff;
      border: 3px solid $black;
      border-radius: 80px;
    }
  }

  .linkBox {
    position: relative;
    padding: 10px 20px;
    width: 700px;
    height: 60px;
    margin: 10px auto;
    background-color: #fff;
    box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    line-height: 2.5;

    &_txt {
      color: $black;
      font-size: 16px;
    }
  }

</style>
