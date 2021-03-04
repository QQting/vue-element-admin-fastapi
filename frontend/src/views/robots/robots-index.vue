<template>
  <div class="app-container">

    <div class="filter-container">
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="todo()">
        Search
      </el-button>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload()">
        Export
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      stripe
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="80" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Status" class-name="status-col" width="100" align="center">
        <template slot-scope="{row}">
          <el-tag :type="row.status | statusFilter">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Hostname" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.hostname }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Battery" width="110px" align="center">
        <template slot-scope="{row}">
          <el-tag :type="row.battery | batteryFilter">
            {{ row.battery }}%
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="WiFi Settings" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.wifi }}</span>
        </template>
      </el-table-column>
      <el-table-column label="CPU" width="110px" align="center">
        <template slot-scope="{row}">
          <el-progress :percentage="row.cpu" :color="percentageColorMethod" />
        </template>
      </el-table-column>
      <el-table-column label="Memory" width="110px" align="center">
        <template slot-scope="{row}">
          <el-progress :percentage="row.memory" :color="percentageColorMethod" />
        </template>
      </el-table-column>
      <el-table-column label="Storage" width="110px" align="center">
        <template slot-scope="{row}">
          <el-progress :percentage="row.storage" :color="percentageColorMethod" />
        </template>
      </el-table-column>
      <el-table-column label="Time Zone" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.timezone }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button v-waves type="primary" size="mini" @click="handleUpdate(row)">
            Edit
          </el-button>
          <el-button v-waves type="" size="mini" @click="todo()">
            Refresh
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <el-form-item label="Status">
          <el-select v-model="temp.status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button v-waves @click="dialogFormVisible = false">
          Cancel
        </el-button>
        <el-button v-waves type="primary" @click="dialogStatus==='create'?createData():updateData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { fetchRobotList, updateRobots } from '@/api/robots'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        Active: 'success',
        Inactive: 'danger'
      }
      return statusMap[status]
    },
    batteryFilter(battery) {
      var tag_val = 'success'
      if (battery < 10) {
        tag_val = 'danger'
      } else if (battery < 20) {
        tag_val = 'warning'
      }
      return tag_val
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        sort: '+id'
      },
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['Active', 'Inactive'],
      temp: {
        id: undefined,
        status: 'Inactive'
      },
      dialogFormVisible: false,
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
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
        this.handleFilter()
      } else if (order === 'descending') {
        this.listQuery.sort = '-id'
        this.handleFilter()
      } else {
        // order === 'null', do nothing
      }
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          updateRobots(tempData).then(() => {
            const index = this.list.findIndex(v => v.id === this.temp.id)
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
    }
  }
}
</script>
