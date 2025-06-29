
<script lang = "ts" setup>
import 'bootstrap';
import {ref} from "vue";

//const props = defineProps(['foo'])

export interface SearchData{
  name?:string,
  platformer?:string,
  type?:string,
  product_exist?:string,
}

const SearchData = ref<SearchData>({
    name:"",
    platformer:"",
    type:"",
    product_exist:""
})

const emit = defineEmits<{
  (e: 'search', searh_data:SearchData): void
}>()

const saerchData = ()=>{
    emit('search', SearchData.value);
}

</script>

<template>
    <div id = "select_search">

        <div class = "selection">
            <label class = "select_label">
                平台種類：
            </label>
            <select class="form-select search-select" aria-label="Default select example" v-model = "SearchData.platformer">
                <option> </option>
                <option> PS4 </option>
                <option> PS5 </option>
                <option> Switch </option>
                <option> Switch2 </option>
                <option> PC </option>
                <option> 其它 </option>
            </select>
        </div>

        <div class = "selection">
            <label class = "select_label">
                品項種類：
            </label>
            <select class="form-select search-select" aria-label="Default select example" v-model = "SearchData.type">
                <option> </option>
                <option> 遊戲 </option>
                <option> 配件 </option>
                <option> 其它 </option>
            </select>
        </div>

        <div class = "selection">
            <label class = "select_label">
                庫存過濾：
            </label>
            <select class="form-select search-select" aria-label="Default select example" v-model = "SearchData.product_exist">
                <option> </option>
                <option> 有庫存 </option>
            </select>
        </div>

        <div class = "input-keyword">
            <label class = "select_label">
                關鍵字：
            </label>
            <input class="form-control keyword-input-control" id = "exampleFormControlInput1" placeholder = "瑪利歐" v-model="SearchData.name">
        </div>

        <button type = "button" class = "btn btn-primary" style = "width: 100px; height: 40px;" @click="saerchData">
            搜尋
        </button>

    </div>
</template>

<style>
#select_search{
  margin-bottom: 5px;

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;

  justify-content: space-between;
  align-content: center;
  align-items: center;
}

.selection, .input-keyword{
  display: flex;
  flex-direction: row;
  margin-top: 5px;
  margin-bottom: 5px;
}

.selection{
    width: 320px;
}

.select_label{
  width: 180px;
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
</style>