<template>
  <div>
    <div :class="$style['inputs']">
      <PrefInput
	:style="{
	  left: confs[idx].x + 'px',
	}"
	:conf="confs[idx]"
	:pref.sync="pref.pref"
	:key="idx"
	v-for="(pref, idx) of preferences" />
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

@Component({
  components: {
    SliderOverlay,
    PrefInput,
  }
})
export default class NimbusPref extends Vue {
  $refs: {
    vega: Element,
    sliders: SliderOverlay[],
  }

  @Prop()
  confs: SliderConf[];

  @Prop()
  vegaView: vega.View;

  @Prop()
  vegaEl: Element;

  preferences: { pref: DimPref }[] = this.initialPreferences();

  initialPreferences(): { pref: DimPref }[] {
    return Array.from(this.confs.map((_conf) => {
      return {
	pref: { 'kind': '=' } as PrefEq
      };
    }));
  }

  mounted() {
    console.log('this.$style', (this as any).$style)
    console.log('this.confs', this.confs);
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
}
</script>

<style lang="scss" module>
.inputs {
  position: relative;
  height: 40px;
  > * {
    position: absolute;
    transform: translateX(-50%);
  }
}
.vega-overlay {
  position: relative;
}
</style>
