<template>
  <div :class="$style['pref-input']">
    <select class="btn-xs select-xs" :value="pref.kind" @input="kindChange">
      <option v-for="kind of PREF_KINDS" :value="kind">{{ kind }}</option>
    </select>
    <input class="btn-xs" :disabled="!hasValue" :value="value" @change="valueChange" />
  </div>
</template>

<script lang="ts">
import {
  Component,
  Model,
  Emit,
  Prop,
  Watch,
  Vue
} from "vue-property-decorator"

import {
  PREF_KINDS,
  DimPref,
  SliderConf,
  numToPref,
  prefToKnownNum,
  kindToPref,
} from './utils';

@Component({})
export default class PrefInput extends Vue {
  @Prop()
  conf: SliderConf;

  @Prop()
  pref: DimPref;

  readonly PREF_KINDS = PREF_KINDS;

  kindChange(input) {
    let kind = input.target.value;
    this.updatePref(kindToPref(kind, this.conf));
  }

  valueChange(input) {
    this.updatePref(numToPref(parseFloat(input.target.value), this.conf, false));
  }

  @Watch('pref')
  onPrefChange(pref) {
    console.log('onPrefChange', pref);
  }

  updatePref(pref: DimPref) {
    this.$emit('update:pref', pref);
  }

  get hasValue(): boolean {
    return ["<=", ">="].includes(this.pref.kind);
  }

  get value(): number | null {
    return prefToKnownNum(this.pref);
  }
}
</script>

<style lang="scss" module>
.pref-input {
  > select {
    padding-left: 0;
    padding-right: 0;
  }
  > input {
    width: 64px;
  }
}
</style>
