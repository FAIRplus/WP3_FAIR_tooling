<template>
  <div class="container">
    <header class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom">
      <a class="d-flex align-items-center text-dark text-decoration-none">
        <span class="logo"><img src="@/assets/img/FAIRplus_logo.svg" width="20px"></span>
        <span class='brand-name'>FAIRification  <br>Tool Discoverer</span>
      </a>
      <b-nav class="col-12 col-md-auto mb-2 justify-content-center mb-md-0" active-class="active">
        <b-nav-item to="/">Home</b-nav-item>
        <b-nav-item to="/run">Run</b-nav-item>
        <b-nav-item to="/fairification" >FAIRification</b-nav-item>
        <b-nav-item to="/help" >Help</b-nav-item>
        <b-nav-item to="/about" >About</b-nav-item>
      </b-nav>
      <div class="col-md-2 text-end">
        <a href="https://github.com/FAIRplus/WP3_FAIR_tooling/tree/app" target='_blank' class="nav-link px-2 link-dark"><i class="fab fa-github fa-lg"></i></a>
      </div>
    </header>
  </div>
</template>
<style>
  @import '../assets/bootstrap-5.1.3/dist/css/bootstrap.css';
  @import '../assets/css/custom.css';
  @import '../assets/fontawesome-free-5.15.4-web/css/all.css';

  .nav-link{
    color: black!important;
    font-size: 1rem;
    background-color: white!important;
  }

  .nav-link.router-link-exact-active{
    color: grey!important;
  }

  .brand-name{
    font-weight: bolder;
    color: grey;
    text-align: left;
    padding-left: .9em;
    padding-top: .4em;
    font-size: 1rem;
  }
  .logo{
    margin-left: .7em
  }

</style>
<script>
export default {
  name: 'NavBar'
}
</script>
