<template>
<v-app  v-if="loaded">
  <v-app-bar color="primary" dark class="d-flex justify-center" app>
    <v-toolbar-title>埼大ツイ廃同盟 & ツイッター研究会活動まとめ</v-toolbar-title>
  </v-app-bar>

  <v-main>
    <v-container>
      <v-select
        v-model="day"
        v-bind:items="dates"
        label="活動日"
        style="max-width: 180px"
        />
      <v-divider />
      <DailyDashboard v-if="day" :day="day" />
    <!-- <v-container> -->
    <!--   <v-row> -->
    <!--     <v-col> -->
    <!--       <CardRanking :thedata="thedata"/> -->
    <!--     </v-col> -->
    <!--     <v-col> -->
    <!--       <CardByTime :thedata="thedata"/> -->
    <!--     </v-col> -->
    <!--   </v-row> -->
    </v-container>
  </v-main>
</v-app>
</template>

<script>

import { mapActions, mapGetters } from 'vuex';

import DailyDashboard from './components/DailyDashboard';

export default {
  name: 'App',
  components: {
    DailyDashboard
  },
  data() {
    return {
      tweetcount_timeline_user: 'all',
      day: undefined
    };
  },
  computed: {
    ...mapGetters(['dates', 'loaded']),
  },
  watch: {
    loaded() {
      this.day = this.dates ? this.dates[this.dates.length - 1] : undefined;
    }
  },
  created() {
    this.fetchTheData();
  },
  methods: {
    ...mapActions(['fetchTheData'])
  }
}
</script>

<style>
</style>
