from models import Base, engine, SessionLocal, Serie, Episodio
from sqlalchemy import select

# Inicializa o banco de dados
def inicializar_banco():
    Base.metadata.create_all(bind=engine)

# ==========================================
# ETAPA 3 - INSERÇÃO DE DADOS
# ==========================================
def popular_banco_inicial():
    session = SessionLocal()
    
    # Verifica se já está populado para não duplicar
    if session.scalars(select(Serie)).first() is not None:
        session.close()
        return

    # 4 Registros na tabela Pai
    s1 = Serie(titulo="Breaking Bad", genero="Drama", ano_lancamento=2008, nota_imdb=9.5)
    s2 = Serie(titulo="Stranger Things", genero="Ficção Científica", ano_lancamento=2016, nota_imdb=8.7)
    s3 = Serie(titulo="The Office", genero="Comédia", ano_lancamento=2005, nota_imdb=9.0)
    s4 = Serie(titulo="Dark", genero="Suspense", ano_lancamento=2017, nota_imdb=8.7)
    
    session.add_all([s1, s2, s3, s4])
    session.commit() # Commit para gerar os IDs dos pais

    # 10 Registros na tabela Filha (todos com pai_id válido)
    eps = [
        Episodio(titulo="Pilot", temporada=1, numero=1, duracao_minutos=58, serie_id=s1.id),
        Episodio(titulo="Cat's in the Bag...", temporada=1, numero=2, duracao_minutos=48, serie_id=s1.id),
        Episodio(titulo="The Chapter One: The Vanishing of Will Byers", temporada=1, numero=1, duracao_minutos=47, serie_id=s2.id),
        Episodio(titulo="The Weirdo on Maple Street", temporada=1, numero=2, duracao_minutos=55, serie_id=s2.id),
        Episodio(titulo="Pilot Office", temporada=1, numero=1, duracao_minutos=23, serie_id=s3.id),
        Episodio(titulo="Diversity Day", temporada=1, numero=2, duracao_minutos=22, serie_id=s3.id),
        Episodio(titulo="The Dundies", temporada=2, numero=1, duracao_minutos=21, serie_id=s3.id),
        Episodio(titulo="Secrets", temporada=1, numero=1, duracao_minutos=44, serie_id=s4.id),
        Episodio(titulo="Lies", temporada=1, numero=2, duracao_minutos=45, serie_id=s4.id),
        Episodio(titulo="Past and Present", temporada=1, numero=3, duracao_minutos=46, serie_id=s4.id)
    ]
    
    session.add_all(eps)
    session.commit()
    session.close()
    print("👉 Banco de dados criado e populado com sucesso!")

# ==========================================
# ETAPA 4 - CONSULTAS (SELECT)
# ==========================================
def listar_todos_episodios_com_serie():
    session = SessionLocal()
    # 1. Listar todos os filhos com dados do pai
    episodios = session.scalars(select(Episodio)).all()
    print("\n--- TODOS OS EPISÓDIOS E SUAS SÉRIES ---")
    for ep in episodios:
        print(f"Episódio: '{ep.titulo}' (T{ep.temporada}E{ep.numero}) -> Série: {ep.serie.titulo}")
    session.close()

def filtrar_episodios_de_uma_serie(serie_id):
    session = SessionLocal()
    # 2. Filtrar filhos de um pai específico
    serie = session.get(Serie, serie_id)
    if serie:
        print(f"\n--- EPISÓDIOS DE: {serie.titulo} ---")
        for ep in serie.episodios:
            print(f"- T{ep.temporada}E{ep.numero}: {ep.titulo} ({ep.duracao_minutos} min)")
    else:
        print("❌ Série não encontrada.")
    session.close()

def listar_series_com_episodios():
    session = SessionLocal()
    # 3. Listar apenas pais que possuem filhos (usando join)
    series = session.scalars(select(Serie).join(Serie.episodios).distinct()).all()
    print("\n--- SÉRIES QUE POSSUEM EPISÓDIOS CADASTRADOS ---")
    for s in series:
        print(f"- {s.titulo} ({s.genero})")
    session.close()

# ==========================================
# ETAPA 5 - ATUALIZAÇÃO (UPDATE)
# ==========================================
def atualizar_nota_serie(serie_id, nova_nota):
    session = SessionLocal()
    serie = session.get(Serie, serie_id)
    if serie:
        serie.nota_imdb = nova_nota
        session.commit()
        print(f"✅ Nota da série '{serie.titulo}' atualizada para {nova_nota}!")
    session.close()

def atualizar_nome_episodio(episodio_id, novo_titulo):
    session = SessionLocal()
    ep = session.get(Episodio, episodio_id)
    if ep:
        ep.titulo = novo_titulo
        session.commit()
        print(f"✅ Título do episódio ID {episodio_id} atualizado para '{novo_titulo}'!")
    session.close()

# ==========================================
# ETAPA 6 - REMOÇÃO (DELETE)
# ==========================================
def deletar_episodio(episodio_id):
    session = SessionLocal()
    ep = session.get(Episodio, episodio_id)
    if ep:
        session.delete(ep)
        session.commit()
        print("✅ Episódio removido com sucesso!")
    session.close()

def deletar_serie_e_filhos(serie_id):
    session = SessionLocal()
    serie = session.get(Serie, serie_id)
    if serie:
        # O cascade="all, delete-orphan" definido no models.py garante
        # que ao deletar o pai, todos os episódios filhos somem automaticamente, evitando erros de chave estrangeira.
        session.delete(serie)
        session.commit()
        print(f"✅ Série '{serie.titulo}' e todos os seus episódios foram removidos!")
    session.close()

# ==========================================
# BÔNUS - MENU INTERATIVO NO TERMINAL
# ==========================================
def menu():
    inicializar_banco()
    popular_banco_inicial()

    while True:
        print("\n==============================")
        print("    SISTEMA SÉRIE & EPISÓDIOS ")
        print("==============================")
        print("1. Listar todos os episódios (com nome da série)")
        print("2. Filtrar episódios por ID da Série")
        print("3. Listar séries que possuem episódios")
        print("4. Atualizar nota de uma Série")
        print("5. Atualizar título de um Episódio")
        print("6. Deletar um Episódio")
        print("7. Deletar uma Série (e seus episódios)")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_todos_episodios_com_serie()
        elif opcao == "2":
            id_s = int(input("Digite o ID da Série (1 a 4): "))
            filtrar_episodios_de_uma_serie(id_s)
        elif opcao == "3":
            listar_series_com_episodios()
        elif opcao == "4":
            id_s = int(input("ID da Série: "))
            nota = float(input("Nova Nota IMDB: "))
            atualizar_nota_serie(id_s, nota)
        elif opcao == "5":
            id_e = int(input("ID do Episódio: "))
            tit = input("Novo Título: ")
            if tit.strip() == "": # Validação bônus
                print("❌ O título não pode ser vazio!")
            else:
                atualizar_nome_episodio(id_e, tit)
        elif opcao == "6":
            id_e = int(input("ID do Episódio para deletar: "))
            deletar_episodio(id_e)
        elif opcao == "7":
            id_s = int(input("ID da Série para deletar inteira: "))
            deletar_serie_e_filhos(id_s)
        elif opcao == "0":
            print("Saindo do sistema... Até logo!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    menu()