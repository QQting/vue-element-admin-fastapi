import request from '@/utils/request'

export function fetchRobotList(query) {
  return request({
    url: '/robots/discovery',
    method: 'get',
    params: query
  })
}

export function updateRobots(data) {
  return request({
    url: '/robots/update',
    method: 'post',
    data
  })
}

export function updateWifi(data) {
  return request({
    url: '/robots/wifi',
    method: 'post',
    data
  })
}

export function fetchWifi() {
  return request({
    url: '/robots/wifi-init',
    method: 'get'
  })
}
