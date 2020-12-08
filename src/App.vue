<template>
  <div id="app">
    <div id="side-bar">

    </div>
    <div id="nav">
        <router-link to="/">Home</router-link>
        <router-link to="/mnist">MNIST</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: rgb(51, 51, 51);
  min-height: 100vh;
  max-height: 100vh;
  background: rgb(30, 30, 30);
}

#nav {
  /* padding: 30px; */
  background: rgb(51, 51, 51);
  display: flex;
  margin-left: 100px;
}

#nav a {
  font-weight: bold;
  color: white;
  padding: 15px 30px;
  box-sizing: border-box;
}

#nav a.router-link-exact-active {
  color: #42b983;
  background: rgb(30, 30, 30);
}

/* .tab {
  max-width: 100px;
  padding: 15px 50px;
} */

.tab:hover {
  cursor: pointer;
}

#side-bar {
  width: 100px;
  min-height: 100vh;
  background: rgb(51, 51, 51);
  color: white;
  position: fixed;
}

#main {

}
</style>
