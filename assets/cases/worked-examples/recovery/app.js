const $=s=>document.querySelector(s);
const items=[{key:'a',id:'EQ-81',name:'三脚架'},{key:'b',id:'EQ-82',name:'领夹话筒'},{key:'c',id:'EQ-83',name:'防风罩'}].map(x=>({...x,status:'idle',qty:null,message:'',max:null,requestId:null}));
let busy=false,checking=false,attempted=false,contactError='',notice='';
function draft(item){const v=$('#qty-'+item.key).value.trim();return /^\d+$/.test(v)?Number(v):NaN}
function problem(item){const n=draft(item);if(!Number.isSafeInteger(n)||n<1)return '件数须为正整数';if(item.max&&n>item.max)return `当前最多可领${item.max}件`;return ''}
function current(item){if(['done','pending','unknown'].includes(item.status))return item.status;return problem(item)?'invalid':item.status==='invalid'?'ready':'idle'}
function render(){
 const states=items.map(current),done=states.filter(x=>x==='done').length,pending=states.filter(x=>x==='pending'||x==='unknown').length;
 const candidates=items.filter(x=>['idle','ready'].includes(current(x))),errors=[];
 for(const item of items){const s=current(item),input=$('#qty-'+item.key),error=problem(item);$('#row-'+item.key).dataset.state=s;input.readOnly=busy||['done','pending','unknown'].includes(s);const active=s==='invalid'&&(attempted||item.status==='invalid');input.setAttribute('aria-invalid',String(active));
  let label='待提交',note='';
  if(s==='done'){label='已接纳';note=`已确认 ${item.qty} 件`}
  else if(s==='pending'){label='待核实';note='申请已发送，请核实接纳结果'}
  else if(s==='unknown'){label='结果未知';note='请保留本页，勿重复提交；需核实原请求'}
  else if(active){label='需修改';note=error;errors.push({key:item.key,text:item.name+'：'+error})}
  else if(s==='ready'){label='已修改 · 待补交';note=`当前草稿 ${draft(item)} 件，尚未接纳`}
  $('#state-'+item.key).textContent=label;$('#note-'+item.key).textContent=note;
 }
 $('#contact').readOnly=busy||attempted;$('#phone').readOnly=busy||attempted;
 $('#error').replaceChildren();if(contactError){$('#error').textContent=contactError}else if(errors.length){const title=document.createElement('strong');title.textContent='请修正以下数量';$('#error').append(title);for(const e of errors){const line=document.createElement('div'),a=document.createElement('a');a.href='#qty-'+e.key;a.textContent=e.text;a.onclick=event=>{event.preventDefault();$('#qty-'+e.key).focus()};line.append(a);$('#error').append(line)}}
 const complete=done===items.length;$('#editing').hidden=complete;$('#recovery').hidden=complete;$('#receipt').hidden=!complete;
 $('#submit').hidden=complete||(!candidates.length&&!errors.length&&attempted);$('#submit').disabled=busy||checking||!candidates.length||errors.length>0;
 $('#submit').textContent=busy?'正在提交…':errors.length?'请先修改领用数量':!attempted?'提交领用申请':candidates.length===1?`补交${candidates[0].name}（${draft(candidates[0])}件）`:`补交 ${candidates.length} 种器材`;
 const verifiable=items.filter(x=>x.status==='pending'&&x.requestId);$('#verify').hidden=!verifiable.length;$('#verify').disabled=busy||checking;$('#verify').textContent=checking?'正在核实…':'核实防风罩结果';
 $('#verify-note').textContent=verifiable.length?`请求 ${verifiable.map(x=>x.requestId).join('、')} · 先查单，不重复提交` : '';
 if(!attempted){$('#result').textContent='数量将以实际接纳结果为准。'}else{const parts=[`${done} 种已接纳`];if(errors.length)parts.push(`${errors.length} 种需修改`);if(candidates.length)parts.push(`${candidates.length} 种待补交`);if(pending)parts.push(`${pending} 种待核实`);$('#result').textContent=(notice?notice+' ':'')+parts.join(' · ')}
 if(complete){$('#intro-copy').textContent='本次领用结果已确认，请保存以下回执。';$('#receipt-contact').textContent=`${$('#contact').value} · ${$('#phone').value}`;$('#receipt-items').replaceChildren();for(const item of items){const li=document.createElement('li'),name=document.createElement('div'),id=document.createElement('span'),qty=document.createElement('strong');name.textContent=item.name;id.textContent=item.id;name.append(id);qty.textContent=item.qty+' 件';li.append(name,qty);$('#receipt-items').append(li)}}
}
for(const item of items)$('#qty-'+item.key).addEventListener('input',()=>{notice='';render()});
$('#delivery').addEventListener('submit',async e=>{e.preventDefault();if(busy||checking)return;contactError='';notice='';
 if(!$('#contact').value.trim()||!$('#phone').value.trim()){contactError='请填写领用人和联系电话。';render();(!$('#contact').value.trim()?$('#contact'):$('#phone')).focus();return}
 const invalid=items.filter(x=>!['done','pending','unknown'].includes(x.status)&&problem(x));if(invalid.length){attempted=true;render();$('#qty-'+invalid[0].key).focus();return}
 const sent=items.filter(x=>['idle','ready'].includes(current(x))).map(x=>({item:x,qty:draft(x)}));if(!sent.length)return;
 busy=true;attempted=true;render();
 try{const response=await fetch('/api/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({contact:$('#contact').value.trim(),phone:$('#phone').value.trim(),items:sent.map(x=>({id:x.item.id,qty:x.qty}))})});if(!response.ok)throw Error('提交响应异常');const data=await response.json();
 for(const {item,qty}of sent){const r=(data.items||[]).find(x=>x.id===item.id);if(!r){item.status='unknown';continue}item.status=r.status==='done'?'done':r.status==='pending'?'pending':r.status==='invalid'?'invalid':'unknown';item.qty=r.qty??qty;item.message=r.message||'';item.max=r.max??item.max;item.requestId=r.requestId||null}
 }catch{for(const {item,qty}of sent){item.status='unknown';item.qty=qty}notice='提交连接中断，接纳结果尚未确认。'}finally{busy=false;render();const error=items.find(x=>current(x)==='invalid');if(error)$('#qty-'+error.key).focus();else if(items.every(x=>x.status==='done'))$('#receipt').focus()}
});
$('#verify').addEventListener('click',async()=>{if(busy||checking)return;const pending=items.filter(x=>x.status==='pending'&&x.requestId);if(!pending.length)return;checking=true;notice='';render();try{for(const item of pending){const response=await fetch('/api/requests/'+encodeURIComponent(item.requestId));if(!response.ok)throw Error('查单失败');const data=await response.json(),r=(data.items||[]).find(x=>x.id===item.id);if(data.status==='done'&&r?.status==='done'){item.status='done';item.qty=r.qty;item.requestId=null}else notice='尚未确认，请稍后继续核实。'}}catch{notice='查单暂不可用，原请求仍待核实。'}finally{checking=false;render();if(items.every(x=>x.status==='done'))$('#receipt').focus();else if(items.some(x=>current(x)==='ready'))$('#submit').focus()}});
render();
