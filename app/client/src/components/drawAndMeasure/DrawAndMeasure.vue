<template>
  <v-flex xs12 sm8 md4>
    <v-card flat>
      <v-card-title primary-title>
        <span class="title font-weight-regular">{{
          $t("appBar.drawAndMeasure.title")
        }}</span>
      </v-card-title>
      <v-card-text class="pr-16 pl-16 pt-0 pb-0 mb-2">
        <v-divider></v-divider>
      </v-card-text>
      <v-subheader
        ><h3>{{ $t("appBar.drawAndMeasure.measure.header") }}</h3>
      </v-subheader>
      <v-divider></v-divider>

      <!-- Measure -->
      <v-expansion-panel class="elevation-0">
        <v-expansion-panel-content
          expand-icon=""
          readonly
          v-for="item in measureItems"
          :key="item.id"
          :class="{
            'expansion-panel__container--active': activeId === item.id
          }"
          @click.native="toggle(item.id, 'measure')"
        >
          <div slot="header">
            <v-layout row>
              <v-flex xs2>
                <v-icon
                  small
                  left
                  :class="{ activeIcon: activeId === item.id }"
                  >{{ item.icon }}</v-icon
                >
              </v-flex>
              <v-flex xs10>
                <span>{{ item.text }}</span>
              </v-flex>
            </v-layout>
          </div>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-divider class="mb-3"></v-divider>

      <!-- Draw -->
      <v-subheader>
        <h3>{{ $t("appBar.drawAndMeasure.draw.header") }}</h3>
      </v-subheader>
      <v-divider></v-divider>
      <v-expansion-panel class="elevation-0">
        <v-expansion-panel-content
          expand-icon=""
          v-for="item in drawItems"
          :key="item.id"
          :class="{
            'expansion-panel__container--active': activeId === item.id
          }"
          @click.native="toggle(item.id, 'draw')"
        >
          <div slot="header">
            <v-layout row>
              <v-flex xs2>
                <v-icon
                  small
                  left
                  :class="{ activeIcon: activeId === item.id }"
                  >{{ item.icon }}</v-icon
                >
              </v-flex>
              <v-flex xs8>
                <span>{{ item.text }}</span>
              </v-flex>
              <v-flex xs2>
                <v-icon class="close" v-bind:ref="item.id">{{
                  activeId === item.id ? "close" : ""
                }}</v-icon>
              </v-flex>
            </v-layout>
          </div>
          <v-card @click.stop="doNothing" class="card">
            <v-card-text>
              <!--Color Settings  -->
              <v-layout row wrap align-center class="ml-3">
                <v-flex xs4>
                  <span>{{ $t("appBar.drawAndMeasure.draw.color") }}</span>
                </v-flex>
                <v-flex xs8>
                  <swatches
                    @input="colorChange"
                    class="ml-3"
                    v-model="colors.selected"
                    colors="text-advanced"
                    swatch-size="24 "
                    popover-to="left"
                    :exceptions="colors.exceptions"
                  ></swatches>
                </v-flex>
              </v-layout>

              <!--Transparency Settings -->
              <v-layout row wrap align-center class="ml-3">
                <v-flex xs4>
                  <span>{{
                    $t("appBar.drawAndMeasure.draw.transparency")
                  }}</span>
                </v-flex>
                <v-flex xs8 class="pl-4 pr-3">
                  <v-slider
                    v-model="transparency"
                    @change="transparencyChange"
                    min="1"
                    max="100"
                  ></v-slider>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-divider></v-divider>

      <v-card-text> </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="white--text" color="green" @click="clear">{{
          $t("appBar.drawAndMeasure.clear")
        }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-flex>
</template>

<script>
import Swatches from "vue-swatches";
import "vue-swatches/dist/vue-swatches.min.css";

export default {
  components: { Swatches },
  data: () => ({
    stroke: "2",
    colors: {
      selected: "#3c78d8",
      exceptions: ["#FFFFFF", "#000000"]
    },
    transparency: 100,
    measureItems: [
      {
        id: 1,
        icon: "fas fa-ruler",
        text: "Length" //this.$t("appBar.drawAndMeasure.measure.length")
      },
      {
        id: 2,
        icon: "fas fa-ruler-combined",
        text: "Area"
      }
    ],
    drawItems: [
      {
        id: 3,
        icon: "far fa-dot-circle",
        text: "Point"
      },
      {
        id: 4,
        icon: "fas fa-dot-circle",
        text: "Point with coordinates"
      },
      {
        id: 5,
        icon: "fas fa-project-diagram",
        text: "Line"
      },
      {
        id: 6,
        icon: "fas fa-draw-polygon",
        text: "Polygon"
      },
      {
        id: 7,
        icon: "fas fa-font",
        text: "Label"
      }
    ],
    activeId: undefined
  }),
  computed: {},
  methods: {
    toggle(id, type) {
      //1- Set active index of clicked item or remove it
      //- If type is measure  toggle off drawing section if opened
      if (type === "measure") this.closeDrawSection();
      if (this.activeId === id) {
        this.activeId = undefined;
      } else {
        this.activeId = id;
      }
    },
    doNothing() {},
    clear() {
      if (this.activeId !== undefined) {
        this.closeDrawSection();
        this.activeId = undefined;
      }
    },
    closeDrawSection() {
      //Option only for draw section items.
      let el = this.$refs[this.activeId];
      if (el) el[0].$el.click();
    },
    colorChange(color) {
      console.log(color);
    },
    transparencyChange(value) {
      console.log(value);
    }
  },
  mounted() {}
};
</script>
<style lang="css" scoped>
.close {
  position: absolute;
  right: 10px;
  color: white;
}
.expansion-panel__container--active {
  background-color: #4caf50 !important;
  color: white !important;
  font-weight: bold !important;
}
.card {
  font-weight: normal !important;
}
.activeIcon {
  font-size: 20px;
  color: white;
}
</style>