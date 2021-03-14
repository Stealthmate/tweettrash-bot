<template>
<v-app  v-if="loaded">
  <v-app-bar color="primary" dark class="d-flex justify-center" app>
    <v-toolbar-title>埼大ツイ廃同盟 & ツイッター研究会活動記録 ({{thedata.day}})</v-toolbar-title>
  </v-app-bar>
  <v-main>
    <v-container>
      <v-row>
        <v-col>
          <CardRanking :thedata="thedata"/>
        </v-col>
        <v-col>
          <CardByTime :thedata="thedata"/>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</v-app>
</template>

<script>

import axios from "axios";

import CardByTime from './components/CardByTime';
import CardRanking from './components/CardRanking';

export default {
  name: 'App',
  components: {
    CardByTime,
    CardRanking
  },
  data() {
    return {
      tweetcount_timeline_user: 'all',
      thedata: undefined
    };
  },
  computed: {
    loaded() {
      return this.thedata !== undefined;
    },
  },
  created() {
    this.fetch();
  },
  methods: {
    fetch() {
      axios.get('./site-data.json').then(response => {
        console.log(response.data);
        this.thedata = response.data;
      });
    }
  }
}
</script>

<style>
</style>
