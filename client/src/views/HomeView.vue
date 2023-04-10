<template>
  <div class="home">
    <WebCam/>
  </div>
</template>

<script>
// @ is an alias to /src
import WebCam from '@/components/WebCam.vue';

export default {
  name: 'HomeView',
  components: {
    WebCam,

  },
};
</script>
