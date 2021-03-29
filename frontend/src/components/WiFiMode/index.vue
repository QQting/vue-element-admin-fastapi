<template>
  <div>
    <el-dialog title="Access Point Mode Setting" :visible.sync="dialogFormVisible" @close="closeDialog">
      <el-form ref="dataForm" :model="wifi_set" label-position="left" label-width="90px" style="width: 400px; margin-left:50px; margin-top:20px">
        <el-form-item label="SSID">
          <el-input v-model="wifi_set.ssid" />
        </el-form-item>
        <el-form-item label="Password">
          <el-input v-model="wifi_set.pwd" show-password />
        </el-form-item>
      </el-form>

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
    wifi_set: Object
  },
  data() {
    return {
      dialogFormVisible: this.dialogShow
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
    }
  }
}
</script>
