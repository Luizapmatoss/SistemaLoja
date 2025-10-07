import time

try:
    from colorama import init as colorama_init
    colorama_init()
except Exception:
    pass

# estilização de cores
class Cores:
    VERMELHO = "\033[91m"
    VERDE = "\033[92m"
    AMARELO = "\033[93m"
    AZUL = "\033[94m"
    MAGENTA = "\033[95m"
    CIANO = "\033[96m"
    RESET = "\033[0m"
    NEGRITO = "\033[1m"

# classes do sistema
class Produto:
    def __init__(self, nome: str, preco: float, codigo: str):
        self.nome = nome
        self._preco = float(preco)
        self.__codigo = codigo

        if self._preco < 0:
            raise ValueError(">> O preço não pode ser negativo!")

    def mostrar_infos(self):
        # Retorna uma linha com nome, preço e código formatados
        return f"{self.nome:<18} | R${self._preco:>7.2f} | [{self.__codigo}]"

class Carrinho:
    def __init__(self):
        self.__itens = []

    def adicionar(self, produto: Produto):
        try:
            print(f"{Cores.CIANO}Adicionando produto ao carrinho...{Cores.RESET}", end="")
            time.sleep(0.6)
            self.__itens.append(produto)
            time.sleep(0.3)
            print(f" {Cores.VERDE}✅ Concluído!{Cores.RESET}")
            return f">> Produto '{produto.nome}' adicionado com sucesso"
        except Exception as e:
            print()
            return f">> Erro ao adicionar produto: {e}"

    def ver_produtos(self):
        if not self.__itens:
            return f"{Cores.AMARELO}>> Carrinho vazio{Cores.RESET}"

        titulo = f"{Cores.MAGENTA}{Cores.NEGRITO}>> Itens que estão no carrinho:{Cores.RESET}\n"
        titulo += f"{Cores.NEGRITO}{'Produto':<18} | {'Preço':<8} | Código{Cores.RESET}\n"
        titulo += "-" * 46 + "\n"
        total = 0.0

        for produto in self.__itens:
            titulo += produto.mostrar_infos() + "\n"
            total += produto._preco

        titulo += "-" * 46 + "\n"
        titulo += f"{Cores.VERDE}{Cores.NEGRITO}>> Total: R${total:.2f}{Cores.RESET}"
        return titulo

    def finalizar_compra(self):
        if not self.__itens:
            return f"{Cores.AMARELO}>> Carrinho vazio. Nada para finalizar.{Cores.RESET}"
        total = sum(p._preco for p in self.__itens)
        self.__itens.clear()
        return f"{Cores.VERDE}Compra finalizada com sucesso! Total pago: R${total:.2f}{Cores.RESET}"

class Cliente:
    def __init__(self, nome, id_cliente):
        self.nome = nome
        self.__id = id_cliente
        self.carrinho = Carrinho()

    def comprar(self, produto: Produto):
        resultado = self.carrinho.adicionar(produto)
        return f"{Cores.AZUL}{self.nome}:{Cores.RESET} {resultado}"

# funções utilitárias
def cabeçalho():
    print(Cores.AZUL + "="*60 + Cores.RESET)
    print(Cores.AZUL + "🛒".center(60) + Cores.RESET)
    print(Cores.NEGRITO + Cores.MAGENTA + "╔══════════════════════════════════════════════════════╗" + Cores.RESET)
    print(Cores.NEGRITO + Cores.MAGENTA + "║        🛍️  SISTEMA DE LOJA VIRTUAL - VERSÃO BONITA     ║" + Cores.RESET)
    print(Cores.NEGRITO + Cores.MAGENTA + "╚══════════════════════════════════════════════════════╝" + Cores.RESET)
    print(Cores.AZUL + "="*60 + Cores.RESET)

def separador(titulo: str = ""):
    print("\n" + Cores.CIANO + "-"*60 + Cores.RESET)
    if titulo:
        print(Cores.NEGRITO + titulo + Cores.RESET)
        print(Cores.CIANO + "-"*60 + Cores.RESET)

