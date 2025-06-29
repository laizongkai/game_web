
<script setup lang = "ts">

import SearchForm from '@/components/SearchForm.vue'
//import "bootstrap"
import { computed, onMounted, ref} from 'vue';

//@ts-ignore
import {getProducts, postProducts, putProducts, deleteProducts} from '@/composables/products';

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

const table_heads = ["#", "平台", "商品類型", "新/舊", "商品名稱", "進貨價格", "建議售價", "剩餘數量", "操作"]

const now_page_number = ref<number>(1);
const total_page_number = ref<number>(0);
const show_number = ref<number>(5);

const product_data = ref<Product[]|null>([]);
const show_data = ref<any[]|null>([]);
const api_message = ref<string>("");

const error_message = ref<string>("");

const create_item = ref<Product>({
    name:"",
    platformer:"",
    production_used:"",
    type:"",
    purchase_price:0,
    selling_price:0,
    img_path:"",
    img_base64:"",
    count:0
})

const selected_item = ref<Product>({
    id: "",
    name:"",
    platformer:"",
    production_used:"",
    type:"",
    purchase_price:0,
    selling_price:0,
    img_path:"",
    count:0
})

const delete_item_id = ref<string>("");

/*------------ method ------------- */

const page_update = (update_number:number)=>{
    now_page_number.value += update_number;
}

const edit_item = (edit_item:Product) => {
    selected_item.value = {...edit_item};

    // var input = document.getElementById('image_uploads');
    // var preview = document.querySelector('.preview');
    //input.style.opacity = 0;
}

const delete_item = (id:string)=>{
    delete_item_id.value = id;
}

async function load_db_data(){
    //@ts-ignore
  const {products, message, error} =  await getProducts();
  product_data.value = products.value;
  api_message.value = message.value;
}

const get_db_data = async ()=>{
    await load_db_data()
    show_data.value = [...product_data.value!];
    //total_page_number.value = Math.ceil(product_data.value!.length / show_number.value);
    update_show_data_page()
}

const loadFile = function(event:any, mode:string) {
    var reader = new FileReader();
    reader.onload = function(){
        if (mode == "create"){
            let output = document.getElementById('create_img') as HTMLImageElement;
            // @ts-ignore
            output!.src = reader.result;
            create_item.value.img_base64 = reader.result;
        }
        else{
            let output = document.getElementById('edit_img');
            // @ts-ignore
            output!.src = reader.result;
            selected_item.value.img_base64 = reader.result;
        }
      
    };
    reader.readAsDataURL(event.target.files[0]);

    if (mode == "create"){
        create_item.value.img_path = event.target.files[0].name;    
    }
    else{
        selected_item.value.img_path = event.target.files[0].name;
    }
};

const get_image_path = (img_name:string)=>{ 
  let path = `http://127.0.0.1:8000/products/get-image/${img_name}`
  return path
}

const create_product = async () => {

    if (create_item.value.name == "" || create_item.value.platformer == "" || create_item.value.production_used == "" || create_item.value.type == ""){
        error_message.value = "有必填欄位未填寫";
        return ;
    }

    else{
        error_message.value = "";

        let body = {
            name: create_item.value.name,
            platformer: create_item.value.platformer,
            production_used: create_item.value.production_used,
            type: create_item.value.type,
            purchase_price: create_item.value.purchase_price,
            selling_price: create_item.value.selling_price,
            img_path: create_item.value.img_path,
            img_base64:create_item.value.img_base64,
            count:create_item.value.count
        }

        const {product, message} =  await postProducts(body);
        
        if (message.value == 'OK'){
            if(product != null){
                update_data_list("create", product)
                
            }

            close_Create_Modal();
            clear_create_modal_par();
        }
        
        else{
            error_message.value = message.value;
        }

    }
}

const close_Create_Modal = ()=>{
    let closebtn = document.getElementById("CreateModalCloseBtn");
    closebtn?.click();
}

const clear_create_modal_par = ()=>{
    error_message.value = "";

    create_item.value.name = "";
    create_item.value.platformer = "";
    create_item.value.production_used = "";
    create_item.value.type = "";
    create_item.value.purchase_price = 0;
    create_item.value.selling_price = 0;
    create_item.value.img_path = "";
    create_item.value.img_base64 = "";
    create_item.value.count = 0;
}


