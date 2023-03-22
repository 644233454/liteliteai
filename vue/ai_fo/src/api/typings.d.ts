export interface KeyValuePair<T> {
  [key: string]: T
}

export interface IOptions extends KeyValuePair<any> {
  headers?: KeyValuePair<string>
  params?: KeyValuePair<any>
}

export declare type HttpMethods = 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE'

export declare type OPtions<T = any> = IOptions
