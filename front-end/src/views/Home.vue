<template>
  <div class="container" id="index-main">
    <h4>The FAIRification tool discoverer</h4>
    <p>
    Discovering tools for your FAIRification tasks

    </p>
    <br>
    <h4>What do you want to do?</h4>
    <br>
    <div class="container" id="index-cards">
    <div class="row" >
      <div class="col-sm-4 d-flex align-items-stretch">
        <div class="card">
          <div class="card-image-top"><i class="fas fa-cogs fa-3x"></i></div>
            <div class="card-body" id="card-one">
              <h5 class="card-title">Run a Query</h5>
              <p class="card-text">Discover tools using a custom list of weighted keywords.</p>
              <div class="spacer"></div>
              <div class='btn-cont'><a href="/run" class="btn">Go</a></div>
            </div>
          </div>
        </div>
        <div class="col-sm-4 d-flex align-items-stretch">
          <div class="card">
            <div class="card-image-top"><i class="fas fa-search fa-3x"></i></div>
            <div class="card-body" id="card-two">
              <h5 class="card-title">Explore FAIRification tools</h5>
              <p class="card-text">Learn more about the FAIRification proccess and the tools for each step.</p>
              <div class="spacer"></div>
              <div class='btn-cont'><a href="/fairification" class="btn">Go</a></div>
            </div>
          </div>
        </div>
        <div class="col-sm-4 d-flex align-items-stretch">
          <div class="card">
            <div class="card-image-top"><i class="fas fa-question-circle fa-3x"></i></div>
            <div class="card-body" id="card-three">
              <h5 class="card-title">Know more</h5>
              <p class="card-text">Find all the features and details of the the Tool Discoverer.</p>
              <div class="spacer"></div>
              <div class='btn-cont'><a href="/help" class="btn">Go</a></div>
            </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>
<style scoped>
#index-main{
  font-size: small;
  margin-bottom: 3%;
  width: 98%;
}

#index-cards{
  justify-content: space-around
}

.card{
  text-align: center;
  margin: auto;
  height: 100%;
}

.card .card-image-top{
  padding-top: 5%;
  width: 30%;
  margin: auto;
  margin-top: 1em
}

.card .card-body{
  position: relative;
}

.card .card-text{
  margin-bottom: 1em;
  margin-top: 1em
}

.card >>> .btn-cont{
  position: absolute;
  bottom: 2em;
  left: 50%;
  transform: translateX(-50%); /* Move 50% of own width to the left*/
}

.card >>> .btn{
  margin: 0%
}
.card .card-image-top .fas{
  color: grey;
}

.spacer{
  width: 3em; 
  height: 4.2em; 
  margin-right:0px;
}

#card-one .btn{
  background-color: #300761;
  color: white;
}

#card-two .btn{
  background-color: #4f4b49;
  color:white;
}

#card-three .btn{
  background-color: #900048;
  color:white;
}

</style>
<script>
export default {
  name: 'Home'
}
</script>
