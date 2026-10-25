from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text(encoding='utf-8')
def r(a,b):
    global s
    n=s.count(a)
    if n!=1: raise RuntimeError(f'Esperado um trecho, encontrados {n}: {a[:80]}')
    s=s.replace(a,b,1)

r('<b>15 dias</b>','<b>48 horas</b>')
r('aria-label="Prazo de referência de 15 dias"','aria-label="Prazo de 48 horas para solicitar saque"')
r('<span>15 dias</span></div></div>','<span>48 horas</span></div></div>')
r('const withdrawDays=15;','const withdrawHours=48;')
r('elapsed/(withdrawDays*day)*100','elapsed/(withdrawHours*3600000)*100')
r('const remaining=withdrawDays*day-(Date.now()-active.started);','const remaining=withdrawHours*3600000-(Date.now()-active.started);')
r("toast('Prazo de 15 dias ainda não concluído. O contador é uma estimativa, não um saldo sacável.');","toast('Prazo de 48 horas ainda não concluído. A liberação depende de recompensas e pagamentos reais.');")
r('Próxima atualização</small><strong id="next-cycle">60:00','Próxima conferência (48h)</small><strong id="next-cycle">48:00:00')
r("let payments=[],filter='all',nextUpdate=Date.now()+3600000;", """let payments=[],filter='all';
    const HOUR=3600000, CYCLE=48*HOUR;
    // Clock follows a fixed 48-hour boundary, unaffected by manual refresh.
    const nextBoundary=length=>Math.floor(Date.now()/length)*length+length;
    let nextFetch=nextBoundary(HOUR);""")
r("const dateText=s=>{const d=new Date(s);return Number.isNaN(d.getTime())?'—':d.toLocaleString('pt-BR',{day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit'});};", """const dayStamp=d=>new Intl.DateTimeFormat('sv-SE',{timeZone:'America/Sao_Paulo',year:'numeric',month:'2-digit',day:'2-digit'}).format(d);
    const dateText=s=>{
      const d=new Date(s);if(Number.isNaN(d.getTime()))return 'Data indisponível';
      const now=dayStamp(new Date()),stamp=dayStamp(d);
      const delta=Math.round((Date.parse(now+'T00:00:00Z')-Date.parse(stamp+'T00:00:00Z'))/86400000);
      const time=d.toLocaleTimeString('pt-BR',{timeZone:'America/Sao_Paulo',hour:'2-digit',minute:'2-digit'});
      return (delta===0?'Hoje':delta===1?'Ontem':delta===2?'Há 2 dias':d.toLocaleDateString('pt-BR',{timeZone:'America/Sao_Paulo'}))+' · '+time;
    };""")
r("amount.className='payout-amount';amount.textContent='—';","amount.className='payout-amount';amount.textContent='0 BSHIBA';")
r("date.className='payout-time';date.textContent='—';","date.className='payout-time';date.textContent='Aguardando registro';")
r("nextUpdate=Date.now()+3600000;renderPayments();clock();","renderPayments();clock();")
r("function clock(){let diff=Math.max(0,nextUpdate-Date.now()),s=Math.ceil(diff/1000);$('next-cycle').textContent=String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');}", """function clock(){
      const remaining=nextBoundary(CYCLE)-Date.now();
      const secs=Math.max(0,Math.ceil(remaining/1000));
      $('next-cycle').textContent=[Math.floor(secs/3600),Math.floor((secs%3600)/60),secs%60].map(n=>String(n).padStart(2,'0')).join(':');
    }""")
r("loadPayments();setInterval(()=>{if(Date.now()>=nextUpdate)loadPayments();else clock()},1000);", """loadPayments();setInterval(()=>{
      if(Date.now()>=nextFetch){nextFetch=nextBoundary(HOUR);loadPayments();}
      clock();
    },1000);""")
r('100 posições para carteiras e histórico de pagamentos.', 'Até 100 carteiras no histórico. Novas transferências são exibidas quando registradas.')
r('As 100 posições são reservadas para registros de carteiras. Os status <b>Pago</b> e <b>Pendente</b> aparecem quando houver transferências confirmadas e solicitações reais.', 'O histórico é conferido a cada hora, com ciclos de 48 horas. <b>Pago</b> indica transferência confirmada na Solana; <b>Pendente</b> indica solicitação registrada. Posições sem cadastro não representam pagamentos.')
p.write_text(s,encoding='utf-8')
print('Atualizada contagem de 48h, relógio permanente e datas.')
