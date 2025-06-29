<script setup lang="ts">
import { RouterView } from 'vue-router'
import "bootstrap"
import 'bootstrap/dist/js/bootstrap.bundle.js';
import 'bootstrap/js/dist/dropdown';

</script>

<template>

  <header style = "top:0px; position: absolute ; width: 100%; min-width:1200px; z-index: 1;">
    <nav class="navbar navbar-expand-lg" style = "background-color: #e3f2fd;">
      <div class="container-fluid">
        
        <img src = "/game.png" style = "height: 50px; margin-left: 30px;">

        <button class="navbar-toggler" type = "button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class = "collapse navbar-collapse" id = "navbarNavDropdown" style="height: 45px;">
          <ul class = "navbar-nav me-auto mb-2 mb-lg-0">
            
            <li class="nav-item" style = "margin-left: 30px; margin-right: 15px;">
              <a class="nav-link active" aria-current="page" href = "\"> 首頁 </a>
            </li>

            <li class="nav-item dropdown" style = "margin-left: 15px; margin-right: 15px;">
              <!-- <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" 
                data-bs-toggle="dropdown" aria-expanded="false">
                其它功能
              </a> -->

              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                其它功能
              </a>
              <ul class = "dropdown-menu">
                <li>
                  <a class="dropdown-item" href = "\production_management"> 商品管理 </a>
                </li>
                <li>
                  <a class="dropdown-item" href = "\selling"> 商品售出 </a>
                </li>
                <li>
                  <a class="dropdown-item" href = "\report"> 報表輸出 </a>
                </li>
              </ul>

            </li>

          </ul>
        </div>
      </div>
    </nav>
    
    <!-- <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Navbar</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Link</a>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Dropdown
          </a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">Action</a></li>
            <li><a class="dropdown-item" href="#">Another action</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">Something else here</a></li>
          </ul>
        </li>
        <li class="nav-item">
          <a class="nav-link disabled" aria-disabled="true">Disabled</a>
        </li>
      </ul>
      <form class="d-flex" role="search">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"/>
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
    </div>
  </div>
</nav> -->
  </header>

  

  <Suspense>
    <template #fallback>
      <div> Loading... </div>
    </template>
  </Suspense>
  
  <RouterView style = "width:100%; min-width:1200px; padding-left: 10px;padding-right: 10px; position: relative; top:80px; height:auto;" />

  <footer class = "footer-div" >
    <p> &copy; 2025 For Video Game Store </p>
  </footer>

</template>

<style scoped>
/* header {
  line-height: 1.5;
  max-height: 100vh;
} */

.logo {
  display: block;
  margin: 0 auto 2rem;
}

.footer-div{
  position: relative; 
  bottom: -120px; 
  padding-top: 20px; 
  padding-bottom: 10px;

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
}

/* nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
} */

/* nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
} */

/* @media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
} */

button{
  width:200px;
  height: 60px;
}
</style>
