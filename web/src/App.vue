
<style>
#canvas {
    width:2000px;
    height:2000px;
    border: 10px solid transparent;
}
.rectangle {
    border: 1px solid #FF0000;
    position: absolute;
}
</style>

<template>
  <v-app id="inspire">
    <v-toolbar color="indigo" dark fixed app>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-toolbar-title>Co-Operative Labling</v-toolbar-title>
    </v-toolbar>

    <v-content>
      <Labler/>
    </v-content>
    
    <v-footer color="indigo" app>
      <span class="white--text">&copy; 2019</span>
    </v-footer>
  </v-app>
</template>

<script>
import Labler from './components/Labler'

export default {
  name: 'App',
  components: {
    Labler,
  },
  data() {
    return {
      //
    }
  },
}
</script>