const edit_product = async () => {

    let body = {
        id:selected_item.value.id,
        name: selected_item.value.name,
        platformer: selected_item.value.platformer,
        production_used: selected_item.value.production_used,
        type: selected_item.value.type,
        purchase_price: selected_item.value.purchase_price,
        selling_price: selected_item.value.selling_price,
        img_path: selected_item.value.img_path,
        img_base64:selected_item.value.img_base64,
        count:selected_item.value.count
    }

    const {product, message} =  await putProducts(body);
    if (message.value == 'OK'){
        
        if(product != null){
            update_data_list("edit", product)
            
        }

        close_Edit_Modal();
        clear_edit_modal_par();
    }
    
    else{
        error_message.value = message.value;
        window.alert("Error");
    }
}

const close_Edit_Modal = ()=>{
    let closebtn = document.getElementById("EditModalCloseBtn");
    closebtn?.click();
}

const clear_edit_modal_par = ()=>{
    error_message.value = "";
}


const delete_product = async () => {

    let body = {
        id:delete_item_id.value,
    }

    const {product, message} =  await deleteProducts(body);

    if (message.value == 'OK'){
        if(product != null){
            update_data_list("delete", product)
        }

        close_Delete_Modal();
        clear_delete_modal_par();
    }
    
    else{
        error_message.value = message.value;
    }
}

const close_Delete_Modal = ()=>{
    let closebtn = document.getElementById("DeleteModalCloseBtn");
    closebtn?.click();
}

const clear_delete_modal_par = ()=>{
    error_message.value = "";
}


const update_data_list = (mode:string, data:any)=>{

    if(mode == "create"){
        product_data.value?.push(data.value)
    }

    else if(mode == "edit"){
        for(let i = 0;i < product_data.value!.length;i++){
            if(product_data.value![i].id == data.value.id){
                product_data.value![i] = data.value;
                break;
            }
        }
    }

    else{
        for(let i = 0;i < product_data.value!.length;i++){
            if(product_data.value![i].id == data.value.id){
                product_data.value?.splice(i, 1)
                break;
            }
        }
    }

    show_data.value = [...product_data.value!];
    //total_page_number.value = Math.ceil(product_data.value!.length / show_number.value);
}


const update_show_data_page = () => {
  total_page_number.value = Math.ceil(show_data.value!.length / show_number.value);
  now_page_number.value = 1;
}

const search_data = (data:any) => {
  let type_index = search_data_type(data.type);
  let platformer_index = search_data_platformer(data.platformer);
  let count_index = search_data_count(data.product_exist);
  let name_index = search_data_name(data.name);
  show_data.value!.length = 0;
    //console.log(data)
  for(let i = 0; i < product_data.value!.length;i++){
    if(type_index.includes(i) && platformer_index.includes(i) && count_index.includes(i) && name_index.includes(i)){
      show_data.value?.push(product_data.value![i])
    }
  }

  update_show_data_page()
}

const search_data_type = (type:string)=>{
  let temp:any = [];

  for(let i = 0 ;i < product_data.value!.length; i++){
    if(type != ""){
      if(product_data.value![i].type == type){
        temp.push(i);
      }
    }
    else{
      temp.push(i);
    }
  }

  return temp;
}


const search_data_platformer = (platformer:string)=>{
  let temp:any = []
  for(let i = 0 ;i < product_data.value!.length; i++){
    if(platformer != ""){
      if(product_data.value![i].platformer == platformer){
        temp.push(i);
      }
    }
    else{
      temp.push(i);
    }
  }

  return temp;
}


const search_data_count = (product_exist:string)=>{
  let temp:any = []
  for(let i = 0 ;i < product_data.value!.length; i++){
    if(product_exist != ""){
      if(product_data.value![i].count > 0){
        temp.push(i);
      }
    }
    else{
      temp.push(i);
    }
  }

  return temp;
}

const search_data_name = (name:string)=>{
  let temp:any = []
  for(let i = 0 ;i < product_data.value!.length; i++){
    if(name != ""){
      if(product_data.value![i].name.includes(name)){
        temp.push(i);
      }
    }
    else{
      temp.push(i);
    }
  }

  return temp;
}

