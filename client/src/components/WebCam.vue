<template>
  <div class="WebCam">
    <h1>Vehicle Enumeration System</h1>
    <img  v-if="frameSrc" :src="frameSrc" alt="Video feed" />
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
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
