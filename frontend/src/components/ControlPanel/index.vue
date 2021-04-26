<template>
  <div>
    <el-dialog title="Control Panel" :visible.sync="dialogFormVisible" @close="closeDialog">
      <el-form ref="dataForm" :model="config" label-position="left" label-width="90px" style="width: 400px; margin-left:50px;">
        <el-form-item label="Hostname">
          <el-input v-model="config.Hostname" :disabled="true" />
        </el-form-item>
        <el-form-item label="Robot ID">
          <el-input v-model="config.DeviceID" :disabled="true" />
        </el-form-item>
      </el-form>

      <el-row>
        <el-select v-model="value" placeholder="Select" style="margin-left:50px;">
          <el-option
            v-for="item in options"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>
        <el-button type="primary" style="width: 100px" @click="setled()">
          Set LED
        </el-button>
      </el-row>

      <el-row>
        <el-button style="width: 100px; margin-left:50px; margin-top:20px" @click="todo()">
          Locate
        </el-button>
      </el-row>
      <el-tooltip effect="dark" content="WARN!! Reboot ROScube">
        <el-button type="danger" style="width: 100px; margin-left:50px; margin-top:20px" @click="Reboot()">
          Reboot
        </el-button>
      </el-tooltip>

      <div slot="footer" class="dialog-footer">
        <el-button @click="closeDialog">
          Done
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>

export default {
  props: {
    dialogShow: {
      type: Boolean,
      default: false
    },
    config: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      dialogFormVisible: this.dialogShow,
      options: ['Green', 'Red', 'Yellow'],
      value: 'Yellow'
    }
  },
  watch: {
    dialogShow(val) {
      this.dialogFormVisible = val
    }
  },
  methods: {
    closeDialog() {
      this.$emit('dialogShowChange', false)
    },
    Reboot() {
      this.$message({
        message: 'ROScube start reboot',
        type: 'warning'
      })
    },
    setled() {
      this.$message({
        message: 'LED color set',
        type: 'success'
      })
    }
  }
}
</script>
