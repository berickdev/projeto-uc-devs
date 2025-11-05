document.addEventListener('DOMContentLoaded', () => {
        const form = document.getElementById('form-servico');
        const tbody = document.getElementById('lista-servicos');
        
        // Função para carregar e exibir serviços
        async function carregarServicos() {
            const response = await fetch('/api/servicos');
            const servicos = await response.json();
            
            tbody.innerHTML = '';
            servicos.forEach(servico => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${servico.id}</td>
                    <td>${servico.descricao}</td>
                    <td>R$ ${servico.valor.toFixed(2)}</td>
                    <td class="actions">
                        <button class="btn-warning btn-sm btn-editar" data-id="${servico.id}">Editar</button>
                        <button class="btn-danger btn-sm btn-excluir" data-id="${servico.id}">Excluir</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
        
        // Lidar com o envio do formulário (Criar/Atualizar)
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const id = document.getElementById('servico-id').value;
            const descricao = document.getElementById('descricao').value;
            const valor = document.getElementById('valor').value;
            
            const url = id ? `/api/servicos/${id}` : '/api/servicos';
            const method = id ? 'PUT' : 'POST';
            
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ descricao, valor })
            });
            
            if (response.ok) {
                form.reset();
                document.getElementById('servico-id').value = '';
                await carregarServicos();
                alert(id ? 'Serviço atualizado!' : 'Serviço criado!');
            } else {
                const erro = await response.json();
                alert(`Erro: ${erro.erro}`);
            }
        });
        
        // Lidar com cliques (Editar/Excluir)
        tbody.addEventListener('click', async (e) => {
            const target = e.target;
            
            if (target.classList.contains('btn-excluir')) {
                const id = target.dataset.id;
                if (confirm(`Tem certeza que deseja excluir o serviço ID ${id}?`)) {
                    const response = await fetch(`/api/servicos/${id}`, { method: 'DELETE' });
                    if (response.ok) {
                        await carregarServicos();
                        alert('Serviço excluído.');
                    } else {
                        const erro = await response.json();
                        alert(`Erro: ${erro.erro}`);
                    }
                }
            }
            
            if (target.classList.contains('btn-editar')) {
                const id = target.dataset.id;
                const response = await fetch(`/api/servicos/${id}`); // GET não implementamos, vamos buscar direto
                
                // Simulação (idealmente teríamos um GET /api/servicos/<id>)
                // Vamos pegar os dados da tabela
                const tr = target.closest('tr');
                const descricao = tr.cells[1].innerText;
                const valor = tr.cells[2].innerText.replace('R$ ', '');
                
                document.getElementById('servico-id').value = id;
                document.getElementById('descricao').value = descricao;
                document.getElementById('valor').value = valor;
                
                window.scrollTo(0, 0);
                form.querySelector('input[name="descricao"]').focus();
            }
        });

        // Carga inicial
        carregarServicos();
    
});