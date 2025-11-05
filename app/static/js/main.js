// Em app/static/js/dashboard.js

document.addEventListener('DOMContentLoaded', async () => {
    // A função 'iniciarPaginaDashboard' não é mais necessária,
    // pois o código está direto no 'DOMContentLoaded'.
    // Tornamos o listener do 'DOMContentLoaded' assíncrono (async)
    
    try {
        // 1. Faz todas as requisições em paralelo
        const [respClientes, respServicos, respAtendimentos] = await Promise.all([
            fetch('/api/clientes'),
            fetch('/api/servicos'),
            fetch('/api/atendimentos')
        ]);
        
        // 2. Verifica se alguma das requisições falhou por falta de login (401)
        const responses = [respClientes, respServicos, respAtendimentos];
        for (const resp of responses) {
            if (resp.status === 401) {
                // Se a sessão expirou, redireciona para o login
                window.location.href = '/auth/login';
                return; // Para a execução do script
            }
        }
        
        // 3. Se todas as respostas foram OK, extrai o JSON
        const [clientes, servicos, atendimentos] = await Promise.all([
            respClientes.json(),
            respServicos.json(),
            respAtendimentos.json()
        ]);
        
        // 4. Atualiza o DOM com as contagens
        document.getElementById('count-clientes').innerText = clientes.length;
        document.getElementById('count-servicos').innerText = servicos.length;
        document.getElementById('count-atendimentos').innerText = atendimentos.length;
        
    } catch (error) {
        // 5. Tratamento de erro (ex: API offline)
        console.error("Erro ao carregar estatísticas do dashboard:", error);
        const statsContainer = document.getElementById('dashboard-stats');
        if (statsContainer) {
            statsContainer.innerHTML = 
                "<p>Erro ao carregar estatísticas. Verifique se a API está online.</p>";
        }
    }
});