<template>
  <div class="container" id="index-main">
    <h4>Overview</h4>
    <p>
    This is a biref description of what the Tool Discoverer is and what it does.
    </p>
    <br>
    <h4>What do you want to do?</h4>
    <br>
    <div class="row" id="index-cards">
      <div class="col-sm-4 d-flex align-items-stretch">
        <div class="card">
          <div class="card-image-top"><i class="fas fa-cogs fa-3x"></i></div>
            <div class="card-body" id="card-one">
              <h5 class="card-title">Run a Query</h5>
              <p class="card-text">Discover tools using a custom list of weighted keywords.</p>
              <a href="/run" class="btn">Go</a>
            </div>
          </div>
        </div>
        <div class="col-sm-4 d-flex align-items-stretch">
          <div class="card">
            <div class="card-image-top"><i class="fas fa-search fa-3x"></i></div>
            <div class="card-body" id="card-two">
              <h5 class="card-title">Explore FAIRification keywords</h5>
              <p class="card-text">We have prepared list of keywords to aid the dicovery of tools that can be used in different steps of a data FAIRification proccess.</p>
              <a href="#" class="btn">Go</a>
            </div>
          </div>
        </div>
        <div class="col-sm-4 d-flex align-items-stretch">
          <div class="card">
            <div class="card-image-top"><i class="fas fa-question-circle fa-3x"></i></div>
            <div class="card-body" id="card-three">
              <h5 class="card-title">Know more</h5>
              <p class="card-text">Find all the features and details of the the Tool Discoverer.</p>
              <a href="#" class="btn">Go</a>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style>
#index-main{
  font-size: small;
  margin-bottom: 3%;
  width: 98%;
}

</style>
<script>
export default {
  name: 'Home'
}
</script>
