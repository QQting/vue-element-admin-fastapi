<template>
  <div>
    <el-dialog title="Access Point Mode Setting" :visible.sync="dialogFormVisible" @close="closeDialog">
      <el-form ref="dataForm" :model="wifi_set" label-position="left" label-width="125px" style="width: 400px; margin-left:50px; margin-top:20px">
        <el-switch
          v-model="wifi_set.mode_on"
          active-text="ON"
          inactive-text="OFF"
        />
        <el-form-item label="Frequency Band" style="margin-top:20px">
          <el-select v-model="wifi_set.band" placeholder="Select" style="margin-left:50px">
            <el-option
              v-for="item in band_list"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="SSID">
          <el-input v-model="wifi_set.ssid" />
        </el-form-item>
        <el-form-item label="Password">
          <el-input v-model="wifi_set.password" show-password minlength="8" />
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="closeDialog">
          Cancel
        </el-button>
        <el-button :disabled="button_block" @click="handleUpdate">
          Done
        </el-button>
      </div>
    </el-dialog>
  </div>

</template>

<script>
import { updateWifi } from '@/api/robots'

export default {
  props: {
    dialogShow: {
      type: Boolean,
      default: false
    },
    wifiSet: Object
  },
  data() {
    return {
      dialogFormVisible: this.dialogShow,
      band_list: ['2.4 GHz', '5 GHz']
    }
  },
  computed: {
    button_block() {
      return this.wifi_set.password ? this.wifi_set.password.length < 8 : true
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
    async handleUpdate() {
      await updateWifi(this.wifi_set)
      this.$emit('dialogShowChange', false)
      this.$emit('syncData')
      this.$notify({
        title: 'Success',
        message: 'Update Successfully',
        type: 'success',
        duration: 2000
      })
    }
  }
}
</script>
