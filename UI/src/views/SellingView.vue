
<script setup lang = "ts">

import {computed, ref, onMounted} from "vue"
import "bootstrap"
import {getProducts} from '@/composables/products';
import {postSelling} from '@/composables/selling';

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

export interface InsertProduct{
  id?:string,
  name:string,
  platformer:string,
  production_used:string,
  type:string,
  purchase_price:number,
  real_selling_price:number,
  sell_count:number,
  count:number,
}


// const now_page_number = ref<number>(1);
// const total_page_number = ref<number>(0);
// const show_number = ref<number>(5);

const product_data = ref<Product[]|null>([]);
const api_message = ref<string>("");

const table_heads = ["#", "平台", "商品類型", "商品名稱", "操作"]
const selling_table_heads = ["#", "商品名稱", "售出價格", "數量", "操作"]


const search_production = ref<string>("");

const selling_product = ref<InsertProduct>({
    id : "",
    name : "",
    platformer : "",
    production_used : "",
    type : "",
    purchase_price:0,
    real_selling_price:0,
    sell_count:0,
    count:0,
});

const selling_product_list = ref<InsertProduct[]>([]);


const judge_insert_product_repeat = (product_name:string)=>{
    let repeat = false;
    for(let i = 0;i < selling_product_list.value.length;i++){
        if (selling_product_list.value[i].name == product_name){
            repeat = true;
            break;
        }
    }
    return repeat
}

const insert_product_to_selling_list = (item:any) => {
    let repeat = judge_insert_product_repeat(item.name);
    if (repeat == true){
        return;
    }
    else{
        selling_product.value.id = item.id;
        selling_product.value.name = item.name;
        selling_product.value.platformer = item.platformer;
        selling_product.value.production_used = item.production_used;
        selling_product.value.type = item.type;
        selling_product.value.purchase_price = item.purchase_price;
        
        selling_product.value.count = item.count;


        selling_product_list.value.push({...selling_product.value});
    }
    
}

const remove_selling_product = (index:number)=>{
    selling_product_list.value.splice(index, 1);
}


const submit_selling = async ()=>{

    let check_ = check_submit_data();

    if (check_ == false){
        window.alert("有價格或數量有未輸入");
        return ;
    }
    else{

        let body = {
            selling_list:JSON.stringify(selling_product_list.value)
        }

        const {product, message} = await postSelling(body);
    
        if(message.value == "OK"){
            remove_data_for_update_success_in_db(product);
            window.alert("新增成功");
        }
        else{
            if(message.value == "Error Count"){
                window.alert(`該產品數量超過資料庫儲存數量：${product.value}`);
            }

            else if(message.value == "Error Selling Count"){
                window.alert(`該產品銷售數量錯誤：${product.value}`);
            }

            else if(message.value == "Error Selling Price"){
                window.alert(`該產品銷售價格錯誤：${product.value}`);
            }

            else{
                window.alert("系統後端出錯");
            }
        }
    }
}


const check_submit_data = () =>{
    let check_ = true;
    for(let i = 0;i < selling_product_list.value.length;i++){
        if (selling_product_list.value[i].sell_count == 0 || selling_product_list.value[i].real_selling_price == 0){
            check_ = false;
            break;
        }
    }

    return check_;
}

const remove_data_for_update_success_in_db = (success_data_list:any)=>{
    for(let i = 0;i < success_data_list.value.length;i++){
        for(let j = 0; j < selling_product_list.value.length;j++){
            if(selling_product_list.value![j].id == success_data_list.value[i].id){
                selling_product_list.value.splice(j, 1);
                break;
            }

        }
    }
    
}


async function load_db_data(){
// @ts-ignore
  const {products, message, error} =  await getProducts();
  product_data.value = products.value;
  api_message.value = message.value;
}

const get_db_data = async ()=>{
    await load_db_data()
    //total_page_number.value = Math.ceil(product_data.value!.length / show_number.value);
}

onMounted(()=>{
    get_db_data()
})


const table_list = computed(()=>{
    
    let temp = []
    let insert_status = false;
    for(let i = 0 ;i < product_data.value!.length;i++){
        insert_status = false;
        if(search_production.value != ""){
            if(product_data.value![i].name.search(search_production.value) != -1){
                insert_status = true;
            }
        }
        else{
            insert_status = true;
        }
        
        if(insert_status == true){
            temp.push(product_data.value![i])
        }
    }

    return temp
})

</script>

