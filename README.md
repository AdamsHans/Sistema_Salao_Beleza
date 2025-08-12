# Studio Glamour: Sistema de Agendamento para Salão

Projeto Django para gerenciar agendamentos, clientes, funcionários, serviços e controle financeiro de salão de beleza.  
Pensado para facilitar a operação do salão, com foco em simplicidade e eficiência.

## Funcionalidades

- Gestão completa de Clientes, Funcionários, Serviços e Agendamentos  
- Controle financeiro básico: cadastro de entradas e saídas, fluxo de caixa  
- Status dos agendamentos: Agendado, Concluído, Cancelado  
- Cadastro de múltiplos serviços por agendamento  
- Busca, filtros e ordenação no Django Admin  

## Tecnologias

- Python 3.x  
- Django 5.0  
- Jazzmin (customização do admin)  
- SQLite (banco padrão para desenvolvimento)  

## Como Executar

1. Clone o repositório:  

       git clone git@github.com:AdamsHans/sistema-salao-beleza.git  
       cd sistema-salao-beleza  

2. Crie e ative o ambiente virtual (Linux/macOS):  

       python3 -m venv venv  
       source venv/bin/activate  

   (Windows PowerShell e Prompt seguem o padrão que você já colocou)

3. Rode as migrações:  

       python manage.py migrate  

4. Execute o servidor:  

       python manage.py runserver  

5. Acesse no navegador:  

       http://127.0.0.1:8000/admin  

## Observações

- Banco padrão é SQLite — ideal para desenvolvimento. Para produção, prefira PostgreSQL ou outro banco robusto.  
- Mantenha o ambiente virtual ativo durante o uso.  
- Jazzmin permite customizar o admin conforme a necessidade.  

---

Feito por AdamsHans
