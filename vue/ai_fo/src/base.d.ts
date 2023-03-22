// eslint-disable-next-line @typescript-eslint/no-unused-vars
declare namespace Api {
  interface Response<T> {
    code: number
    message: string
    data: T
    success?: boolean
    traceId?: string
  }
  interface RichResponse {
    data: {
      content: string
      version?: string
    }
    success?: boolean
  }
  interface ListResponse<T> {
    code: number
    message: string
    data: {
      data: T
      pageParam: {
        pageNum: number
        pageSize: number
        limitOffset: number
        limitRows: number
      }
      totalCount: number
      totalPage: number
    }
    success: boolean
  }
  type ListQuery<T = unknown> = {
    pageNum?: number
    pageSize?: number
  } & T
}
