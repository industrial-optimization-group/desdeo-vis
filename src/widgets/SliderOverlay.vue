<template>
  <input
    :class="$style['slider']"
    type="range"
    :min="conf.min"
    :max="conf.max"
    :step="step"
    :style="style"
    :value="value"
    @input="valueChange" />
</template>

<script lang="ts">
import {
  Component,
  Prop,
  Vue
} from "vue-property-decorator"

import { SliderConf, numToPref, DimPref, prefToNum } from './utils';

let thumb_w = 2;

@Component({})
export default class SliderOverlay extends Vue {
  @Prop()
  conf: SliderConf;

  @Prop()
  pref: DimPref;

  get value(): number {
    return prefToNum(this.pref, this.conf);
  }

  get step() {
    return ((this.conf.max - this.conf.min) / 1000).toPrecision(4);
  }

  get style() {
    let fullRange = this.conf.height + thumb_w;
    return {
      left: this.conf.x + 'px',
      top: this.conf.y - (thumb_w / 2) + 'px',
      width: fullRange + 1 + 'px',
      // frig factor * rotation origin compensation * rotation
      transform: 'translate(-3px, 5px) '
	+ `translateX(${-fullRange}px)`
	+ 'rotate(270deg)'
    };
  }

  valueChange(input) {
    this.updatePref(numToPref(input.target.value, this.conf));
  }

  updatePref(pref: DimPref) {
    this.$emit('update:pref', pref);
  }
}
</script>

<style lang="scss" module>
/*
For a full exploration of styling input[range] see:
https://css-tricks.com/sliding-nightmare-understanding-range-input/
*/
$track-w: 200px;
$track-h: 4px;
$thumb-h: 16px;
$thumb-w: 2px;

.slider {
  transform-origin: top right;
  position: absolute;
  cursor: pointer;
}

@mixin track() {
  box-sizing: border-box;
  border: none;
  width: $track-w;
  height: $track-h;
  background: rgba(0, 0, 0, 0.0);
}

@mixin thumb() {
  box-sizing: border-box;
  border: none;
  width: $thumb-w;
  height: $thumb-h;
  border-radius: 0;
  background: blue;
}

[type='range'] {
  &, &::-webkit-slider-thumb {
	  -webkit-appearance: none;
  }
  
  /*position: absolute;
  top: 50%; left: 50%;*/
  margin: 0;
  padding: 0;
  width: $track-w; height: $thumb-h;
  /*transform: translate(-50%, -50%) 
	  rotate(-90deg);*/
  background: transparent;
  font: 1em/1 arial, sans-serif;
  
  &::-webkit-slider-runnable-track {
      @include track
  }
  &::-moz-range-track {
    @include track
  }
  &::-ms-track {
    @include track
  }
  
  &::-webkit-slider-thumb {
    margin-top: .5*($track-h - $thumb-h);
    @include thumb
  }
  &::-moz-range-thumb {
    @include thumb
  }
  &::-ms-thumb {
    margin-top: 0;
    @include thumb
  }
  
  &::-ms-tooltip {
    display: none
  }
}
</style>
