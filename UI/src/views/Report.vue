<script setup lang = "ts">
import Chart from "chart.js/auto";
import { onMounted, ref } from "vue";

import {getSelling} from '@/composables/selling';


export interface SellingData{
  record_id:string,
  id:string,
  name:string,
  platformer:string,
  production_used:string,
  type:string,
  purchase_price:number,
  real_selling_price:number,
  sell_count:number,
  income:number,
  data_time:string,
}

export interface DetailData{
  name:string,
  platformer:string,
  type:string,
  sell_count:number,
  one_purchase:number,
  one_sell:number,
  total_income:number,
}

const selling_data = ref<SellingData[]|null>([]);


let plot_bar_chart_data = {}
let plot_pie_chart_data = {}

let bar_chart:any = null;
let pie_chart:any = null;

const expenses = ref<number>(0);
const real_sell = ref<number>(0);

const start_date = ref<string>("");
const end_date = ref<string>("");

const detail_list = ref<DetailData[]>([]);
const detail_date = ref<string>("");

const table_heads = ["#", "商品名稱", "平台", "類型", "數量",  '單片進價', "實際售價" , "淨利"]

/* ------------------- Methods ------------------------ */

const set_initial_datetime = ()=>{
  let now = new Date();
  //const timestamp = Date.now()

  const priorDate = new Date(new Date().setDate(now.getDate() - 30));
  const nextDate = new Date(new Date().setDate(now.getDate() + 1));

  start_date.value = priorDate.toISOString().slice(0, 10);
  end_date.value = nextDate.toISOString().slice(0, 10);

}

const search = ()=>{
  load_db_data(start_date.value, end_date.value);
}

async function load_db_data(start_date:string, end_date:string){
  // @ts-ignore
  const {selling, message, error} =  await getSelling(start_date, end_date);
  selling_data.value = selling.value;

  update_bar_chart_data()
  plot_bar_chart()
  plot_pie_chart()
}


const update_bar_chart_data = ()=>{
  let label_list:any = [];
  let income_data:any = [];

  expenses.value = 0;
  real_sell.value = 0;

  for(let i = 0;i < selling_data.value!.length;i++){
    let insert_index = -1;

    if (label_list.includes(selling_data.value![i].data_time) == false){
      label_list.push(selling_data.value![i].data_time);
      income_data.push(selling_data.value![i].income);
    }
    else{
      insert_index = label_list.indexOf(selling_data.value![i].data_time);
      income_data[insert_index] += selling_data.value![i].income;
    }

    expenses.value += selling_data.value![i].purchase_price * selling_data.value![i].sell_count;
    real_sell.value += selling_data.value![i].real_selling_price * selling_data.value![i].sell_count;
  }

  plot_bar_chart_data = {
    labels:label_list,
    datasets: [
      // 物件的屬性有 label 與 data
      {
        // label 為資料分類的名稱
        label: "淨利",
        //  data 為資料內容，是一個陣列，相同 index 的數值會放在同一個橫軸的分類區間
        data: income_data,
      },
    ],
  }

  plot_pie_chart_data = {
    labels:['支出', '收入'],
    datasets:[{
      label:'Profit',
      data:[expenses.value, real_sell.value],
      backgroundColor:[
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)'
      ]
    }]
  }

}

const show_history_record = (e:any, chart:any)=>{
  
  const activePoints = chart.getElementsAtEventForMode(e, 'nearest', {
    intersect: true
  }, false);

  if (activePoints.length > 0) {
    const index = activePoints[0].index;
    detail_date.value = chart.data.labels[index];

    let product_id:any = []
    let product_name:any = [];
    let selling_count:any = [];
    let product_type:any = [];
    let product_plat:any = [];
    let product_purchase:any = [];
    let product_sell:any = [];
    let product_income:any = [];

    for(let i = 0;i < selling_data.value!.length ; i++){
      if(selling_data.value![i].data_time == detail_date.value){
        let insert_index = -1;
        if (product_id.includes(selling_data.value![i].id) == false){
          product_id.push(selling_data.value![i].id)

          product_name.push(selling_data.value![i].name);
          product_type.push(selling_data.value![i].type)
          selling_count.push(selling_data.value![i].sell_count);
          product_plat.push(selling_data.value![i].platformer);
          product_purchase.push(selling_data.value![i].purchase_price);
          product_sell.push(selling_data.value![i].real_selling_price);
          product_income.push((selling_data.value![i].real_selling_price - selling_data.value![i].purchase_price) * selling_data.value![i].sell_count);

        } 

        else{
          insert_index = product_id.indexOf(selling_data.value![i].id);
          selling_count[insert_index] += selling_data.value![i].sell_count;
        }
      }
    }

    detail_list.value.length = 0;

    for(let i = 0 ; i < product_name.length;i++){
      detail_list.value.push({
        name:product_name[i],
        platformer:product_plat[i], 
        type:product_type[i],
        sell_count:selling_count[i],
        one_purchase:product_purchase[i],
        one_sell:product_sell[i],
        total_income:product_income[i]
      });
    }
  }

}


const plot_bar_chart = ()=> {
  const ctx = document.getElementById("SellingChart");

  if (bar_chart){
    bar_chart.destroy();
  }
  // @ts-ignore
  bar_chart = new Chart(ctx, {
    // type 可以是 bar，也可以是 line
    type: "bar",
    data: plot_bar_chart_data,
    options: {
      responsive: true,
      // 如果不設 maintainAspectRatio,寬度會固定
      maintainAspectRatio: false,
      plugins: {
        legend: {
          // datasets裡每一個物件會變成圖例，出現在給定的位置
          position: "top",
        },
        title: {
          display: true,
          text: "勝光淨利",
        },
      },
      onClick:(e) =>{
        show_history_record(e, bar_chart);
      }
    },
  });
}

