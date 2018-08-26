<template>
  <div :class="$style['pref-container']">
    <div>
      <MaxAsMinPanel
	:confs="confs"
	:maximized="maximized"
	:maxAsMin="maxAsMin"
	:class="[$style['annotation'], $style['max-min']]" />
      <div :class="$style['vega-overlay']">
	<div ref="vega"></div>
      </div>
    </div>
    <div :class="$style['side-panel']">
      <div :class="$style['more-buttons']">
	<NimbusPrefSettings :origMaxAsMin="maxAsMin" ref="settings"></NimbusPrefSettings>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { VueConstructor } from 'vue';
import { Component, Prop } from "vue-property-decorator"
import { mixins } from 'vue-class-component'

import NimbusPrefSettings from './NimbusPrefSettings.vue';
import MaxAsMinPanel from './MaxAsMinPanel.vue';
import VegaMixin from './VegaMixin';

@Component({
  components: {
    NimbusPrefSettings,
    MaxAsMinPanel,
  }
})
export default class Parplot extends mixins(VegaMixin) {
  mounted() {
    this.vegaInit();
  }
}
</script>

<style lang="scss" module>
@import "./parplot.scss";
</style>
