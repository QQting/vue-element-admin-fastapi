<template>
  <div class="app-container">

    <div class="filter-container">
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="getList()">
        Search
      </el-button>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload()">
        Export
      </el-button>
      <upload-excel-component class="filter-item" style="margin-left:9px; margin-right:9px;" :on-success="handleSuccess" :before-upload="beforeUpload" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-location-outline" @click="dialogShowWifi(true)">
        WiFi mode
      </el-button>
    </div>

    <el-table
      ref="multipleTable"
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      stripe
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" align="center" />
      <el-table-column label="Index" prop="Index" sortable align="center" width="80" :class-name="getSortClass('Index')">
        <template #default="{row}">
          <span>{{ row.Index }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Device ID" width="110px" align="center">
        <template #default="{row}">
          <span>{{ row.DeviceID }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Hostname" width="110px" align="center">
        <template #default="{row}">
          <span>{{ row.Hostname }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Model" width="110px" align="center">
        <template #default="{row}">
          <span>{{ row.Model }}</span>
        </template>
      </el-table-column>
      <el-table-column label="IP adress" width="110px" align="center">
        <template #default="{row}">
          <span>{{ row.IP }}</span>
        </template>
      </el-table-column>
      <el-table-column label="MAC address" width="150px" align="center">
        <template #default="{row}">
          <span>{{ row.MAC }}</span>
        </template>
      </el-table-column>
      <el-table-column label="RMT version" width="110px" align="center">
        <template #default="{row}">
          <span>{{ row.RMT_VERSION }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" width="230" class-name="small-padding fixed-width">
        <template #default="{row}">
          <el-button v-waves type="info" size="mini" @click="handleUpdate(row)">
            Edit
          </el-button>
          <el-button v-waves type="primary" size="mini" @click="handlecontrol(row)">
            Control
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog title="Export Excel" :visible.sync="downloadLoading">
      <el-form ref="dataForm" :rules="rules" label-position="left" label-width="80px" style="width: 400px; margin-left:50px;">
        <el-form-item label="File name">
          <el-input v-model="filename" />
        </el-form-item>
      </el-form>
      <template>
        <el-checkbox v-model="checkAll" :indeterminate="isIndeterminate" @change="handleCheckAllChange">Check all</el-checkbox>
        <div style="margin: 15px 0;" />
        <el-checkbox-group v-model="checkedParams" @change="handleCheckedParamChange">
          <el-checkbox v-for="param in ParamOption" :key="param" :label="param">{{ param }}</el-checkbox>
        </el-checkbox-group>
      </template>
      <div slot="footer" class="dialog-footer">
        <el-button v-waves @click="downloadLoading = false">
          Cancel
        </el-button>
        <el-button v-waves type="primary" @click="handleConfirm">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-tabs>
        <el-tab-pane label="Config" name="Config">Robot Parameters
          <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px; margin-top:20px">
            <el-form-item label="Network">
              <el-input v-model="temp.Network" />
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="WiFi" name="WiFi">WiFi Setting
          <el-form ref="dataForm" :model="wifi_client" label-position="left" label-width="90px" style="width: 400px; margin-left:50px; margin-top:20px">
            <el-form-item label="SSID">
              <el-input v-model="wifi_client.ssid" />
            </el-form-item>
            <el-form-item label="Password">
              <el-input v-model="wifi_client.password" show-password />
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      <div slot="footer" class="dialog-footer">
        <el-button v-waves @click="dialogFormVisible = false">
          Cancel
        </el-button>
        <el-button v-waves type="primary" @click="dialogStatus==='create'?createData():updateData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>
    <control-component :dialog-show="panel_on_control" :config="temp" @dialogShowChange="dialogShowControl" />
    <wifi-mode-component :dialog-show="panel_on_wifi" :wifi-set="temp_wifi" @dialogShowChange="dialogShowWifi" @syncData="syncData" />
  </div>
</template>

<script>
import { fetchRobotList, updateRobots, fetchWifi } from '@/api/robots'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import UploadExcelComponent from '@/components/UploadExcel/index_robot.vue'
import ControlComponent from '@/components/ControlPanel/index.vue'
import WifiModeComponent from '@/components/WiFiMode/index.vue'

export default {
  name: 'ComplexTable',
  components: { Pagination, UploadExcelComponent, ControlComponent, WifiModeComponent },
  directives: { waves },
  filters: {
    // statusFilter(status) {
    //   const statusMap = {
    //     Active: 'success',
    //     Inactive: 'danger'
    //   }
    //   return statusMap[status]
    // },
    // batteryFilter(battery) {
    //   var tag_val = 'success'
    //   if (battery < 10) {
    //     tag_val = 'danger'
    //   } else if (battery < 20) {
    //     tag_val = 'warning'
    //   }
    //   return tag_val
    // }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      multipleSelection: [],
      downloadLoading: false,
      checkAll: false,
      filename: '',
      ParamOption: [],
      checkedParams: [],
      isIndeterminate: true,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        sort: '+Index'
      },
      wifi_set: {
        ssid: '',
        password: '',
        band: '2.4 GHz',
        mode_on: false
      },
      wifi_client: {
        ssid: '',
        password: ''
      },
      temp_wifi: {},
      sortOptions: [{ label: 'Index Ascending', key: '+Index' }, { label: 'Index Descending', key: '-Index' }],
      temp: {
        index: undefined
      },
      dialogFormVisible: false,
      panel_on_control: false,
      panel_on_wifi: false,
      dialogStatus: '',
      percentage: 0,
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      rules: {
        // type: [{ required: true, message: 'type is required', trigger: 'change' }],
        // timestamp: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        // title: [{ required: true, message: 'title is required', trigger: 'blur' }]
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchRobotList(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
      fetchWifi().then(response => {
        this.wifi_set = response.data
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'Index') {
        this.sortByIndex(order)
      }
    },
    sortByIndex(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+Index'
        this.handleFilter()
      } else if (order === 'descending') {
        this.listQuery.sort = '-Index'
        this.handleFilter()
      } else {
        // order === 'null', do nothing
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    handleCheckAllChange(val) {
      this.checkedParams = val ? this.ParamOption : []
      this.isIndeterminate = false
    },
    handleCheckedParamChange(value) {
      const checkedCount = value.length
      this.checkAll = checkedCount === this.ParamOption.length
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.ParamOption.length
    },
    handleDownload() {
      if (this.multipleSelection.length) {
        this.ParamOption = Object.keys(this.list[0])
        this.downloadLoading = true
      } else {
        this.$message({
          message: 'Please select at least one item',
          type: 'warning'
        })
      }
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => v[j]))
    },
    handleConfirm() {
      import('@/vendor/Export2Excel').then(excel => {
        const filterVal = this.checkedParams
        const tHeader = filterVal
        const list = this.multipleSelection
        const data = this.formatJson(filterVal, list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: this.filename
        })
        this.$refs.multipleTable.clearSelection()
        this.downloadLoading = false
      })
    },

    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handlecontrol(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.panel_on_control = true
    },
    dialogShowControl(val) {
      this.panel_on_control = val
    },
    dialogShowWifi(val) {
      if (val) { this.temp_wifi = Object.assign({}, this.wifi_set) }
      this.panel_on_wifi = val
    },
    syncData() {
      this.wifi_set = Object.assign({}, this.temp_wifi)
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          updateRobots(tempData).then(() => {
            const index = this.list.findIndex(v => v.index === this.temp.index)
            this.list.splice(index, 1, this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Update Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    },
    percentageColorMethod(percentage) {
      if (percentage < 70) {
        return '#909399'
      } else if (percentage < 90) {
        return '#e6a23c'
      } else {
        return '#f56c6c'
      }
    },
    beforeUpload(file) {
      const isLt1M = file.size / 1024 / 1024 < 1
      if (isLt1M) {
        return true
      }

      this.$message({
        message: 'Please do not upload files larger than 1m in size.',
        type: 'warning'
      })

      return false
    },
    handleSuccess({ results, header }) {
      for (var index in results) {
        if (parseInt(index + 1, 10) > this.list.length) {
          this.list.push(results[index])
          continue
        }
        for (var param in results[index]) {
          this.list[index][param] = results[index][param]
        }
      }
    }
  }
}
</script>

