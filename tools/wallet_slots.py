from pathlib import Path
import sys

path = Path(sys.argv[1])
html = path.read_text(encoding='utf-8')
old_empty = "if(!list.length){empty(filter==='paid'?'Nenhum pagamento confirmado':filter==='pending'?'Nenhuma solicitação pendente':'Nenhum pagamento registrado');return;}"
new_empty = "if(!list.length && filter!=='all'){empty(filter==='paid'?'Nenhum pagamento confirmado':'Nenhuma solicitação pendente');return;}"
if old_empty not in html:
    raise SystemExit('Condição da lista vazia não encontrada.')
html = html.replace(old_empty, new_empty, 1)
old_tail = """        tr.append(user,amount,at,statusCell);rows.append(tr);
      }
    }
    function acceptRecords(records){"""
new_tail = """        tr.append(user,amount,at,statusCell);rows.append(tr);
      }
      if(filter==='all'){
        // Até 100 posições; entradas sem carteira não são transações.
        for(let i=list.length+1;i<=100;i++){
          const tr=document.createElement('tr');
          tr.className='wallet-slot';
          const user=document.createElement('td'),profile=document.createElement('div');
          profile.className='user-line';
          const avatar=document.createElement('span');
          avatar.className='wallet-icon person-icon';avatar.textContent='👤';
          const label=document.createElement('span');
          label.className='pay-address';
          label.textContent='Carteira '+String(i).padStart(3,'0')+' · Aguardando cadastro';
          profile.append(avatar,label);user.append(profile);
          const amount=document.createElement('td');
          amount.className='payout-amount';amount.textContent='—';
          const date=document.createElement('td');
          date.className='payout-time';date.textContent='—';
          const status=document.createElement('td');
          status.textContent='Não registrada';status.style.color='#a9b4c2';
          tr.append(user,amount,date,status);rows.append(tr);
        }
      }
    }
    function acceptRecords(records){"""
if old_tail not in html:
    raise SystemExit('Fim da renderização não encontrado.')
html = html.replace(old_tail, new_tail, 1)
html = html.replace('<p>Pagamentos confirmados e solicitações registradas.</p>', '<p>100 posições para carteiras e histórico de pagamentos.</p>', 1)
html = html.replace('O histórico carrega transações informadas pelo serviço de pagamentos. O status <b>Pago</b> depende de transferência confirmada na Solana. O total de hoje é atualizado a partir desses registros.', 'As 100 posições são reservadas para registros de carteiras. Os status <b>Pago</b> e <b>Pendente</b> aparecem quando houver transferências confirmadas e solicitações reais.', 1)
path.write_text(html, encoding='utf-8')
print('100 posições de carteira instaladas.')
