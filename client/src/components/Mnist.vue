<template>
  <div class="container">
    <div>
      <div id="canvas-area">
        <canvas id="myCanvas" width="200" height="200"
          @mousedown="dragStart" @mouseup="dragEnd" @mouseout="dragEnd" @mousemove="draw"
        ></canvas>
      </div>
      <div style="padding:10px">
        <button type="button" id="clear-button" @click="clear">clear</button>
        <button type="button" id="submit-button" @click="submit">done</button>
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
        })
        .catch((error) => {
          console.error(error);
        });
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
