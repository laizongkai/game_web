
import {useFetch, getFetch} from './api'

export interface Valiant{
    id:string
    title:string
    sku:string
    quantity:number
}

export interface Product{
  id:string,
  name:string,
  platformer:string,
  production_used:string,
  type:string,
  purchase_price:number,
  selling_price:number,
  img_path:string,
  count:number
}

// export async function getProducts(){
//     const {response:products, request} = useApi<Product[]>('http://localhost:8000/products')
    
//     const loaded = ref(false);

//     if (loaded.value == false){
//         await request();
//         loaded.value = true;
//     }

//     return {products}
// }

// @ts-expect-error
export async function getProducts(name?:any){
    
    //let url = `http://localhost:8000/products?product_name=${name}`

    let url = `http://localhost:8000/products`

    const {data:products, message, error} = await getFetch<Product[]>(url)

    return {products, message, error}
}


export async function postProducts(body:any){
    // @ts-expect-error
    const {data:product, message, error} = await useFetch<Product>('http://localhost:8000/products', "POST", body)
    console.log(product)
    return {product, message}
}

export async function putProducts(body:any){
    console.log(body)
    // @ts-expect-error
    const {data:product, message, error} = await useFetch<Product>('http://localhost:8000/products', "PUT", body)
    return {product, message}
}

export async function deleteProducts(body:any){
    // @ts-expect-error
    const {data:product, message, error} = await useFetch<Product>('http://localhost:8000/products', "DELETE", body)
    return {product, message}
}