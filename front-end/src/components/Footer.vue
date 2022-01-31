<template>
  <footer class="text-lg-start bg-light text-muted">
    <div class="container">
        <div class="item-foot">
        <a href="https://europa.eu/" target="_blank"><img src="@/assets/img/eu-flag.png" alt="EU flag" class="logo" loading="lazy"></a>
        <a href="https://www.imi.europa.eu/" target="_blank"><img src="@/assets/img/imi-logo.png" alt="IMI logo" class="logo" loading="lazy"></a>
        <a href="https://efpia.eu" target="_blank"><img src="@/assets/img/efpia-logo.png" alt="EFPIA logo" class="logo" loading="lazy"></a>
        </div>
        <div class="item-foot copyright">
         Contact <a href="mailto:inb.hub@bsc.es">inb.hub@bsc.es</a> <br> Copyright © <a href="https://www.bsc.es/" target="_blank">BSC-CNS</a> 2022
        </div>
        <div class="item-foot">
              This project has received funding from the <a href="https://www.imi.europa.eu/">Innovative Medicines Initiative</a> Joint Undertaking under grant agreement No 802750.
              This Joint Undertaking receives support from the European Union’s Horizon 2020 research and innovation programme and EFPIA Companies.<br>
              This communication reflects the views of the authors and neither IMI nor the European Union, EFPIA or any Associated Partners are liable for any use that may be made of the information contained herein.
        </div>
        
      </div>
  </footer>
</template>
<style scoped>
  @import '../assets/bootstrap-5.1.3/dist/css/bootstrap.css';
  @import '../assets/css/custom.css';
  @import '../assets/fontawesome-free-5.15.4-web/css/all.css';

  footer .container{
    display: flex;
    flex-flow: row wrap;
    flex-basis: 1;
    flex-grow: 1;
    font-size: .75rem;
    justify-content: space-between;
    margin-bottom: 2em
  }

  footer{
    padding-top: 1%;
    font-size: smaller;
    margin-top: auto;
    width: 100%;
  }

  footer .item-foot{
    display: inline-block;
    vertical-align: middle;
    margin-top: 0%;
    margin-left: 1em
  }

  .logo{
    margin: 1em;
    margin-top: 0%;
    height: 3.5em;
  }
  .copyright{
    font-size: .7rem
  }

</style>
<script>

export default {
  name: 'Footer'
}
</script>
