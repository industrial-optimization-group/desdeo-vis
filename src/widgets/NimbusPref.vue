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
      <div :style="{opacity: maxAsMin ? 0 : 1}" :class="[$style['annotation'], $style['max-min']]">
	<div
	  :style="{
	    left: confs[idx].x + 'px',
	    }"
	  v-for="(mx_mn, idx) of maximized">
	  <i v-if="mx_mn" class="fa fa-angle-up"></i>
	  <i v-else class="fa fa-angle-down"></i>
	</div>
      </div>
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
import {
  Component,
  Prop,
  Vue
} from "vue-property-decorator"

import * as vega from 'vega';
import { SliderConf, DimPref, PrefEq, numToPref } from './utils';
import SliderOverlay from './SliderOverlay.vue';
import PrefInput from './PrefInput.vue';
import NimbusPrefSettings from './NimbusPrefSettings.vue';

@Component({
  components: {
    SliderOverlay,
    PrefInput,
    NimbusPrefSettings,
  }
})
export default class NimbusPref extends Vue {
  $refs: {
    vega: Element,
    sliders: SliderOverlay[],
    settings: NimbusPrefSettings,
  }

  @Prop()
  confs: SliderConf[];

  @Prop()
  vegaView: vega.View;

  @Prop()
  vegaEl: Element;

  @Prop()
  maximized: boolean[];

  @Prop()
  maxAsMin: boolean;

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
    this.vegaView.initialize(this.$refs.vega)
                 .hover()
                 .run();
    /*
      Perhaps this would be better than reinitialising, but this.$refs.vega is
      undefined.

      this.$refs.vega.appendChild(this.vegaEl);
    */

    //this.$watch('sliderValues', this.valuesChange);
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

  get curMaxAsMin(): boolean {
    return this.$refs.settings['curMaxAsMin'];
  }
}
</script>

<style lang="scss" module>
.inputs {
  height: 32px;
}

.max-min {
  height: 16px;
  font-size: 24px;
  margin-top: -8px;
  margin-bottom: 4px;
}

.annotation {
  position: relative;
  > * {
    position: absolute;
    transform: translateX(-50%);
    white-space: nowrap;
  }
}

.pref-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-left: 20px;
}

.vega-overlay {
  position: relative;
}

.side-panel {
  align-self: stretch;
  width: 320px;
}

.more-buttons {
  position: relative;
  margin-left: 20px;
  white-space: nowrap;
  > * {
    float: right;
  }

  > *:last-child {
    margin-right: 10px;
  }
}

.warning {
  max-width: 320px;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}
</style>
