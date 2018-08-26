<template>
  <div :class="$style['pref-container']">
    <div>
      <div :class="[$style['annotation'], $style['inputs']]">
	<PrefInput
	  :style="{
	    left: confs[idx].x + 'px',
	  }"
	  :conf="confs[idx]"
	  :pref.sync="pref.pref"
	  :key="idx"
	  v-for="(pref, idx) of preferences" />
      </div>
      <MaxAsMinPanel
	:confs="confs"
	:maximized="maximized"
	:maxAsMin="maxAsMin"
	:class="[$style['annotation'], $style['max-min']]" />
      <div :class="$style['vega-overlay']">
	<div ref="vega"></div>
	<SliderOverlay
	  ref="sliders"
	  :conf="confs[idx]"
	  :pref.sync="pref.pref"
	  :key="idx"
	  v-for="(pref, idx) in preferences" />
      </div>
    </div>
    <div :class="$style['side-panel']">
      <div :class="$style['more-buttons']">
	<a class="btn btn-default"
	   target="_blank"
	   href="https://desdeo.readthedocs.io/en/latest/background/classification-in-nimbus.html">
	  <i class="fa-question-circle fa"></i>
	  <span class="toolbar-btn-label">Help</span>
	</a>
	<NimbusPrefSettings :origMaxAsMin="maxAsMin" ref="settings"></NimbusPrefSettings>
      </div>
      <div v-if="problem" class="alert alert-warning" :class="$style['warning']">
	Current preference is invalid because {{ problem }}.
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { VueConstructor } from 'vue';
import { Component, Prop } from "vue-property-decorator"
import { mixins } from 'vue-class-component'

import * as vega from 'vega';
import { SliderConf, DimPref, PrefEq, numToPref } from './utils';
import SliderOverlay from './SliderOverlay.vue';
import PrefInput from './PrefInput.vue';
import NimbusPrefSettings from './NimbusPrefSettings.vue';
import MaxAsMinPanel from './MaxAsMinPanel.vue';
import VegaMixin from './VegaMixin';

@Component({
  components: {
    SliderOverlay,
    PrefInput,
    NimbusPrefSettings,
    MaxAsMinPanel,
  }
})
export default class NimbusPref extends mixins(VegaMixin) {
  $refs: {
    vega: Element,
    settings: NimbusPrefSettings,
    sliders: SliderOverlay[],
  }

  @Prop({ default: null, type: Array })
  initPreferences: DimPref[] | null;

  preferences: { pref: DimPref }[] = this.initialPreferences();

  initialPreferences(): { pref: DimPref }[] {
    if (this.initPreferences) {
      return Array.from(this.initPreferences.map((pref) => {
	return {
	  pref
	};
      }));
    } else {
      return Array.from(this.confs.map((_conf) => {
	return {
	  pref: { 'kind': '=' } as PrefEq
	};
      }));
    }
  }

  mounted() {
    this.vegaInit();
  }

  get problem(): string | null {
    let hasImprove = false;
    let hasDegrade = false;
    for (let pref of this.preferences) {
      if (['<', '<='].includes(pref.pref['kind'])) {
	hasImprove = true;
      } else if (['>', '>='].includes(pref.pref['kind'])) {
	hasDegrade = true;
      }
    }
    if (!hasImprove && !hasDegrade) {
      return "preference must improve and degrade some criteria";
    } else if (!hasImprove) {
      return "preference must improve some criteria";
    } else if (!hasDegrade) {
      return "preference must degrade some criteria";
    }
    return null;
  }

  get prefs(): DimPref[] {
    return this.preferences.map((pref) => {
      return pref.pref;
    });
  }
}
</script>

<style lang="scss" module>
@import "./parplot.scss";

.inputs {
  height: 32px;
}

.warning {
  max-width: 320px;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}
</style>
