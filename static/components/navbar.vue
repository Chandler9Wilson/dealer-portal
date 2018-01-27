<template>
  <div id="navbar">
    <ul>
      <li><a href="/home">home</a></li>
      <li><a href="/debug">[[ msg ]]</a></li>
      <li class="logout"><a href="/login?logout=true" onclick="logout()">logout</a></li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      msg: "Hello World"
    }
  }
}
</script>

<style scoped>
#navbar ul {
  margin: 0;
  padding: 5px;
  list-style-type: none;
  text-align: center;
  background-color: #000;
}

#navbar ul li {
  display: inline;
}

#navbar ul li a {
  text-decoration: none;
  padding: 0.2em 1em;
  color: #fff;
  background-color: #000;
}

#navbar ul li a:hover {
  color: #000;
  background-color: #fff;
}
</style>

