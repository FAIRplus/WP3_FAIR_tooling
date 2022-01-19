<template>
  <footer class="text-lg-start bg-light text-muted">
    <div class="container">
      <p>The sole responsibility for the content of this webpage lies with BSC. It does not necessarily reflect the opinion of the European Union and the European Commission is not responsible for any use that may be made of the information contained therein.
      </p>
      <p>Copyright © BSC-CNS 2021
      Contact xxxx-support@bsc.es
      </p>
    </div>
  </footer>
</template>
<style>
  @import '../assets/bootstrap-5.1.3/dist/css/bootstrap.css';
  @import '../assets/css/custom.css';
  @import '../assets/fontawesome-free-5.15.4-web/css/all.css';

  footer .container{
    flex: 1 0 auto;
  }

  footer{
    padding-top: 1.5%;
    font-size: smaller;
    margin-top: auto;
    width: 100%;
  }

</style>
<script>

export default {
  name: 'Footer'
}
</script>
