import request from '@/utils/request'

export function fetchRobotList(query) {
  return request({
    url: '/vue-element-admin/robots/list',
    method: 'get',
    params: query
  })
}

export function updateRobots(data) {
  return request({
    url: '/vue-element-admin/robots/update',
    method: 'post',
    data
  })
}