<template>
    <div id = "view_body" >
        <div  class = "selling-body" style = "width:90%;height:90%;">
            <div style = "width: 50%;height: 100%; position: relative;">
                <div id="product-list">

                    <div class = "search-body" >
                        <div class = "search-component" style = "height:60px; display: flex;flex-direction: row;">
                            <label class = "input-label"> 商品名稱： </label>
                            <input class = "form-control" style = "width: 70%;" v-model="search_production">
                        </div>
                        <hr>
                    </div>
                    
                    <div class = "product-table-sticky-wrapper">
                        <table class = "table table-hover">
                            <thead class = "product-table-thead">
                                <tr>
                                    <th  class = "text-center" scope="col" v-for = "head_item in table_heads" style="font-weight: bolder; background-color: rgb(120,180,200);"> {{head_item}} </th>
                                </tr>
                            </thead>
                        
                            <tbody class = "product-table-tbody">
                                <tr v-for = "(item, index) in table_list" style = "height: 40px;" >
                                    <td class = "align-middle text-center" scope = "row"> {{index + 1}} </td>
                                    <td class = "align-middle text-center" style = "width: 10%;"> {{ item.platformer }}</td>
                                    <td class = "align-middle text-center" style = "width: 20%;"> {{item.type}} </td>
                                    <td class = "align-middle text-center" style = "width: 40%;"> {{item.name}} </td>
                                    <td class = "align-middle text-center" style = "width: 15%;">
                                        <button v-if = "item.count > 0" class = "btn btn-success table-btn" @click="insert_product_to_selling_list(item)">
                                            匯入
                                        </button>
                                        <button v-else class = "btn btn-success table-btn" disabled>
                                            匯入
                                        </button>

                                    </td>
                                </tr>
                            
                            </tbody>
                        
                        </table>    
                    </div>
                </div>

            </div>

            <div style = "width: 45%;">
                <h4>售出商品 </h4>
                <div class = "selling-table-sticky-wrapper">
                    <table class = "table table-hover">
                        <thead  class = "product-table-thead">
                            <tr>
                                <th class = "text-center selling-table-thead" scope="col" v-for = "head_item in selling_table_heads" style="font-weight: bolder; background-color: rgb(42, 212, 189);"> {{head_item}} </th>
                            </tr>
                        </thead>

                        <tbody class = "product-table-tbody">
                            <tr v-for = "(selling_item, index) in selling_product_list" >
                                <th class = "align-middle text-center" scope = "row"> {{index + 1}} </th>
                                <td class = "align-middle text-center" style = "width: 40%;"> 
                                    <input class="form-control" id = "exampleFormControlInput1" v-model="selling_item.name" disabled>
                                </td>
                                <td class = "align-middle text-center" style = "width: 15%;"> 
                                    <input class="form-control" id = "exampleFormControlInput1"  v-model="selling_item.real_selling_price" placeholder = "1790">
                                </td>
                                <td class = "align-middle text-center" style = "width: 15%;"> 
                                    <input class="form-control" id = "exampleFormControlInput1" v-model="selling_item.sell_count" placeholder = "1">    
                                </td>

                                <td class = "align-middle text-center" style = "width: 15%;">
                                    <button class = "btn btn-danger table-btn" @click = "remove_selling_product(index)">
                                        刪除
                                    </button>
                                </td>
                        
                            </tr>
                            
                        </tbody>
                    </table>  
                </div>

                <button class = "btn btn-primary" style = "height: 40px; width: 120px;" @click = "submit_selling" >
                    送出
                </button>
            </div>
        </div>
    </div>
</template>

<style>
#view_body{
    display:flex;
    flex-direction: column; 
    flex-wrap:wrap; 
    /* justify-content: center;  */
    align-content: center; 
}

.selling-body{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    
    justify-content: space-around;
    align-content: center;
    align-items: center;
}

#product-list{
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 10px;
    padding-bottom: 10px;
    height: auto;
    min-height:750px;
    max-height: 750px;

    border: 1px solid rgb(199,199,199);
    border-radius: 10px;

    
}

.search-component, .input-label{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    align-content: center;
}

table{
    width: 100%;
    /* table-layout: fixed; */
}

table thead th{
    position: sticky;
    z-index: 1;
    top:0px;
}

tbody td{
    z-index: 0;
}

.product-table-sticky-wrapper, .selling-table-sticky-wrapper{
    width: 100%;
    height: 600px;
    overflow: auto;
}

.selling-table-sticky-wrapper{
    border: 1px solid rgb(199,199,199);
    border-radius: 10px;
    margin-bottom: 10px;
}

.selling-table-thead{
    font-weight: bolder;
    background-color: rgb(42, 212, 189);
}

.product-table-tbody{
    position: relative;
    z-index: 0;
    height: auto;
    width: 100%;
    overflow: hidden;
}

.input-label{
    font-weight: bolder;
}

</style>