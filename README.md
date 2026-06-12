# 🎬 Projeto Relacionamento 1:N - Séries e Episódios

Atividade acadêmica prática desenvolvida utilizando a técnica de **Pair Programming** com Python e SQLAlchemy ORM para simular e gerenciar relacionamentos em bancos de dados relacionais.

## 👥 Integrantes da Dupla
* **Piloto / Navegador:** [Nome do Aluno 1]
* **Navegador / Piloto:** [Nome do Aluno 2]

---

## 📌 Explicação do Relacionamento 1:N
O tema escolhido foi **Série → Episódios**. No modelo relacional adotado:
* A tabela **Série** atua como o lado **PAI (1)** da relação. Uma única série possui atributos macro como título, gênero e nota.
* A tabela **Episódio** atua como o lado **FILHO (N)** da relação. Cada episódio possui dados específicos da exibição e aponta obrigatoriamente para sua respectiva série por meio do campo `serie_id` (Chave Estrangeira - *ForeignKey*).

Para mitigar problemas de integridade relacional ao efetuar exclusões, foi aplicado o parâmetro `cascade="all, delete-orphan"` no mapeamento do SQLAlchemy. Dessa forma, caso uma série seja excluída, o banco de dados limpa automaticamente todos os episódios vinculados a ela.

---

## 🔍 Funcionamento das Consultas
As buscas implementadas no arquivo `main.py` abrangem os seguintes cenários:
1. **Listagem Completa (Filho + Pai):** Percorre todos os episódios cadastrados, mapeando de forma automática os dados da série vinculada através do relacionamento mapeado pelo ORM.
2. **Filtro Direcionado:** Busca uma série específica através do seu identificador (ID) e lista de forma limpa apenas os episódios que possuem a correspondência exata de chave.
3. **Filtro de Existência (Join):** Realiza uma operação de junção (`JOIN`) clássica para filtrar e exibir exclusivamente as séries que possuem ao menos uma ocorrência de episódio na tabela filha.

---

## ⚙️ Como Executar o Projeto

1. Certifique-se de possuir o Python instalado em sua máquina.
2. Instale o pacote do SQLAlchemy executando no terminal:
   ```bash
   pip install sqlalchemy