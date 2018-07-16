import {
  DOMWidgetModel, DOMWidgetView, ISerializers, WidgetModel
} from '@jupyter-widgets/base';

import * as Backbone from 'backbone';

import {
  EXTENSION_SPEC_VERSION
} from '../version';

import * as vega from 'vega';

export
class VegaModel extends DOMWidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: VegaModel.model_name,
      _model_module: VegaModel.model_module,
      _model_module_version: VegaModel.model_module_version,
      _view_name: VegaModel.view_name,
      _view_module: VegaModel.view_module,
      _view_module_version: VegaModel.view_module_version,
    };
  }

  static serializers: ISerializers = {
      ...DOMWidgetModel.serializers,
      // Add any extra serializers here
    }

  static model_name = 'VegaModel';
  static model_module = 'desdeo_vis';
  static model_module_version = EXTENSION_SPEC_VERSION;
  static view_name = 'VegaView';  // Set to null if no view
  static view_module = 'desdeo_vis';   // Set to null if no view
  static view_module_version = EXTENSION_SPEC_VERSION;
}


export
class VegaView extends DOMWidgetView {
  spec: any;
  view: any;

  constructor(options?: Backbone.ViewOptions<WidgetModel> & {options?: any}) {
    super(options);
    this.model.on('change:spec', () => {
      while (this.el.firstChild) {
        this.el.removeChild(this.el.firstChild);
      }
      this.render();
    });
  }

  render() {
    this.spec = this.model.get('spec');
    this.view = new vega.View(vega.parse(this.spec))
            .renderer('canvas');
    this.mountView();
  }

  mountView() {
    this.view.initialize(this.vegaEl)
             .hover()
             .run();
  }

  get vegaEl() {
    return this.el;
  }
}
