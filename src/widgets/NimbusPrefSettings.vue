<template>
  <div>
    <button @click="open = !open" class="btn btn-default">
      <i class="fa-cog fa"></i>
      <span class="toolbar-btn-label">Settings</span>
    </button>
    <ul :class="$style['overlay']" v-show="open">
      <li>
	<label>
	  <input type="checkbox" v-model="curMaxAsMin">
	  <div>
	    Reformulate maximization as minimization
	  </div>
	</label>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Prop,
  Vue,
} from "vue-property-decorator"

@Component({})
export default class NimbusPrefSettings extends Vue {
  @Prop()
  origMaxAsMin: boolean;

  curMaxAsMin: boolean = this.origMaxAsMin;

  open: boolean = false;
}
</script>

<style lang="scss" module>
.overlay {
  position: absolute;
  right: 0;
  width: 256px;
  list-style: none;
  border: 1px solid #ccc;
  color: #333;
  white-space: normal;
  background: white;
  padding: 2px 8px;
  margin-top: -1px;
}

.overlay label {
  display: flex;
  align-items: center;

  > input {
    margin-right: 8px;
  }
}
</style>