# programa principal
def main():
    cabeçalho()
    produtos_disponiveis = []

    separador(">> Cadastrar produtos iniciais")
    # alguns produtos iniciais para demo
    try:
        produtos_disponiveis.append(Produto("Arroz 5kg", 25.90, "P001"))
        produtos_disponiveis.append(Produto("Teclado Gamer", 149.90, "P002"))
        produtos_disponiveis.append(Produto("Camiseta", 39.99, "P003"))
    except ValueError as e:
        print(Cores.VERMELHO + str(e) + Cores.RESET)

    # cadastrar cliente
    separador(">> Cadastro do cliente")
    nome_cliente = input("> Nome do cliente: ")
    id_cliente = input("> ID do cliente: ")
    cliente = Cliente(nome_cliente, id_cliente)
    print(f"{Cores.VERDE}>> Cliente '{cliente.nome}' cadastrado com sucesso!{Cores.RESET}")

    # menu principal
    while True:
        separador(">> Menu Principal")
        print("""
    [1] Mostrar produtos disponíveis
    [2] Adicionar produto ao carrinho (pelo código)
    [3] Ver carrinho
    [4] Finalizar compra
    [5] Cadastrar novo produto
    [0] Sair
        """)
        opc = input("Escolha uma opção: ").strip()

        if opc == "0":
            print(Cores.AMARELO + "👋 Saindo da loja... Até mais!" + Cores.RESET)
            break

        elif opc == "1":
            separador(">> Produtos Disponíveis")
            print(f"{Cores.NEGRITO}{'Produto':<18} | {'Preço':<8}  | Código{Cores.RESET}")
            print("-"*46)
            for p in produtos_disponiveis:
                print(p.mostrar_infos())
            print("-"*46)

        elif opc == "2":
            codigo_busca = input("> Digite o código do produto para adicionar: ").strip()
            encontrado = None
            for p in produtos_disponiveis:
                try:
                    codigo_p = getattr(p, f"_Produto__codigo")
                except AttributeError:
                    codigo_p = None

                if codigo_busca.lower() == p.mostrar_infos().split("|")[-1].strip().strip("[]").lower():
                    encontrado = p
                    break

                if codigo_busca.lower() == str(p._Produto__codigo).lower() if hasattr(p, "_Produto__codigo") else False:
                    encontrado = p
                    break
            if not encontrado:
                for p in produtos_disponiveis:
                    if codigo_busca.lower() in p.nome.lower() or codigo_busca.lower() in getattr(p, "_Produto__codigo", "").lower():
                        encontrado = p
                        break

            if encontrado:
                resultado = cliente.comprar(encontrado)
                print(resultado)
            else:
                print(Cores.VERMELHO + ">> Produto não encontrado. Tente pelo nome ou código." + Cores.RESET)

        elif opc == "3":
            separador(">> Seu Carrinho")
            print(cliente.carrinho.ver_produtos())

        elif opc == "4":
            separador(">> Finalizar Compra")
            print(cliente.carrinho.finalizar_compra())

        elif opc == "5":
            separador(">> Cadastrar Novo Produto")
            nome = input("> Nome do produto: ")
            try:
                preco = float(input("Preço do produto: R$"))
            except ValueError:
                print(Cores.VERMELHO + "Preço inválido. Tente novamente." + Cores.RESET)
                continue
            codigo = input("Código do produto: ")
            try:
                novo = Produto(nome, preco, codigo)
                produtos_disponiveis.append(novo)
                print(Cores.VERDE + ">> Produto cadastrado com sucesso!" + Cores.RESET)
            except ValueError as e:
                print(Cores.VERMELHO + str(e) + Cores.RESET)

        else:
            print(Cores.AMARELO + "Opção inválida — tenta outra vez" + Cores.RESET)

if __name__ == "__main__":
    main()
