import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import { VegaModel, VegaView } from './vega';

import NimbusPref from './NimbusPref.vue';

import { SliderConf } from './utils';

export
class NimbusPrefModel extends VegaModel {
  static model_name = 'NimbusPrefModel';
  static view_name = 'NimbusPrefView';
}

export
class NimbusPrefView extends VegaView {
  component: NimbusPref;
  vegaElement = document.createElement('div');

  render() {
    super.render();
    let root = this.view.data('root')[0];
    let rootBounds = root.bounds;
    let confs: SliderConf[] = [];
    let scales = root.context.scales;
    let fieldNames = root.context.data.fields.values.value;
    let values = root.context.data.main.values.value[0];
    let idx = 0;
    for (let axis of root.items) {
      if (axis.role !== 'axis') {
        continue;
      }
      let axisShape = axis.items[0]
      let x = axisShape.x - rootBounds.x1;
      let y = axisShape.y - rootBounds.y1;
      let height = axisShape.range;

      let domain = scales[fieldNames[idx].data].value.domain();
      let value = values[fieldNames[idx].data];
      
      console.log(
        'SliderConf',
        x, y, height, domain[0], domain[1], value
      );
      confs.push(new SliderConf(
        x, y, height, domain[0], domain[1], value
      ));
      idx++;
    }
    this.component = new NimbusPref({
      propsData: {
        confs,
        vegaView: this.view,
        vegaEl: this.vegaEl
      }
    }).$mount();
    this.vegaEl.style.position = 'relative';
    this.el.appendChild(this.component.$el);
  }

  get vegaEl() {
    return this.vegaElement;
  }
}
