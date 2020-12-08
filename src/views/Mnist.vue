<template>
  <div class="about">
    <div class="pad">
        <div>
          <div id="canvas-area">
            <canvas id="myCanvas" width="300" height="300" @mousedown="dragStart" @mouseup="dragEnd" @mouseout="dragEnd" @mousemove="draw"></canvas>
          </div>
          <div id="bottun-area" class="m-3">
            <b-button variant="outline-secondary" type="button" id="clear-button" class='mr-2' @click="clear">clear</b-button>
            <b-button variant="outline-success" type="button" id="submit-button" class="ml-2" @click="submit">run</b-button>
          </div>
        </div>
      </div>
      <div id="terminal">
        <div id="terminal-header">
          <div class="terminal-tab" v-bind:class="{'terminal-tab-active' : this.activeTerminalTab == 'terminal'}" @click="changeTerminal('terminal')">
            <p>ターミナル</p>
          </div>
          <div class="terminal-tab" v-bind:class="{'terminal-tab-active' : this.activeTerminalTab == 'output'}" @click="changeTerminal('output')">
            <p>出力</p>
          </div>
          <div class="terminal-tab" v-bind:class="{'terminal-tab-active' : this.activeTerminalTab == 'console'}" @click="changeTerminal('console')">
            <p>デバックコンソール</p>
          </div>
        </div>
        <div id="terminal-body">
          <div v-show="this.activeTerminalTab == 'terminal'">
            <div class="d-flex">
              <div v-for="(digit, index) in this.digits" :key="index" class="mt-3 ml-3">
                <h3>{{digit.prediction}}</h3>
                <img role="img" :src="tobase64(digit)">
              </div>
            </div>
          </div>
          <div v-show="this.activeTerminalTab == 'output'">
            <p>|</p>
          </div>
          <div v-show="this.activeTerminalTab == 'console'">
            <p>|</p>
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
      activeTerminalTab: 'terminal',
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
        url: '/api/mnist',
        method: 'post',
        data: {
          img: JSON.stringify(img),
          width: this.canvas.width,
          height: this.canvas.height,
          },
      }).then((res) => {
          this.digits = res.data.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    tobase64(binaryData) {
      return "data:image/jpg;base64, " + binaryData.img_str;
    },
    changeTerminal(name) {
      this.activeTerminalTab = name;
    }
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
#canvas-area {
  width: 300px;
  height: 300px;
  padding: 1px;
  margin: 1rem auto 0px auto;
  border: solid 1px rgb(60, 60, 60);
  box-sizing: content-box;
}

#button-area {
  width: 300px;
}

.about {
  background: rgb(30, 30, 30);
  margin-left: 100px;
}

#terminal {
  border-top: solid 1px rgb(60, 60, 60);
}

#terminal-header {
  width: 100%;
  display: flex;
  font-size: 12px;
}

.terminal-tab {
  color: rgb(150, 150, 150);
}

.terminal-tab:hover {
  color: white;
  cursor: pointer ;
}

.terminal-tab-active {
  color: white;
}

.terminal-tab p {
  padding: 10px 0px;
  margin: 0px 15px;
}

.terminal-tab-active p {
  border-bottom: solid 1px white;
}

.terminal-body {
  width: 100%;
}
</style>
