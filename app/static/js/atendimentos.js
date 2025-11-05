document.addEventListener('DOMContentLoaded', () => {
        const form = document.getElementById('form-atendimento');
        const tbody = document.getElementById('lista-atendimentos');
        const selectCliente = document.getElementById('select-cliente');
        const selectServico = document.getElementById('select-servico');
        
        // Carregar os Dropdowns (Selects) de clientes e serviços
        async function carregarDropdowns() {
            // Clientes
            const respClientes = await fetch('/api/clientes');
            const clientes = await respClientes.json();
            selectCliente.innerHTML = '<option value="">Selecione um cliente</option>';
            clientes.forEach(c => {
                selectCliente.innerHTML += `<option value="${c.id}">${c.nome}</option>`;
            });
            
            // Serviços
            const respServicos = await fetch('/api/servicos');
            const servicos = await respServicos.json();
            selectServico.innerHTML = '<option value="">Selecione um serviço</option>';
            servicos.forEach(s => {
                selectServico.innerHTML += `<option value="${s.id}">${s.descricao}</option>`;
            });
        }
        
        // Carregar a tabela de atendimentos registrados
        async function carregarAtendimentos() {
            const response = await fetch('/api/atendimentos');
            const atendimentos = await response.json();
            
            tbody.innerHTML = '';
            atendimentos.forEach(a => {
                const tr = document.createElement('tr');
                // Formata a data para ficar mais legível (ex: dd/mm/aaaa hh:mm)
                const dataFormatada = new Date(a.data).toLocaleString('pt-BR');
                
                tr.innerHTML = `
                    <td>${a.id}</td>
                    <td>${dataFormatada}</td>
                    <td>${a.cliente_nome}</td>
                    <td>${a.servico_descricao}</td>
                    <td>R$ ${a.servico_valor.toFixed(2)}</td>
                    <td>${a.observacoes || 'N/A'}</td>
                    <td class="actions">
                        <button class="btn-danger btn-sm btn-excluir" data-id="${a.id}">Excluir</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
        
        // Lidar com o registro de um novo atendimento
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const cliente_id = selectCliente.value;
            const servico_id = selectServico.value;
            const observacoes = document.getElementById('observacoes').value;
            
            if (!cliente_id || !servico_id) {
                alert('Por favor, selecione um cliente e um serviço.');
                return;
            }
            
            const response = await fetch('/api/atendimentos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cliente_id, servico_id, observacoes })
            });
            
            if (response.ok) {
                form.reset();
                await carregarAtendimentos();
                alert('Atendimento registrado com sucesso!');
            } else {
                const erro = await response.json();
                alert(`Erro: ${erro.erro}`);
            }
        });
        
        // Lidar com Exclusão de Atendimento
        tbody.addEventListener('click', async (e) => {
            const target = e.target;
            if (target.classList.contains('btn-excluir')) {
                const id = target.dataset.id;
                if (confirm(`Tem certeza que deseja excluir o atendimento ID ${id}?`)) {
                    const response = await fetch(`/api/atendimentos/${id}`, { method: 'DELETE' });
                    if (response.ok) {
                        await carregarAtendimentos();
                        alert('Atendimento excluído.');
                    } else {
                        const erro = await response.json();
                        alert(`Erro: ${erro.erro}`);
                    }
                }
            }
        });

        // Carga inicial
        carregarDropdowns();
        carregarAtendimentos();
    
});