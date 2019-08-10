<template>
  <v-layout>
    <v-flex xs12 class="mx-3">
      <template v-for="calculation in calculations">
        <v-card class="mb-3 " :key="calculation.id">
          <!-- Isochrone Nr -->
          <div class="isochrone-nr">{{ calculation.id }}</div>
          <v-card-title class="pb-0 mb-0">
            <v-layout row wrap align-center>
              <v-flex xs6>
                <v-card-text class="pa-0 ma-0 ml-3">
                  <v-icon small class="mr-1 text-xs-center"
                    >fas fa-clock</v-icon
                  >
                  <span class="subtitle-2 text-xs-center">{{
                    calculation.time
                  }}</span>
                  <v-icon small class="ml-2 mr-1 "
                    >fas fa-tachometer-alt</v-icon
                  >
                  <span class="subtitle-2 text-xs-center">{{
                    calculation.speed
                  }}</span>
                </v-card-text>
              </v-flex>
              <v-flex xs6>
                <v-card-text class="pa-0 ma-0">
                  <v-icon
                    @click="showPoisTable(calculation)"
                    small
                    class="result-icons ml-7 mr-2"
                    >fas fa-table</v-icon
                  >
                  <v-icon small class="result-icons mr-2"
                    >fas fa-pencil-alt</v-icon
                  >
                  <v-icon
                    @click="showHideCalculation(calculation)"
                    small
                    class="result-icons mr-2"
                    v-html="
                      calculation.isVisible ? 'fas fa-eye-slash' : 'fas fa-eye'
                    "
                  ></v-icon>
                  <v-icon
                    @click="toggleDownloadDialog(calculation)"
                    small
                    class="result-icons mr-2"
                    >fas fa-download</v-icon
                  >
                  <v-icon
                    @click="deleteCalculation(calculation)"
                    small
                    class="result-icons mr-1"
                  >
                    fas fa-trash-alt</v-icon
                  >
                </v-card-text>
              </v-flex>
            </v-layout>
            <v-card-text class="pr-0 pl-0 pt-0 pb-0">
              <v-divider></v-divider>
            </v-card-text>
          </v-card-title>
          <v-subheader
            class="clickable"
            @click="calculation.isExpanded = !calculation.isExpanded"
          >
            <v-icon
              small
              class="mr-2"
              v-html="
                calculation.isExpanded
                  ? 'fas fa-chevron-down'
                  : 'fas fa-chevron-right'
              "
            ></v-icon>
            <h3>{{ calculation.position }}</h3>
          </v-subheader>
          <v-card-text class="pt-0 " v-show="calculation.isExpanded">
            <v-data-table
              :headers="headers"
              :items="calculation.data"
              class="elevation-1 subtitle-1"
              hide-default-footer
              light
            >
              <template v-slot:items="props">
                <td>{{ props.item.type }}</td>
                <td>{{ props.item.range }}</td>
                <td>{{ props.item.area }}</td>
              </template>
              <template v-slot:item.visible="{ item }">
                <v-switch
                  :input-value="item.isVisible"
                  primary
                  hide-details
                  @change="toggleIsochroneFeatureVisibility(item)"
                ></v-switch>
              </template>
              <template v-slot:item.legend="{ item }">
                <div
                  class="legend"
                  :style="{ backgroundColor: item.color }"
                ></div>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </template>
    </v-flex>
    <confirm ref="confirm"></confirm>
    <download
      :visible="showDialog"
      :calculation="selectedCalculation"
      @close="showDialog = false"
    ></download>
  </v-layout>
</template>
<script>
import { mapGetters, mapActions, mapMutations } from "vuex";
import Confirm from "../core/Confirm";
import Download from "./IsochronesDownload";
import IsochroneUtils from "../../utils/IsochroneUtils";

export default {
  components: {
    confirm: Confirm,
    download: Download
  },
  data() {
    return {
      headers: [
        { text: "Type", value: "type", sortable: false },
        { text: "Range", value: "range", sortable: false },
        { text: "Area", value: "area", sortable: false },
        { text: "Visible", value: "visible", sortable: false },
        { text: "Legend", value: "legend", sortable: false }
      ],
      showDialog: false,
      selectedCalculation: null
    };
  },

  methods: {
    ...mapActions("isochrones", {
      removeCalculation: "removeCalculation",
      setSelectedThematicData: "setSelectedThematicData"
    }),
    ...mapMutations("isochrones", {
      toggleIsochroneFeatureVisibility: "TOGGLE_ISOCHRONE_FEATURE_VISIBILITY",
      toggleIsochroneCalculationVisibility:
        "TOGGLE_ISOCHRONE_CALCULATION_VISIBILITY",
      toggleThematicDataVisibility: "TOGGLE_THEMATIC_DATA_VISIBILITY"
    }),
    deleteCalculation(calculation) {
      this.$refs.confirm
        .open(
          "Delete",
          "Are you sure you want to delete Calculation " +
            calculation.id +
            " ?",
          { color: "green" }
        )
        .then(confirm => {
          if (confirm) {
            this.removeCalculation(calculation);
          }
        });
    },
    toggleDownloadDialog(calculation) {
      this.showDialog = true;
      this.selectedCalculation = calculation;
    },
    showHideCalculation(calculation) {
      let me = this;
      me.toggleIsochroneCalculationVisibility(calculation);
    },
    showPoisTable(calculation) {
      let me = this;
      let features = IsochroneUtils.getCalculationFeatures(
        calculation,
        me.isochroneLayer
      );

      let calculationId = calculation.id;
      let calculationName = calculation.name;
      let pois = IsochroneUtils.getCalculationPoisObject(features);

      let payload = {
        calculationId: calculationId,
        calculationName: calculationName,
        pois: pois
      };

      me.setSelectedThematicData(payload);
      me.toggleThematicDataVisibility(true);
    }
  },
  computed: {
    ...mapGetters("isochrones", {
      calculations: "calculations",
      isochroneLayer: "isochroneLayer"
    })
  }
};
</script>
<style lang="css">
.result-icons {
  color: "#4A4A4A";
}
.result-icons:hover {
  cursor: pointer;
  color: #30c2ff;
}
.isochrone-nr {
  position: absolute;
  left: 6px;
}
.v-data-table td,
.v-data-table th {
  padding: 0 5px;
}
.v-data-table th {
  font-size: 14px;
}
.v-data-table td {
  font-size: 13px;
}
.legend {
  height: 24px;
  width: 24px;
  border-radius: 7px;
}

.activeIcon {
  color: #30c2ff;
}
.v-input--selection-controls {
  margin-top: 0px;
  padding-top: 0px;
}
</style>