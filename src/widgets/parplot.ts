import {
  DOMWidgetModel, DOMWidgetView, ISerializers, WidgetModel
} from '@jupyter-widgets/base';

import { VegaModel, VegaView } from './vega';

import Parplot from './Parplot.vue';

import { SliderConf } from './utils';

export
class ParplotModel extends VegaModel {
  static model_name = 'ParplotModel';
  static view_name = 'ParplotView';
}

export
class ParplotView extends VegaView {
  component: Parplot;
  vegaElement = document.createElement('div');

  getConfs() {
    let root = this.view.data('root')[0];
    let rootBounds = root.bounds;
    let confs: SliderConf[] = [];
    let scales = root.context.scales;
    let fieldNames = root.context.data.fields.values.value;
    let values = root.context.data.main.values.value[0];
    let idx = 0;
    let maximized = this.model.get('maximized');
    let maxAsMin = this.model.get('cur_max_as_min');
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
      
      let inverted = !maxAsMin && maximized[idx];

      confs.push(new SliderConf(
        x, y, height, domain[0], domain[1], inverted, value
      ));
      idx++;
    }
    return [confs, maximized, maxAsMin];
  }

  render() {
    super.render();
    let [confs, maximized, maxAsMin] = this.getConfs();
    this.component = this.getComponent(confs, maximized, maxAsMin);
    this.addComponentWatchers();
    this.vegaEl.style.position = 'relative';
    this.el.appendChild(this.component.$el);
  }

  getComponent(confs, maximized, maxAsMin) {
    return new Parplot({
      propsData: {
        confs,
        vegaView: this.view,
        vegaEl: this.vegaEl,
        maximized,
        maxAsMin,
      }
    }).$mount();
  }

  addComponentWatchers() {
    this.component.$watch(
      function() {
        return [this['prefs'], this['problem']];
      },
      (newPrefProb, oldPrefProb) =>
        this.onPrefsChange(newPrefProb, oldPrefProb),
      {
        deep: true,
        immediate: true,
      }
    );
    this.component.$watch(
      'curMaxAsMin',
      (newMaxAsMin, oldMaxAsMin) =>
        this.onMaxAsMinChange(newMaxAsMin, oldMaxAsMin)
    );
  }

  onPrefsChange(newPrefProb, oldPrefProb) {
    this.model.set('prefs', newPrefProb[0]);
    this.model.set('prob', newPrefProb[1]);
    this.touch();
  }

  onMaxAsMinChange(newMaxAsMin, oldMaxAsMin) {
    this.model.set('cur_max_as_min', newMaxAsMin);
    this.touch();
  }

  get vegaEl() {
    return this.vegaElement;
  }
}
