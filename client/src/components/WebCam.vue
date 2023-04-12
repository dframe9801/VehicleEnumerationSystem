<template>
  <div class="WebCam">
    <div class="container text-center">
      <div class="row">
        <div class="col-2 border">
          <div class="counter-container">
            <p>Counter</p>
            <div class="counter-box">
              <span class="counter">0</span>
            </div>
          </div>
        </div>
        <div class="col border">
          Stream
          <img  v-if="frameSrc" :src="frameSrc" alt="Video feed" class="img-thumbnail" />
        </div>
      </div>
      <div class="row">
        <div class="col border">
          <CPMGraph />
        </div>
        <div class="col border">
          <CPMGraph />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import CPMGraph from './CarsPerMinGraph.vue';

export default {
  name: 'WebCam',
  components: { CPMGraph },
  data() {
    return {
      frameSrc: null,
    };
  },
  mounted() {
    this.fetchFrames();
  },
  methods: {
    async fetchFrames() {
      try {
        const response = await axios.get('http://localhost:5000/video_feed');
        if (response.data.success) {
          this.frameSrc = `data:image/jpeg;base64,${response.data.frame}`;
        } else {
          console.error('Failed to fetch frame');
        }
      } catch (error) {
        console.error('Error fetching frame:', error);
      } finally {
        setTimeout(() => this.fetchFrames(), 10);
      }
    },
  },
};
</script>

<style scoped>
.counter-box {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    width: 100px;
    height: 100px;
    border: 2px solid #333;
    border-radius: 5px;
    background-color: #f7f7f7;
}

.counter {
    font-size: 32px;
    font-weight: bold;
    color: #333;
}

.counter-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px;
}
</style>
