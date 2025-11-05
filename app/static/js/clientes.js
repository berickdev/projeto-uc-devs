document.addEventListener('DOMContentLoaded', () => {
    
        const form = document.getElementById('form-cliente');
        const tbody = document.getElementById('lista-clientes');
        
        // Função para carregar e exibir clientes na tabela
        async function carregarClientes() {
            // 1. Faz a requisição GET para nossa API
            const response = await fetch('/api/clientes');
            const clientes = await response.json();
            
            // 2. Limpa a tabela
            tbody.innerHTML = '';
            
            // 3. Manipula o DOM: Adiciona cada cliente na tabela
            clientes.forEach(cliente => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${cliente.id}</td>
                    <td>${cliente.nome}</td>
                    <td>${cliente.email}</td>
                    <td>${cliente.telefone || 'N/A'}</td>
                    <td class="actions">
                        <button class="btn-warning btn-sm btn-editar" data-id="${cliente.id}">Editar</button>
                        <button class="btn-danger btn-sm btn-excluir" data-id="${cliente.id}">Excluir</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
        
        // Lidar com o envio do formulário (Criar ou Atualizar)
        form.addEventListener('submit', async (e) => {
            e.preventDefault(); // Impede o recarregamento da página
            
            const id = document.getElementById('cliente-id').value;
            const nome = document.getElementById('nome').value;
            const email = document.getElementById('email').value;
            const telefone = document.getElementById('telefone').value;
            
            const url = id ? `/api/clientes/${id}` : '/api/clientes';
            const method = id ? 'PUT' : 'POST';
            
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nome, email, telefone })
            });
            
            if (response.ok) {
                form.reset(); // Limpa o formulário
                document.getElementById('cliente-id').value = ''; // Limpa o ID oculto
                await carregarClientes(); // Recarrega a tabela
                alert(id ? 'Cliente atualizado!' : 'Cliente criado!');
            } else {
                const erro = await response.json();
                alert(`Erro: ${erro.erro}`);
            }
        });
        
        // Lidar com cliques nos botões Editar e Excluir (Event Delegation)
        tbody.addEventListener('click', async (e) => {
            const target = e.target;
            
            // Botão Excluir
            if (target.classList.contains('btn-excluir')) {
                const id = target.dataset.id;
                if (confirm(`Tem certeza que deseja excluir o cliente ID ${id}?`)) {
                    const response = await fetch(`/api/clientes/${id}`, { method: 'DELETE' });
                    if (response.ok) {
                        await carregarClientes();
                        alert('Cliente excluído.');
                    } else {
                        const erro = await response.json();
                        alert(`Erro: ${erro.erro}`);
                    }
                }
            }
            
            // Botão Editar
            if (target.classList.contains('btn-editar')) {
                const id = target.dataset.id;
                
                // 1. Busca os dados atuais do cliente na API
                const response = await fetch(`/api/clientes/${id}`);
                const cliente = await response.json();
                
                // 2. Preenche o formulário com os dados
                document.getElementById('cliente-id').value = cliente.id;
                document.getElementById('nome').value = cliente.nome;
                document.getElementById('email').value = cliente.email;
                document.getElementById('telefone').value = cliente.telefone;
                
                // 3. Foca no formulário
                window.scrollTo(0, 0); // Rola a página para o topo
                form.querySelector('input[name="nome"]').focus();
            }
        });
        
        // Carga inicial dos dados
        carregarClientes();

});