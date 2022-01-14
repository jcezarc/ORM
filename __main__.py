from commands import Commands


class Pessoa:
    def __init__(self, cpf, nome, idade, salario):
        self.cpf = cpf
        self.nome = nome
        self.idade = idade
        self.salario = salario


if __name__ == '__main__':  # --- TESTES ---
    joao = Pessoa(
        cpf='111.222.333-44',
        nome='João',
        idade=21,
        salario=3456.78
    )
    for cmd in Commands(joao, key='cpf').sql.values():
        print('-'*20)
        print(cmd)
