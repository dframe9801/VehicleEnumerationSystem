<template>
  <div class="WebCam">
    <div class="container text-center">
      <div class="row">
        <div class="col-2 bg-secondary">
          Column
        </div>
        <div class="col">
          Column
        </div>
      </div>
    </div>
   <!-- <img  v-if="frameSrc" :src="frameSrc" alt="Video feed" /> -->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'WebCam',
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

</style>
