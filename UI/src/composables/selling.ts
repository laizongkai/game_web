import {useFetch, getFetch} from './api'


export interface SellingProduct{
  id?:string,
  name:string,
  platformer:string,
  production_used:string,
  type:string,
  purchase_price:number,
  selling_price:number,
  count:number,
  income:number,
}

export async function getSelling(start_date:string, end_date:string){
    
    let url = `http://localhost:8000/selling?start_date=${start_date}&end_date=${end_date}`

    const {data:selling, message, error} = await getFetch<SellingProduct[]>(url)

    return {selling, message, error}
}

export async function postSelling(body:any){
  // @ts-expect-error
    const {data:product, message, error} = await useFetch<SellingProduct>('http://localhost:8000/selling', "POST", body)
    console.log(product)
    return {product, message}
}