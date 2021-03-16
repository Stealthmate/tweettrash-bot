<template>
<v-container>
  <v-row>
    <v-col>
      <CardRanking :ranking="thedata[day].ranking" />
    </v-col>
    <v-col>
      <CardByTime :timedata="thedata[day].timedata" />
    </v-col>
  </v-row>
</v-container>
</template>
<script>

import { mapGetters } from 'vuex';

import CardByTime from './CardByTime';
import CardRanking from './CardRanking';

export default {
  name: 'DailyDashboard',
  components: {
    CardByTime,
    CardRanking
  },
  props: {
    day: { type: String }
  },
  computed: {
    ...mapGetters(['thedata'])
  }
}
</script>
