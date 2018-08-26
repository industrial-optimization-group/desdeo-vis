import {
  Component,
  Prop,
  Vue,
} from "vue-property-decorator"
import * as vega from 'vega';
import { SliderConf } from './utils';
import NimbusPrefSettings from './NimbusPrefSettings.vue';

@Component
export default class VegaMixin extends Vue {
  $refs: {
    vega: Element,
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

  vegaInit() {
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

  get curMaxAsMin(): boolean {
    return this.$refs.settings['curMaxAsMin'];
  }
}
