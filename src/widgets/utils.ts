import { Vue } from "vue-property-decorator"

export class SliderConf {
  constructor(
    readonly x: number,
    readonly y: number,
    readonly height: number,
    readonly min: number,
    readonly max: number,
    readonly inverted: number,
    readonly initValue: number,
  ) {}
  
  get initMinValue() {
    if (this.inverted) {
      return -this.initValue;
    } else {
      return this.initValue;
    }
  }

  get ideal() {
    if (this.inverted) {
      return -this.max;
    } else {
      return this.min;
    }
  }

  get nadir() {
    if (this.inverted) {
      return -this.min;
    } else {
      return this.max;
    }
  }
}

export interface PrefLt {
  readonly kind: '<',
}

export interface PrefLte {
  readonly kind: '<=',
  readonly val: number,
}

export interface PrefEq {
  readonly kind: '=',
}

export interface PrefGte {
  readonly kind: '>=',
  readonly val: number,
}

export interface PrefNeq {
  readonly kind: '<>',
}

export const PREF_KINDS = ['<', '<=', '=', '>=', '<>'];
export const MAX_PREF_KINDS = ['>', '>=', '=', '<=', '<>'];

export type DimPref = PrefLt | PrefLte | PrefEq | PrefGte | PrefNeq;

export function numToPref(val: number, conf: SliderConf, snap = true): DimPref {
  let minVal;
  if (conf.inverted) {
    minVal = -val;
  } else {
    minVal = val;
  }
  let { ideal, nadir, initMinValue } = conf;
  let near = (ideal - nadir) / 100;
  if (minVal < ideal || (snap && Math.abs(minVal - ideal) <= near)) {
    return { kind: '<' };
  } else if (minVal > nadir || (snap && Math.abs(minVal - nadir) <= near)) {
    return { kind: '<>' };
  } else if (snap ? Math.abs(minVal - initMinValue) <= near : minVal == initMinValue) {
    return { kind: '=' };
  } else if (minVal < initMinValue) {
    return { kind: '<=', val: minVal };
  } else {
    return { kind: '>=', val: minVal };
  }
}

export function kindToPref(kind: string, conf: SliderConf): DimPref {
  let { ideal, nadir, initMinValue } = conf;
  switch (kind) {
    case "<=":
      if (ideal >= initMinValue) {
        return { kind: "<" };
      } else {
        return {
          kind,
          val: ideal + (initMinValue - ideal) / 2
        };
      }
    case ">=":
      if (nadir <= initMinValue) {
        return { kind: "<>" };
      } else {
        return {
          kind,
          val: nadir - (nadir - initMinValue) / 2
        };
      }
    // Typescript compiler not smart enough to recognise single case...
    case "<":
      return { kind };
    case "<>":
      return { kind };
    case "=":
      return { kind };
    default:
      throw new Error("kindToPref got non-kind input");
  }
}

export function prefToDispNum(pref: DimPref, conf: SliderConf): number | null {
  switch (pref.kind) {
    case "<=":
    case ">=":
      if (conf.inverted) {
        return -pref.val;
      } else {
        return pref.val;
      }
    default:
      return null;
  }
}

export function prefToNum(pref: DimPref, conf: SliderConf): number {
  switch (pref.kind) {
    case "<=":
    case ">=":
      if (conf.inverted) {
        return -pref.val;
      } else { 
        return pref.val;
      }
    case "=":
      return conf.initValue;
    case "<":
      if (conf.inverted) {
        return conf.max;
      } else {
        return conf.min;
      }
    case "<>":
      if (conf.inverted) {
        return conf.min;
      } else {
        return conf.max;
      }
  }
}

// XXX: Broken do not use (yet)
export function* zip(firstArr: any[], ...arrs: any[][]) {
  for (let key of firstArr.keys()) {
    yield [firstArr[key]].concat(arrs.map((arr) => arr[key]));
  }
}

// For easy access from templates
Vue.prototype.zip = zip;
