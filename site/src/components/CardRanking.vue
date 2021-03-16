<template>
  <v-card max-width="600" class="mt-3 d-flex flex-column align-center">
    <v-card-title>
      ツイ廃ランキング結果
    </v-card-title>
    <v-card-text>
      <v-list>
        <v-list-item
          v-for="r, i in ranking"
          :key="i"
          :href="`https://twitter.com/${r.screen_name}`"
          >
          <v-list-item-icon>
            <v-icon
              v-if="i < 3"
              :color="starColor(i)"
              >
              mdi-star
            </v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>
              {{users[r.screen_name].name}}
            </v-list-item-title>
            <v-list-item-subtitle>
              {{r.count}} 件 (全体の {{(100 * r.density).toFixed(2)}} %)
            </v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-avatar>
            <v-img
              :src="users[r.screen_name].profile_image_url"
              ></v-img>
          </v-list-item-avatar>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'CardByTime',
  props: {
    ranking: { type: Array }
  },
  computed: {
    ...mapGetters(['users'])
  },
  methods: {
    starColor(i) {
    console.log(this.ranking);
      switch(i) {
      case 0: return '#CFB53B';
      case 1: return '#ACACAC';
      default: return '#A57164';
      }
    }
  }
}
</script>
