<template>
  <v-card max-width="600" class="mt-3 d-flex flex-column align-center">
    <v-card-title>
      ツイ廃ランキング結果
    </v-card-title>
    <v-card-text>
      <v-list>
        <v-list-item
          v-for="r, i in thedata.ranking"
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
              {{thedata.users[r.screen_name].name}}
            </v-list-item-title>
            <v-list-item-subtitle>
              {{r.count}} 件 (全体の {{(100 * r.density).toFixed(2)}} %)
            </v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-avatar>
            <v-img
              :src="thedata.users[r.screen_name].profile_image_url"
              ></v-img>
          </v-list-item-avatar>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
  var SVG_WIDTH = 500;
  var SVG_ASPECT_RATIO = 12/5;
  var SVG_M_X = 10;
  var SVG_M_B = 50;
  var SVG_TEXT_OFFSET = 20;
  var SVG_XAXIS_OFFSET = 25;
export default {
  name: 'CardByTime',
  props: {
    thedata: { type: Object }
  },
  data() {
    return {
      user: 'all'
    };
  },
  computed: {

    select_users: function() {
      var r = this.thedata.users.map(function(x) {
        return {
          text: x.name,
          value: x.screen_name
        };
      });
      r.push({text: '全体', value: 'all'});
      return r;
    },
    tweetcount_timeline: function() {
      var root = this;
      return this.thedata.data_per_hour[this.user].map(
        function(x, i) {
          var y = JSON.parse(JSON.stringify(x));
          var h = root.svg_height * x.density;
          y.rect = {
            x: SVG_M_X + i * root.canvas_width / 24,
            y: root.svg_height - SVG_M_B - h,
            width: 0.5 * root.canvas_width / 24,
            height: h
          };
          y.text_count = {
            x: y.rect.x + y.rect.width / 2,
            y: y.rect.y - SVG_TEXT_OFFSET,
          }
          y.text_count.transform = `rotate(-90 ${y.text_count.x} ${y.text_count.y})`;
          y.text_labels = {
            x: y.rect.x + y.rect.width / 2,
            y: y.rect.y + y.rect.height + SVG_XAXIS_OFFSET
          }
          y.text_labels.transform = `rotate(-90 ${y.text_labels.x} ${y.text_labels.y})`;
          y.hour = String(i).padStart(2, '0') + ':00'
          return y;
        }
      );
    },
    svg_width: function() {
      return SVG_WIDTH;
    },
    svg_height: function() {
      return SVG_WIDTH / SVG_ASPECT_RATIO;
    },
    canvas_width: function() {
      return this.svg_width - SVG_M_X;
    }
  },
  methods: {
    starColor(i) {
      switch(i) {
      case 0: return '#CFB53B';
      case 1: return '#ACACAC';
      default: return '#A57164';
      }
    }
  }
}
</script>

<style scoped>
rect {
  fill: var(--v-primary-base);
  transition: 0.2s linear;
}
</style>
