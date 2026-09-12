/* Approved budget assumptions; all state stays inside this block. */
(() => {
const root=document.getElementById('mbga-budget');
if(!root)return;

const $=id=>root.querySelector('#mbga-'+id);const nf=new Intl.NumberFormat('ru-RU',{maximumFractionDigits:2});const rub=n=>nf.format(n)+' ₽';
function update(){const reels=+$('reels').value,price=+$('price').value,funnels=+$('funnels').value,fx=+$('fx').value,website=$('website').checked;const before=reels*price+funnels*20000+20000+(website?50000:0);const valid=Number.isFinite(fx)&&fx>0;const after=valid?200*fx:null;const savings=valid?before-after:null;
$('reels-value').textContent=reels;$('price-value').textContent=rub(price);$('funnels-value').textContent=funnels;$('reels-formula').textContent=reels+' в месяц × '+rub(price);$('funnels-formula').textContent=funnels+' в месяц × 20 000 ₽';$('reels-total').textContent=rub(reels*price);$('funnels-total').textContent=rub(funnels*20000);$('site-status').textContent=website?'Разово · включён в первый месяц':'Разово · сейчас не включён';$('before-period').textContent=website?'Итого за первый месяц':'Итого в месяц';$('before-total').textContent=rub(before);$('after-total').textContent=valid?rub(after):'—';$('conversion').textContent=valid?'200 € × '+nf.format(fx)+' ₽':'200 € · укажите курс';$('savings').textContent=valid?rub(savings):'—';$('fxerror').hidden=valid;$('fx').setAttribute('aria-invalid',String(!valid));$('savings-caption').textContent=valid?(savings<0?'После дороже · ':'Расчётная экономия · ')+(website?'за первый месяц':'за месяц')+' · до минус после':'Укажите условный курс для расчёта';}
['reels','price','funnels','fx','website'].forEach(id=>$(id).addEventListener('input',update));update();

})();
