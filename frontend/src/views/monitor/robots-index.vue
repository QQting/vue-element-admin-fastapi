<template>
  <div class="app-container">
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
    >
      <el-table-column label="Index" prop="Index" sortable align="center" width="80" :class-name="getSortClass('Index')">
        <template #default="{row}">
          <span>{{ row.index }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Device ID" width="110px" align="center">
        <template #default="{row}">
          <span>{{ row.deviceID }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Hostname" width="110px" align="center">
        <template #default="{row}">
          <span>{{ row.hostname }}</span>
        </template>
      </el-table-column>
      <el-table-column label="CPU Usage" width="160px" align="center">
        <template #default="{row}">
          <el-progress :percentage="row.cpu" :color="usageColorMethod" />
        </template>
      </el-table-column>
      <el-table-column label="Disk Usage" width="160px" align="center">
        <template #default="{row}">
          <el-progress :percentage="50" :color="usageColorMethod" />
        </template>
      </el-table-column>
      <el-table-column label="RAM Usage" width="160px" align="center">
        <template #default="{row}">
          <el-progress :percentage="row.ram" :color="usageColorMethod" />
        </template>
      </el-table-column>
      <el-table-column label="Battery Level" width="160px" align="center">
        <template #default="{row}">
          <el-progress :percentage="99" :color="batteryColorMethod" />
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />
  </div>
</template>

<script>
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import io from 'socket.io-client'

export default {
  name: 'ComplexTable',
  components: { Pagination },
  data() {
    return {
      tableKey: 0,
      percentage: 0,
      list: null,
      total: 0,
      isIndeterminate: true,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        sort: '+Index'
      },
      sortOptions: [{ label: 'Index Ascending', key: '+Index' }, { label: 'Index Descending', key: '-Index' }],
      temp: {
        index: undefined
      },
      dialogStatus: ''
    }
  },
  created() {
    this.getList()
  },
  beforeDestroy() {
    this.socket.close()
  },
  methods: {
    getList() {
      const _this = this
      this.socket = io(process.env.VUE_APP_BASE_API + '/server', {
        transports: ['websocket']
      })
      this.socket.on('monitor_robot', function(data) {
        _this.list = data.items
        _this.total = data.total
        _this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
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
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    },
    usageColorMethod(percentage) {
      if (percentage < 30) {
        return '#67c23a'
      } else if (percentage < 70) {
        return '#6f7ad3'
      } else {
        return '#f56c6c'
      }
    },
    batteryColorMethod(percentage) {
      if (percentage < 50) {
        return '#f56c6c'
      } else if (percentage < 80) {
        return '#F9F900'
      } else {
        return '#67c23a'
      }
    }
  }
}
</script>