const plot_pie_chart = ()=> {
  const ctx = document.getElementById("ProfitChart");
  if (pie_chart){
    pie_chart.destroy();
  }
  // @ts-ignore
  pie_chart = new Chart(ctx, {
    type: "pie",
    data: plot_pie_chart_data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "收入 / 支出",
        },
      },
    },
  });
}

onMounted(async () => {
  set_initial_datetime();
  await load_db_data(start_date.value, end_date.value)
});

</script>

<template>
    <div id = "view_body">
        <div id = "select-data-time">
            <div class = "select-date">
                <label class = "select-label">
                    開始時間：
                </label>
                <input class = "form-control input-date" type="date" v-model = "start_date"/>
            </div>

            <div class = "select-date">
                <label class = "select-label">
                    結束時間：
                </label>
                <input class = "form-control input-date" type="date" v-model = "end_date"/>
            </div>

            <div style = "margin-left: 30px;">
                <button type = "button" class = "btn btn-primary" style = "width: 100px; height: 40px;" @click = "search">
                    搜尋
                </button>
            </div>
           
        </div>

        <div class="shadow p-3 mb-5 bg-body rounded" style = "height: 500px; width: 90%;">
          <canvas id = "SellingChart" ></canvas>
        </div>

        <div class="shadow p-3 mb-5 bg-body rounded" style = "height: 500px; width: 90%;" v-if ="detail_date != ''">
          <div style = "display: flex; flex-direction: column; width: 100%;">
            <label class = "profit-datetime-label"> {{ detail_date }} 銷售紀錄 </label>
            <hr style = "border: 1px solid grey;">
            
             <div class = "product-table-sticky-wrapper">
                <table class = "table table-hover">
                    <thead class = "product-table-thead">
                        <tr>
                            <th  class = "text-center" scope="col" v-for = "head_item in table_heads" style="font-weight: bolder; background-color: rgb(120,180,200);"> {{head_item}} </th>
                        </tr>
                    </thead>
                
                    <tbody class = "product-table-tbody">
                        <tr v-for = "(item, index) in detail_list" style = "height: 40px;" >
                            <td class = "align-middle text-center" scope = "row"> {{index + 1}} </td>
                            <td class = "align-middle text-center" style = "width: 30%;"> {{item.name}} </td>
                            <td class = "align-middle text-center" style = "width: 10%;"> {{item.platformer}} </td>
                            <td class = "align-middle text-center" style = "width: 10%;"> {{item.type}} </td>
                            <td class = "align-middle text-center" style = "width: 8%;"> {{item.sell_count}} </td>
                            <td class = "align-middle text-center" style = "width: 10%;"> {{item.one_purchase}} </td>
                            <td class = "align-middle text-center" style = "width: 10%;"> {{item.one_sell}} </td>
                            <td class = "align-middle text-center" style = "width: 10%;"> {{item.total_income}} </td>
                        </tr>
                    
                    </tbody>
                
                </table>    
            </div>
          </div>
        </div>

        <div class="shadow p-3 mb-5 bg-body rounded" style = "height: 450px; width: 90%;">
          <div style = "height: 400px; display: flex; flex-direction: row; width: 100%;">
            
            <div style = "width: 50%;">
              <canvas id = "ProfitChart"></canvas>
            </div>
            
            <div style = "width: 50%;">
              <div>
                <label class = "profit-datetime-label"> 數據明細： </label>
              </div>
              
              <hr style = "border: 1px solid grey;">

              <div style = "margin-top: 10px;">
                <label class = "profit-label" > 計算期間：</label>
                <span style = "font-weight: bolder; font-size: 20px;"> {{ start_date }} ~ {{ end_date }} </span>
              </div>

              <div style = "margin-top: 10px;">
                <label class = "profit-label" > 期間收入：</label>
                <span style = "color: green; font-weight: bolder; font-size: 20px;"> $ {{ real_sell }} </span>
              </div>

              <div style = "margin-top: 10px;">
                <label class = "profit-label" > 期間支出：</label>
                <span style = "color: red; font-weight: bolder; font-size: 20px;"> $ {{ expenses }} </span>
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
    width: 100%;
}

#select-data-time{
    display: flex;
    flex-direction: row;

    margin-bottom: 20px;
    width: 90%;
}

.select-date{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
}

.select-label{
  width: 120px;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-content: end;
  justify-content: center;
  margin-right: 5px;
}

.input-date{
    width: 200px;
}

#SellingChart{
    height:400px;
    width: auto;
    min-width: 600px;
    /* max-width: 80%; */
}

.profit-datetime-label{
  font-size: 24px;
  font-weight: bolder;
}

.profit-label{
  font-size: 20px;
  font-weight: bolder;
}

.product-table-sticky-wrapper{
    width: 100%;
    height: 400px;
    overflow: auto;
}

.product-table-tbody{
    position: relative;
    z-index: 0;
    height: auto;
    width: 100%;
    overflow: hidden;
}

table thead th{
    position: sticky;
    z-index: 1;
    top:0px;
}

tbody td{
    z-index: 0;
}

</style>