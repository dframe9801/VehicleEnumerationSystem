<template>
  <div class="home">
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
          <WebCam />
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
// @ is an alias to /src
import WebCam from '@/components/WebCam.vue';
import CPMGraph from '@/components/CarsPerMinGraph.vue';

export default {
  name: 'HomeView',
  components: {
    WebCam,
    CPMGraph,

  },
};
</script>

<style>
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
