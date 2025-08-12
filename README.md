# Studio Glamour: Sistema de Agendamento para Salão

 Studio Glamour é o jeito moderno de administrar seu salão é muito mais do que um simples sistema de agendamento é a solução completa para transformar a gestão do seu salão.
Com ele, você organiza agenda, clientes, serviços, equipe e finanças de forma prática e eficiente, tudo em um único lugar.

Desde o primeiro contato com o cliente até o fechamento do caixa, cada etapa é controlada com clareza e segurança.
A instalação é rápida, a interface é intuitiva e a adaptação ao seu negócio é imediata.

Mais do que economizar tempo, o Studio Glamour ajuda a aumentar sua produtividade, melhorar a experiência do cliente e profissionalizar a gestão.
Você foca no que faz de melhor: cuidar da beleza, enquanto o sistema cuida do resto.




## Funcionalidades

- Agendamentos sem confusão:

       Organize horários, serviços e profissionais em segundos, evitando falhas e cancelamentos desnecessários.

- Gestão financeira simplificada:

       Registre entradas e saídas, controle seu caixa e saiba exatamente quanto foi seu Lucro.

- Controle total dos clientes:

       Histórico de serviços, preferências e informações sempre à mão para oferecer um atendimento VIP.

- Visual moderno e intuitivo:

       Com o Jazzmin, seu painel administrativo fica bonito e fácil de navegar, mesmo para quem não entende de tecnologia.


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

   Windows PowerShell

       python -m venv venv
       .\venv\Scripts\Activate.ps1   
      
3. Instale as dependências necessárias direto com pip:
   
       pip install Django==5.0 django-jazzmin==2.6.0
   

4. Rode as migrações:  

       python manage.py migrate  

5. Execute o servidor:  

       python manage.py runserver  

6. Acesse no navegador:  

       http://127.0.0.1:8000/admin

7. Login Padrão

       Usuário: m2a
       Senha: admin123


## Observações

       - Banco padrão é SQLite — ideal para desenvolvimento. Para produção, prefira PostgreSQL ou outro banco robusto.  
       - Mantenha o ambiente virtual ativo durante o uso.  
       - Jazzmin permite customizar o admin conforme a necessidade.  

---

Feito por Adams Hans