onMounted(()=>{
    get_db_data()
})


const table_list = computed(()=>{
    let start_index = (now_page_number.value - 1 ) * show_number.value;
    let end_index = now_page_number.value * show_number.value;
    let temp = []
    for(let i = start_index ;i < end_index;i++){
        if(i < show_data.value!.length){
            temp.push(show_data.value![i]);
        }
    }
    return temp
})


</script>


<template>
    <div id = "view_body" >
        <div style="width:90%;">
            <SearchForm @search = "search_data"></SearchForm>
            <hr style = "border: 1px solid;">
            
            <div id = "title_and_create">
                <div style = "display: flex; flex-direction: row;">
                    <label class = "title"> 管理列表 </label>
                    <button class = "btn btn-primary create-btn" data-bs-toggle = "modal" data-bs-target = "#CreateModal">
                        新增
                    </button>
                </div>

                <nav aria-label = "Page navigation example">
                    <ul class="pagination">
                        <li class="page-item" v-if = "now_page_number <= 1">
                            <a class="page-link" href="#" aria-label="Previous">
                                <span aria-hidden="true">&laquo;</span>
                            </a>
                        </li>
                        <li class="page-item" @click = "page_update(-1)" v-else >
                            <a class="page-link" href="#" aria-label="Previous">
                                <span aria-hidden="true">&laquo;</span>
                            </a>
                        </li>
                        <li class="page-item"><a class="page-link" href="#" @click = "page_update(-1)" v-if = "now_page_number > 1"> {{ now_page_number - 1}} </a></li>
                        <li class="page-item"><a class="page-link" href="#" style = "background: rgb(120, 120, 120);"> {{ now_page_number }} </a></li>
                        <li class="page-item"><a class="page-link" href="#" @click = "page_update(+1)" v-if = "now_page_number < total_page_number" > {{ now_page_number + 1}} </a></li>
                        <li class="page-item" v-if = " now_page_number < total_page_number " @click = "page_update(+1)">
                            <a class="page-link" href="#" aria-label="Next">
                                <span aria-hidden="true">&raquo;</span>
                            </a>
                        </li>

                        <li class="page-item" v-else>
                            <a class="page-link" href="#" aria-label="Next">
                                <span aria-hidden="true">&raquo;</span>
                            </a>
                        </li>

                    </ul>
                </nav>

                
            </div>

            <div  id = "product-management-list">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th class = "text-center" scope="col" v-for = "head_item in table_heads" style="font-weight: bolder;"> {{head_item}} </th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for = "(item, index) in table_list" >
                            <th class = "align-middle text-center" scope = "row"> {{index + show_number * (now_page_number - 1) + 1}} </th>
                            <td class = "align-middle text-center" style = "width: 10%;"> {{ item.platformer }}</td>
                            <td class = "align-middle text-center" style = "width: 10%;"> {{item.type}} </td>
                            <td class = "align-middle text-center" style = "width: 10%;"> {{item.production_used}} </td>
                            <td class = "align-middle text-center"> {{item.name}} </td>
                            <td class = "align-middle text-center" style = "width: 10%;"> {{item.purchase_price}} </td>
                            <td class = "align-middle text-center" style = "width: 10%;"> {{item.selling_price}} </td>
                            <td class = "align-middle text-center" style = "width: 10%;"> {{item.count}} </td>
                            <td class = "align-middle text-center" style = "width: 15%;">
                                <button class = "btn btn-primary table-btn" data-bs-toggle = "modal" data-bs-target = "#EditModal" @click = "edit_item(item)">
                                    編輯
                                </button>

                                <button class = "btn btn-danger table-btn" data-bs-toggle = "modal" data-bs-target = "#DeleteModal" @click = "delete_item(item.id!)">
                                    刪除
                                </button>
                            </td>
                        </tr>
                        
                    </tbody>
                </table>

                <!-- Create Modal -->
                <div class="modal fade" id = "CreateModal" aria-hidden="true" data-bs-backdrop = "static" data-bs-keyboard="false" aria-labelledby="exampleModalToggleLabel" tabindex="-1">
                    <div class="modal-dialog modal-dialog-centered modal-xl" style = "width: 1300px; min-width: 650px; ">
                        <div class="modal-content">

                            <div class="modal-header">
                                <h5 class="modal-title" id = "exampleModalToggleLabel"> 新增資料 </h5>
                                <button id = "CreateModalCloseBtn" type = "button" class = "btn-close" data-bs-dismiss = "modal" aria-label = "Close" @click = "clear_create_modal_par()"></button>
                            </div>
                            <div class="modal-body">
                                <div class = "modal-form" style="width: 100%; height:50%;">
                                    <div style = "width: 400px; height: 250px;position: relative; display: flex; flex-direction: row; flex-wrap: wrap; justify-content: center; align-content: center;overflow-x: hidden; border: 2px solid gainsboro; border-radius: 10px;" >
                                        <div style="width: 100%; opacity: 0;">
                                            <input type="file" id="image_uploads" name="image_uploads" accept = ".jpg, .jpeg, .png" @change = "loadFile($event, 'create')" style="position:absolute;background-color: aqua;height: 100%; width: 100%;">
                                        </div>
                                        
                                        <img v-if = "create_item.img_path != '' "  id = "create_img" v-bind:src = create_item.img_path style = "height: 100%;" class = "preview">
                                        <img v-else src = "/game.png" style = "height: 100%;" class = "preview">
                                    
                                    </div>
                                    
                                    <div class = "modal-form-body" style = "width: 600px; height:250px;">

                                        <div class = "modal-form-component" > 
                                            <label class = "modal-form-component-title"> 商品名稱： </label>
                                            <input class = "form-control" style = "width: 500px;" v-model = "create_item.name">
                                        </div>

                                        <div class = "modal-form-row">
                                            <div class = "modal-form-component" > 
                                                <label class = "modal-form-component-title"> 平台： </label>
                                                <select class = "form-select" style = "width: 150px;" v-model = "create_item.platformer">
                                                    <option> PS4 </option>
                                                    <option> PS5 </option>
                                                    <option> Switch </option>
                                                    <option> Switch2 </option>
                                                    <option> PC </option>
                                                    <option> 其它 </option>
                                                </select>
                                            </div>

                                            <div class = "modal-form-component" > 
                                                <label class = "modal-form-component-title"> 商品類型： </label>
                                                <select class = "form-select" style = "width: 150px;" v-model = "create_item.type">
                                                    <option> 遊戲 </option>
                                                    <option> 配件 </option>
                                                    <option> 其它 </option>
                                                </select>
                                            </div>
                                        </div>

                                        <div class = "edit-form-row">
                                            <div class = "edit-form-component" > 
                                                <label class = "edit-form-component-title"> 進貨價格： </label>
                                                <input class = "form-control" style = "width: 150px;" v-model = "create_item.purchase_price" >
                                            </div>

                                            <div class = "edit-form-component" > 
                                                <label class = "edit-form-component-title"> 售出價格： </label>
                                                <input class = "form-control" style = "width: 150px;" v-model = "create_item.selling_price">
                                            </div>
                                        </div>

                                        <div class = "edit-form-row">
                                            <div class = "edit-form-component" > 
                                                <label class = "edit-form-component-title"> 剩餘數量： </label>
                                                <input class = "form-control" style = "width: 150px;" v-model = "create_item.count">
                                            </div>

                                            <div class = "edit-form-component" > 
                                                <label class = "edit-form-component-title"> 新/舊： </label>
                                                <select class = "form-select" style = "width: 150px;" v-model = "create_item.production_used">
                                                    <option> 新品 </option>
                                                    <option> 二手 </option>
                                                </select>
                                            </div>
                                        </div>

                                        <div>  
                                            <div class="input-group mb-3">
                                                <label class = "edit-form-component-title"> 圖片上傳： </label>
                                                <input class = "form-control" id = "inputGroupFile02" v-model = "create_item.img_path" v-if = "create_item.img_path != ''" disabled>
                                                <input class = "form-control" value = "請上傳檔案" v-else disabled>
                                            </div>
                                        </div>

                                    </div>
                                </div>

                                <div v-if = "error_message != '' " class = "alert alert-danger" role = "alert" style = "margin-top: 10px;">
                                    {{ error_message }}
                                </div>

                            </div>
                            <div class="modal-footer">
                                <button class="btn btn-secondary" style = "width: 80px;" data-bs-dismiss = "modal" @click="clear_create_modal_par()"> 取消 </button>
                                <button class="btn btn-primary" style = "width: 80px;" @click = "create_product()" > 確認 </button>
                            </div>

                        </div>
                    </div>
                </div>

                <!-- Edit Modal -->
                <div class="modal fade" id = "EditModal" aria-hidden="true" data-bs-backdrop = "static" data-bs-keyboard="false" aria-labelledby="exampleModalToggleLabel" tabindex="-1">
                    <div class="modal-dialog modal-dialog-centered modal-xl" style = "width: 1300px; min-width: 650px; ">
                        <div class="modal-content">

                            <div class="modal-header">
                                <h5 class="modal-title" id="exampleModalToggleLabel"> 編輯資料 </h5>
                                <button id = "EditModalCloseBtn" type = "button" class = "btn-close" data-bs-dismiss = "modal" aria-label = "Close" @click="clear_edit_modal_par"></button>
                            </div>
                            <div class="modal-body">
                                <div class = "edit-form" style="width: 100%; height:50%;">
                                    <!-- <div style = "width: 400px; height:100%; display: flex; flex-direction: row; flex-wrap: wrap; justify-content: center; align-content: center;overflow-x: hidden;" > -->
                                        <!-- <img id = "show_img" v-bind:src = selected_item.img_path style = "height: 80%; "> -->
                                    <div style = "width: 400px; height: 250px;position: relative; display: flex; flex-direction: row; flex-wrap: wrap; justify-content: center; align-content: center;overflow-x: hidden; border: 2px solid gainsboro; border-radius: 10px;" >
                                        <div style="width: 100%; opacity: 0;">
                                            <input type="file" id="image_uploads" name="image_uploads" accept = ".jpg, .jpeg, .png" @change = "loadFile($event, 'edit')" style="position:absolute;background-color: aqua;height: 100%; width: 100%;">
                                        </div>
                                        
                                        <img v-if = "selected_item.img_path != '' "  id = "edit_img" v-bind:src = "get_image_path(selected_item.img_path)"  style = "height: 100%;" class = "preview">
                                        <img v-else src = "/game.png" style = "height: 100%;" class = "preview">
                                        <!-- <div v-else class="preview" style="float:left;background:#cccccc;height:100%;width:100%;text-align:center;z-index:1;">
                                            <p style="line-height: 250px;"> 未選擇任何檔案 </p>
                                        </div> -->
                                    
                                    </div>
                                    
                                    <div class = "edit-form-body" style = "width: 600px; height:250px;">

                                        <div class = "edit-form-component" > 
                                            <label class = "edit-form-component-title"> 商品名稱： </label>
                                            <input class = "form-control" style = "width: 500px;" v-model = "selected_item.name">
                                        </div>

                                        <div class = "edit-form-row">
                                            <div class = "edit-form-component" > 
                                                <label class = "edit-form-component-title"> 平台： </label>
                                                <select class = "form-select" style = "width: 150px;" v-model = "selected_item.platformer">
                                                    <option> PS4 </option>
                                                    <option> PS5 </option>
                                                    <option> Switch </option>
                                                    <option> Switch2 </option>
                                                    <option> PC </option>
                                                    <option> 其它 </option>
                                                </select>
                                            </div>

                                            <div class = "edit-form-component" > 
                                                <label class = "edit-form-component-title"> 商品類型： </label>
                                                <select class = "form-select" style = "width: 150px;" v-model = "selected_item.type">
                                                    <option> 遊戲 </option>
                                                    <option> 配件 </option>
                                                    <option> 其它 </option>
                                                </select>
                                            </div>
                                        </div>

                                        <div class = "edit-form-row">
                                            <div class = "edit-form-component" > 
                                                <label class = "edit-form-component-title"> 進貨價格： </label>
                                                <input class = "form-control" style = "width: 150px;" v-model = "selected_item.purchase_price" >
                                            </div>

                                            <div class = "edit-form-component" > 
                                                <label class = "edit-form-component-title"> 售出價格： </label>
                                                <input class = "form-control" style = "width: 150px;" v-model = "selected_item.selling_price">
                                            </div>
                                        </div>

                                        <div class="edit-form-row">
                                            <div class = "edit-form-component" > 
                                                <label class = "edit-form-component-title"> 剩餘數量： </label>
                                                <input class = "form-control" style = "width: 150px;" v-model = "selected_item.count">
                                            </div>

                                            <div class = "edit-form-component" > 
                                                <label class = "edit-form-component-title"> 新/舊： </label>
                                                <select class = "form-select" style = "width: 150px;" v-model = "selected_item.production_used">
                                                    <option> 新品 </option>
                                                    <option> 二手 </option>
                                                </select>
                                            </div>
                                        </div>

                                        <div>  
                                            <div class="input-group mb-3">
                                                <label class = "edit-form-component-title"> 圖片上傳： </label>
                                                <input class = "form-control" id = "inputGroupFile02" v-model = "selected_item.img_path" v-if = "selected_item.img_path != ''" disabled>
                                                <input class = "form-control" value = "請上傳檔案" v-else disabled>
                                            </div>
                                        </div>

                                    </div>
                                </div>

                                <div v-if = "error_message != '' " class = "alert alert-danger" role = "alert" style = "margin-top: 10px;">
                                    {{ error_message }}
                                </div>

                            </div>
                            <div class="modal-footer">
                                <button class="btn btn-secondary" style = "width: 80px;" data-bs-dismiss = "modal"  @click="clear_edit_modal_par"> 取消 </button>
                                <button class="btn btn-primary" style = "width: 80px;"  @click="edit_product"> 確認 </button>
                            </div>

                        </div>
                    </div>
                </div>


                <!-- Delete Modal -->
                <div class="modal fade" id = "DeleteModal" aria-hidden="true" data-bs-backdrop = "static" data-bs-keyboard="false" aria-labelledby="exampleModalToggleLabel" tabindex="-1">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">

                            <div class="modal-header">
                                <h5 class = "modal-title" id = "exampleModalToggleLabel"> 刪除確認 </h5>
                                <button id = "DeleteModalCloseBtn" type = "button" class = "btn-close" data-bs-dismiss = "modal" aria-label = "Close"></button>
                            </div>
                            <div class="modal-body">
                                確定要刪除該筆資料？？
                            </div>

                            <div v-if = "error_message != '' " class = "alert alert-danger" role = "alert" style = "margin-top: 10px;">
                                {{ error_message }}
                            </div>

                            <div class="modal-footer">
                                <button class="btn btn-secondary" style = "width: 80px;" data-bs-dismiss = "modal"> 取消 </button>
                                <button class="btn btn-danger" style = "width: 80px;" @click = "delete_product"> 確認 </button>
                            </div>

                        </div>
                    </div>
                </div>

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

