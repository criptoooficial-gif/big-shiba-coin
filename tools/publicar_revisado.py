from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text(encoding='utf-8')

def swap(old,new):
    global s
    if old in s: s=s.replace(old,new)
    elif new not in s: raise RuntimeError('Trecho ausente: '+old[:90])

swap('120 BSHIBA/dia, por até 10 dias','120 BSHIBA/dia, por até 48 horas')
swap('<small>Período de cálculo</small><b>10 dias</b>','<small>Período de cálculo</small><b>48 horas</b>')
swap('<small>Referência por dia</small><b>R$ 2,50</b>','<small>Referência por dia</small><b>R$ 12,50</b>')
swap('<small>Prazo mínimo para saque</small><b>15 dias</b>','<small>Prazo mínimo para saque</small><b>48 horas</b>')
swap('aria-label="Prazo de referência de 15 dias"','aria-label="Prazo de 48 horas para solicitar saque"')
swap('<span>15 dias</span>','<span>48 horas</span>')
swap('const countDays=10;','const countDays=2;')
swap('const withdrawDays=15;','const withdrawHours=48;')
swap('elapsed/(withdrawDays*day)*100','elapsed/(withdrawHours*3600000)*100')
swap('const remaining=withdrawDays*day-(Date.now()-active.started);','const remaining=withdrawHours*3600000-(Date.now()-active.started);')
swap("toast('Prazo de 15 dias ainda não concluído. O contador é uma estimativa, não um saldo sacável.');","toast('Prazo de 48 horas ainda não concluído. O contador é uma estimativa, não um saldo sacável.');")
swap('Próxima atualização</small><strong id="next-cycle">60:00','Próxima conferência (48h)</small><strong id="next-cycle">48:00:00')
swap("let payments=[],filter='all',nextUpdate=Date.now()+3600000;", """let payments=[],filter='all';
    const HOUR=3600000,PERIOD=48*HOUR;
    const boundary=span=>Math.floor(Date.now()/span)*span+span;
    let nextFetch=boundary(HOUR);""")
swap('nextUpdate=Date.now()+3600000;renderPayments();clock();','renderPayments();clock();')
swap("function clock(){let diff=Math.max(0,nextUpdate-Date.now()),s=Math.ceil(diff/1000);$('next-cycle').textContent=String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');}","""function clock(){const secs=Math.max(0,Math.ceil((boundary(PERIOD)-Date.now())/1000));$('next-cycle').textContent=[Math.floor(secs/3600),Math.floor(secs%3600/60),secs%60].map(n=>String(n).padStart(2,'0')).join(':');}""")
swap("loadPayments();setInterval(()=>{if(Date.now()>=nextUpdate)loadPayments();else clock()},1000);","loadPayments();setInterval(()=>{if(Date.now()>=nextFetch){nextFetch=boundary(HOUR);loadPayments()}clock()},1000);")
swap("const dateText=s=>{const d=new Date(s);return Number.isNaN(d.getTime())?'—':d.toLocaleString('pt-BR',{day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit'});};", """const dateText=s=>{const d=new Date(s);if(!Number.isFinite(d.getTime()))return '—';
      const fmt=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Sao_Paulo',year:'numeric',month:'2-digit',day:'2-digit'});
      const diff=Math.round((Date.parse(fmt.format(new Date())+'T00:00:00Z')-Date.parse(fmt.format(d)+'T00:00:00Z'))/86400000);
      const when=diff===0?'Hoje':diff===1?'Ontem':diff===2?'Há 2 dias':d.toLocaleDateString('pt-BR',{timeZone:'America/Sao_Paulo'});
      return when+' · '+d.toLocaleTimeString('pt-BR',{timeZone:'America/Sao_Paulo',hour:'2-digit',minute:'2-digit'});
    };""")
start=s.index("      if(filter==='all'){",s.index("function renderPayments()"))
end=s.index("    function acceptRecords",start)
s=s[:start]+"""      if(filter==='all'){
        // Display the actual visitor wallet, not invented payment activity.
        const saved=(()=>{try{return JSON.parse(localStorage.getItem('bshiba_wallet_fixa_v1'))}catch{return null}})();
        if(saved && validAddress(saved.address) && Number.isFinite(saved.started) && !payments.some(p=>p.address===saved.address)){
          const amount=Math.min(Math.max(0,Date.now()-saved.started),48*3600000)*120/86400000;
          const tr=document.createElement('tr');tr.className='local-wallet-row';
          const user=document.createElement('td');user.textContent='👤 '+short(saved.address);
          const quantity=document.createElement('td');quantity.className='payout-amount';quantity.textContent=tokenAmount(amount);
          const dt=document.createElement('td');dt.textContent=dateText(new Date(saved.started).toISOString());
          const status=document.createElement('td');status.textContent='Acumulando';status.style.color='#ffc76d';
          tr.append(user,quantity,dt,status);rows.prepend(tr);
        }else if(!list.length){empty('Nenhum pagamento confirmado até agora');}
      }
    }
"""+s[end:]
swap('100 posições para carteiras e histórico de pagamentos.','Histórico de até 100 carteiras e transferências.')
s=s.replace('As 100 posições são reservadas para registros de carteiras. Os status <b>Pago</b> e <b>Pendente</b> aparecem quando houver transferências confirmadas e solicitações reais.','<b>Pago</b> corresponde a transferência confirmada; <b>Pendente</b> a solicitação registrada.')
s=s.replace("O histórico carrega transações informadas pelo serviço de pagamentos. O status <b>Pago</b> depende de transferência confirmada na Solana. O total de hoje é atualizado a partir desses registros.","<b>Pago</b> corresponde a transferência confirmada; <b>Pendente</b> a solicitação registrada.")
for forbidden in ['10 dias','15 dias','withdrawDays','nextUpdate']:
    if forbidden in s: raise RuntimeError('Prazo antigo ainda presente: '+forbidden)
assert s.count('48 horas')>=4
p.write_text(s,encoding='utf-8')
print('48 horas confirmado; historico de carteiras reais ativo')