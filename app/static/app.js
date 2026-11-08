const API="/api/ships";
const labels={sailing:"航行中",moored:"停泊",maintenance:"维修中",offline:"离线"};
const types={cargo:"货船",tanker:"油轮",passenger:"客船",fishing:"渔船",patrol:"公务船",other:"其他"};
const rows=document.querySelector("#rows"), message=document.querySelector("#message"), dialog=document.querySelector("#dialog"), form=document.querySelector("#ship-form");
let ships=[], editingId=null;
async function load(){
  // TODO: send keyword and status filters to the API
  try{
    const response=await fetch(API);
    if(!response.ok) throw new Error("加载失败："+response.status);
    ships=await response.json(); render(); message.textContent="共 "+ships.length+" 条记录";
  }catch(error){message.textContent=error.message;message.style.color="crimson";}
}
function render(){
  document.querySelector("#total").textContent=ships.length;
  document.querySelector("#sailing").textContent=ships.filter(x=>x.status==="sailing").length;
  document.querySelector("#moored").textContent=ships.filter(x=>x.status==="moored").length;
  document.querySelector("#attention").textContent=ships.filter(x=>["maintenance","offline"].includes(x.status)).length;
  rows.innerHTML=ships.length?ships.map(x=>`<tr><td>${safe(x.name)}</td><td>${safe(x.mmsi)}</td><td>${types[x.ship_type]||safe(x.ship_type)}</td><td>${labels[x.status]||safe(x.status)}</td><td>${safe(x.owner||"—")}</td><td><button class="edit" data-id="${x.id}">编辑</button></td></tr>`).join(""):'<tr><td colspan="6">没有找到符合条件的船舶</td></tr>';
}
function safe(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
document.querySelector("#filters").addEventListener("submit",e=>{e.preventDefault();load();});
document.querySelector("#filters").addEventListener("reset",()=>setTimeout(load,0));
document.querySelector("#add").addEventListener("click",()=>{editingId=null;form.reset();document.querySelector("#form-title").textContent="新增船舶";dialog.showModal();});
document.querySelector("#cancel").addEventListener("click",()=>dialog.close());
rows.addEventListener("click",e=>{const b=e.target.closest("[data-id]");if(!b)return;const x=ships.find(s=>s.id===Number(b.dataset.id));if(!x)return;editingId=x.id;for(const k of ["name","mmsi","ship_type","status","owner"])form.elements[k].value=x[k]||"";document.querySelector("#form-title").textContent="编辑船舶";dialog.showModal();});
form.addEventListener("submit",async e=>{
  e.preventDefault();
  // TODO: submit POST for create and PUT for edit; show API validation errors
  message.textContent="新增和编辑功能尚未实现";
});
load();
