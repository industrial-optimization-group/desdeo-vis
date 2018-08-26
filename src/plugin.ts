// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import {
  Application, IPlugin
} from '@phosphor/application';

import {
  Widget
} from '@phosphor/widgets';

import {
  IJupyterWidgetRegistry
 } from '@jupyter-widgets/base';

import {
  VegaModel, VegaView
} from './widgets/vega';

import {
  ParplotModel, ParplotView
} from './widgets/parplot';

import {
  NimbusPrefModel, NimbusPrefView
} from './widgets/nimbus-pref';

import {
  EXTENSION_SPEC_VERSION
} from './version';

const EXTENSION_ID = 'jupyter.extensions.example';


/**
 * The example plugin.
 */
const examplePlugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  activate: activateWidgetExtension,
  autoStart: true
};

export default examplePlugin;


/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app: Application<Widget>, registry: IJupyterWidgetRegistry): void {
  registry.registerWidget({
    name: 'desdeo_vis',
    version: EXTENSION_SPEC_VERSION,
    exports: {
      VegaModel,
      VegaView,
      ParplotModel,
      ParplotView,
      NimbusPrefModel,
      NimbusPrefView,
    }
  });
}
