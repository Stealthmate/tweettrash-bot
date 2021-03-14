<template>
  <v-card max-width="600" class="mt-3 d-flex flex-column align-center">
    <v-card-title>
      ツイート数
    </v-card-title>
    <v-card-text class="d-flex justify-center" >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        version="1.1"
        v-bind:width="svg_width" v-bind:height="svg_height" v-bind:viewBox="`0 0 ${svg_width} ${svg_height}`">
        <g>
          <rect
            v-for="(d, i) in tweetcount_timeline"
            v-bind:key="i"
            v-bind="d.rect"
            />
        </g>
        <g>
          <text
            v-for="(d, i) in tweetcount_timeline"
            v-bind:key="i"
            v-bind="d.text_count"
            text-anchor="middle"
            dominant-baseline="central"
            >{{d.count}}</text>
        </g>
        <g>
          <text
            v-for="(d, i) in tweetcount_timeline"
            v-bind:key="i"
            v-bind="d.text_labels"
            text-anchor="middle"
            dominant-baseline="central"
            font-size="0.8em"
            >{{d.hour}}</text>
        </g>
      </svg>
    </v-card-text>
    <v-card-actions class="align-self-end">
      <v-select
        v-model="user"
        v-bind:items="select_users"
        label="ツイ廃を選択"
        default="all"
        dense
        style="width: 300px"
        />
    </v-card-actions>
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

    select_users() {
      let us = this.thedata.users;
      let r = Object.keys(us).map(k => {
        return {
          text: us[k].name,
          value: us[k].screen_name
        };
      });
      r.push({text: '全体', value: 'all'});
      return r;
    },
    tweetcount_timeline: function() {
      var root = this;
      return this.thedata.by_time[this.user].map(
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
  }
}
</script>

<style scoped>
rect {
  fill: var(--v-primary-base);
  transition: 0.2s linear;
}
</style>