#product-management-list{
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 10px;
    padding-bottom: 10px;
    height:auto;
    min-height:600px;
    max-height: 600px;

    border: 1px solid rgb(199,199,199);
    border-radius: 10px;
}

#title_and_create{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
}

.title{
    font-size: 24px;
    font-weight: bolder;
}

.create-btn{
    margin-left: 20px;
    width: 120px;
    height: 40px;
}

.table-btn{
    margin-left: 5px;
    margin-right: 5px;
    width: 100px;
    font-weight: bolder;
    color: rgb(223, 222, 222);
}

.edit-form, .modal-form{
    display:flex;
    flex-direction: row;
    flex-wrap: wrap;

    justify-content: space-around;
    align-content: center;
}

.edit-form-component, .edit-form-component-title, .modal-form-component, .modal-form-component-title{
    display:flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    align-content: center;
}

.edit-form-component-title, .modal-form-component-title{
    width: 100px;
    font-weight: bold;
}


.edit-form-body, .modal-form-body{
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;

    justify-content: space-around;
    width: 100%;
}

.edit-form-row, .modal-form-row{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-between;
    align-content: center;
}

.preview {
  /* background:#888888; */
  
  height:auto;
  text-align:center;
}
.preview img{
  order:1;
  vertical-align : middle;
}

</style>