import { Vue } from "vue-property-decorator"

export class SliderConf {
  constructor(
    readonly x: number,
    readonly y: number,
    readonly height: number,
    readonly min: number,
    readonly max: number,
    readonly initValue: number,
  ) {}
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

export type DimPref = PrefLt | PrefLte | PrefEq | PrefGte | PrefNeq;

export function numToPref(val: number, conf: SliderConf, snap = true): DimPref {
  let { min, max, initValue } = conf;
  let near = (max - min) / 100;
  console.log('numToCls', near, val, min, max, initValue);
  if (val < min || (snap && Math.abs(val - min) <= near)) {
    return { kind: '<' };
  } else if (val > max || (snap && Math.abs(val - max) <= near)) {
    return { kind: '<>' };
  } else if (snap ? Math.abs(val - initValue) <= near : val == initValue) {
    return { kind: '=' };
  } else if (val < initValue) {
    return { kind: '<=', val };
  } else {
    return { kind: '>=', val };
  }
}

export function kindToPref(kind: string, conf: SliderConf): DimPref {
  let { min, max, initValue } = conf;
  switch (kind) {
    case "<=":
      if (min >= initValue) {
        return { kind: "<" };
      } else {
        return {
          kind,
          val: min + (initValue - min) / 2
        };
      }
    case ">=":
      if (max <= initValue) {
        return { kind: "<>" };
      } else {
        return {
          kind,
          val: max - (max - initValue) / 2
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

export function prefToKnownNum(pref: DimPref): number | null {
  switch (pref.kind) {
    case "<=":
    case ">=":
      return pref.val;
    default:
      return null;
  }
}

export function prefToNum(pref: DimPref, conf: SliderConf): number {
  switch (pref.kind) {
    case "<=":
    case ">=":
      return pref.val;
    case "=":
      return conf.initValue;
    case "<":
      return conf.min;
    case "<>":
      return conf.max;
  }
}

// XXX: Broken do not use (yet)
export function* zip(firstArr: any[], ...arrs: any[][]) {
  for (let key of firstArr.keys()) {
    console.log('zip', key);
    yield [firstArr[key]].concat(arrs.map((arr) => arr[key]));
  }
}

// For easy access from templates
Vue.prototype.zip = zip;
