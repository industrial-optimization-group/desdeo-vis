<template>
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
</template>

<script lang="ts">
import {
  Component,
  Prop,
  Vue
} from "vue-property-decorator"

import { SliderConf } from './utils';

@Component({})
export default class MaxAsMinPanel extends Vue {
  @Prop()
  confs: SliderConf[];

  @Prop()
  maximized: boolean[];

  @Prop()
  maxAsMin: boolean;
}
</script>

<style lang="scss" module>
@import "./parplot.scss";
</style>
