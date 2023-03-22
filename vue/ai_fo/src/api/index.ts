// import axios from 'axios'
import axios, { AxiosRequestConfig } from 'axios'
import { HttpMethods } from './typings'
import router from '@/router'


const url = 'https://bot.liteliteai.top/'

const baseConfig: AxiosRequestConfig = {
  baseURL: url,
  headers: {
    'x-auth-token': localStorage.getItem('token') || '',
    'content-type': 'multipart/form-data',
  },
  timeout: 60000,
}

const _axios = axios.create(baseConfig)

// 请求拦截
_axios.interceptors.request.use(
  (req) => {
    // 当getters里面的isLoading为true再显示请求加载
    return req
  },
  (err) => {
    return Promise.reject(err)
  },
)

// 响应拦截
_axios.interceptors.response.use(
  (res) => {
    return res.data
  },
  (err) => {
    return Promise.reject(err)
  },
)

function request(method: HttpMethods, url: string, params: any) {
  const defered = _axios({
    method,
    url,
    data: params.data,
    headers: {
      'x-auth-token': localStorage.getItem('token') || '',
    },
  })
  return defered
}

const get = (url: string, data = {}): any => {
  return new Promise((resolve, reject) => {
    request('GET', url, {
      data,
    })
      .then((response) => response.data)
      .then((res) => {
        resolve(res)
      })
      .catch((err) => {
        reject(err.response)
      })
  })
}

const post = (url: string, data = {}): any => {
  return new Promise((resolve, reject) => {
    request('POST', url, {
      data,
    })
      .then((response) => {
        resolve(response.data)
      })
      .catch((err) => {
        reject(err.response)
      })
  })
}
const postNoData = (url: string, data = {}): any => {
  return new Promise((resolve, reject) => {
    request('POST', url, {
      data,
    })
      .then((response) => {
        resolve(response)
      })
      .catch((err) => {
        reject(err.response)
      })
  })
}
export default {
  get,
  post,
  postNoData,
}
