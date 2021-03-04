import request from '@/utils/request'

export function fetchRobotList(query) {
  return request({
    url: '/robots/list',
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
