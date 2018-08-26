import {
  DOMWidgetModel, DOMWidgetView, ISerializers, WidgetModel
} from '@jupyter-widgets/base';

import { ParplotModel, ParplotView } from './parplot';

import NimbusPref from './NimbusPref.vue';

import { SliderConf } from './utils';

export
class NimbusPrefModel extends ParplotModel {
  static model_name = 'NimbusPrefModel';
  static view_name = 'NimbusPrefView';
}

export
class NimbusPrefView extends ParplotView {
  component: NimbusPref;

  getComponent(confs, maximized, maxAsMin) {
    let initPreferences;
    if (this.model.get('prefs').length) {
      initPreferences = this.model.get('prefs');
    } else {
      initPreferences = null;
    }
    return new NimbusPref({
      propsData: {
        confs,
        vegaView: this.view,
        vegaEl: this.vegaEl,
        maximized,
        maxAsMin,
        initPreferences,
      }
    }).$mount();
  }
}
