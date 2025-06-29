<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';

import SearchForm from '@/components/SearchForm.vue'
//@ts-ignore
import {getProducts} from '@/composables/products';


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

const product_data = ref<Product[]|null>([]);

const show_data = ref<any[]|null>([]);

const api_message = ref<string>("");

const now_page_number = ref<number>(1);
const total_page_number = ref<number>(0);
const show_number = ref<number>(5);


async function load_db_data(){
  const {products, message, error} =  await getProducts();
  product_data.value = products.value;
  api_message.value = message.value;
  console.log(error)
}

const page_update = (update_number:number)=>{
    now_page_number.value += update_number;
}

const get_db_data = async ()=>{
  await load_db_data();
  show_data.value = [...product_data.value!];
  update_show_data();
}

const get_image_path = (img_name:string)=>{
  let path = `http://127.0.0.1:8000/products/get-image/${img_name}`
  return path
}

const update_show_data = () => {
  total_page_number.value = Math.ceil(show_data.value!.length / show_number.value);
  now_page_number.value = 1;
}

const search_data = (data:any) => {
  console.log(data)
  let type_index = search_data_type(data.type);
  let platformer_index = search_data_platformer(data.platformer);
  let count_index = search_data_count(data.product_exist);
  let name_index = search_data_name(data.name);
  console.log(type_index, platformer_index, count_index, name_index)
  show_data.value!.length = 0;

  for(let i = 0; i < product_data.value!.length;i++){
    if(type_index.includes(i) && platformer_index.includes(i) && count_index.includes(i) && name_index.includes(i)){
      show_data.value?.push(product_data.value![i])
    }
  }

  update_show_data()
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

onMounted(()=>{
  get_db_data()
})

</script>

<template>

  <div style = "display: flex; flex-direction: row; flex-wrap: wrap; justify-content: center;">
    <div style = "width: 90%;">
      
      <SearchForm @search = "search_data"></SearchForm>

      <hr style = "border: 1px solid;">

      <div id = "page_and_title">
        <label class = "title"> 所有商品 </label>

        <nav aria-label="Page navigation example">
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
      
      <div id = "game_production_list" >
        <div  v-for = "item in table_list" :key = "item.id" style = "width: 20%; min-width: 300px; display: flex; flex-direction: column; flex-wrap: wrap; align-items: center;">
          <div class = "card game_card" style = "width: 240px; display: flex; flex-direction: column; flex-wrap: wrap; justify-content: center;align-content: center;">
            <div style = "width: 220px; height:250px; display: flex; flex-direction: column; flex-wrap: wrap; justify-content: center;align-content: center; " >
              <img v-if = "item.img_path != '' " :src = "get_image_path(item.img_path)" class="card-img-top" alt="..." style="width: 180px;" >
              <img v-else src = "../../public/game.png" style="width: 180px;" >
            </div>
            <hr>
            <div class = "production-card-body">
              <div style = "display: flex; flex-direction: column; padding-left: 10px;">
                <label style = "font-size: 18px;font-weight:bold"> 
                  {{ item.name }}
                </label>
                <label style = "color: red; font-weight:bold"> 
                    ${{ item.selling_price }} 
                </label>
              </div>
          
              <div style = "display: flex; flex-direction: row; justify-content: space-around;">
                <div>
                  <span class="badge bg-primary game-badge" v-if = "item.platformer == 'PS5'"> {{item.platformer}} </span>
                  <span class="badge bg-primary game-badge" v-else-if = "item.platformer == 'PS4'"> {{item.platformer}} </span>
                  <span class="badge bg-danger game-badge" v-else-if = "item.platformer == 'Switch'"> {{item.platformer}} </span>
                  <span class="badge bg-info game-badge"> {{item.type}} </span>
                </div>
                <label style = "font-weight: bolder;"> 庫存：{{ item.count }}</label>
              </div>

            </div>
          </div>
        </div>
      </div>

    </div>
  </div>

  
</template>

<style>

#page_and_title{
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;

  justify-content: space-between;
}

#select_search{
  margin-bottom: 5px;

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;

  justify-content: space-between;
  align-content: center;
  align-items: center;
}

.title{
  font-size: 24px;
  font-weight: bolder;
}

.selection, .input-keyword{
  display: flex;
  flex-direction: row;
  margin-top: 5px;
  margin-bottom: 5px;
}

.select_label{
  width: 120px;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-content: end;
  justify-content: center;
  margin-right: 5px;
}

.search-select{
  width: 200px;
}

.keyword-input-control{
  width: 300px;
}

#game_production_list{
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;

  /* align-items; */

  border: 4px solid rgb(199, 199, 199);
  border-radius: 10px;
  min-height:600px;
  height: auto;
} 

.game-badge{
  margin-right: 10px;
  width: 60px;
}
/* 
@media (max-width: 1024px) {
  #game_production_list{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-column-gap: 10px;
    grid-row-gap: 1em;
  }
} */

.game_card{
  margin-top: 20px;
  margin-bottom: 20px;
  margin-left: 20px;
  margin-right: 20px;
}

.production-card-body{
  padding-left: 5px;
  padding-right: 5px;
  padding-bottom: 10px;
}
</style>