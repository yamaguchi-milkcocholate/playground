<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div>
          <div class="mt-4">
            <h4>Left and Right (or Start and End)</h4>
            <b-card img-left class="mb-3">
              <b-card-text>
                <div class="row">
                  <div style="width: 300px; height: 300px">
                    <div id="canvas-area">
                      <canvas id="myCanvas" width="300" height="300"
                        @mousedown="dragStart"
                        @mouseup="dragEnd"
                        @mouseout="dragEnd"
                        @mousemove="draw"
                      ></canvas>
                    </div>
                  </div>
                  <div stype="width: 300px;">
                    <div>
                      <b-button
                        variant="danger"
                        type="button"
                        id="clear-button"
                        class='ml-2'
                        @click="clear"
                      >clear</b-button>
                      <b-button
                        variant="primary"
                        type="button"
                        id="submit-button"
                        class='ml-2'
                        @click="submit"
                      >done</b-button>
                    </div>
                  </div>
                </div>
              </b-card-text>
            </b-card>
          </div>

          <div v-for="(digit, index) in this.digits" :key="index">
            <img role="img" :src="tobase64(digit)">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  name: 'Mnist',
  data() {
    return {
      canvas: null,
      context: null,
      isDrag: false,
      digits: [],
    };
  },
  methods: {
    draw(e) {
      if (!this.isDrag) {
        return;
      }
      this.context.lineTo(e.layerX, e.layerY);
      this.context.stroke();
    },
    dragStart(e) {
      this.context.beginPath();
      this.context.lineTo(e.layerX, e.layerY);
      this.context.stroke();
      this.isDrag = true;
    },
    dragEnd() {
      this.context.closePath();
      this.isDrag = false;
    },
    clear() {
      this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.context.fillStyle = 'black';
      this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);
      this.digits = [];
    },
    submit() {
      /* eslint-disable */
      const imgData = this.context.getImageData(0, 0, this.canvas.width, this.canvas.height);
      const img = Array();
      imgData.data.forEach((val, idx) => {
        if (idx % 4 == 0) {
          img.push(val);
        }
      })

      axios({
        url: 'http://localhost:5000/api/mnist',
        method: 'post',
        data: {
          img: JSON.stringify(img),
          width: this.canvas.width,
          height: this.canvas.height,
          },
      }).then((res) => {
          console.log(res.data);
          this.digits = res.data.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    tobase64(binaryData) {
      console.log(binaryData);
      return "data:image/jpg;base64, " + binaryData.img_str;
    },
  },
  mounted() {
    this.canvas = document.querySelector('#myCanvas');
    this.context = this.canvas.getContext('2d');
    this.context.fillStyle = 'black';
    this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);
    this.context.lineCap = 'round';
    this.context.lineJoin = 'round';
    this.context.lineWidth = 10;
    this.context.strokeStyle = '#ffffff';
  },
};
</script>
<style scoped>
#myCanvas {
 border: 1px solid #000000;
}
</style>
