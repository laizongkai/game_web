
import { ref } from 'vue'
import type {Ref} from 'vue'
export type ApiRequest = ()=> Promise<void>

export function useApi<T>(url:RequestInfo, options?:RequestInit){
    const response: Ref< T | undefined> = ref();

    console.log(url, options)
    // const request = async ()=> {
    //     const res = await fetch(url, options);
    //     const data = await res.json();
    //     response.value = data;
    // }

    const request:ApiRequest = async ()=> {
        const res = await fetch(url, options);
        const data = await res.json();
        response.value = data;
    }
    return {response, request};
}

export interface Product{
  id?:string,
  name:string,
  platformer:string,
  production_used:string,
  type:string,
  purchase_price:number,
  selling_price:number,
  img_path:string,
  img_base64?:string|null|ArrayBuffer,
  count:number
}

// @ts-expect-error
export async function getFetch<T>(url:string) {
    const data = ref(null);
    const message = ref("");
    const error = ref(null);
    
    const fetchData = async () => {
        data.value = null;
        message.value = "";
        error.value = null;

        await fetch(url, {
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method: "GET",
        })
        .then((res) => {
            return res.json()
        })
        .then((json) => {
            data.value = json.data;
            message.value = json.message;
        })
        .catch((err) => (error.value = err))
    }

    await fetchData()
    return { data, message, error }
}


export async function useFetch<T>(url:string, option:string, input_data?:any) {
    const data = ref(null);
    const error = ref(null);
    const message = ref("");
    // @ts-expect-error
    const response: Ref< T | undefined> = ref();

    const fetchData = async () => {
        // reset state before fetching..
        data.value = null
        error.value = null

        await fetch(url, {
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method: option,
            body: JSON.stringify(input_data)
        })
        .then((res) => {
            return res.json()
        })
        .then((json) => {
            data.value = json.data;
            message.value = json.message;
            // response.value = json;
        })
        .catch((err) => (error.value = err))
    }

    await fetchData()

    return { data, message, error }
}