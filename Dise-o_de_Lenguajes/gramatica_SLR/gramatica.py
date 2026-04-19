class Item:
    """Item LR(0): A -> α • β"""
    def __init__(self, production, position):
        self.no_terminal = production[0]
        self.body = production[1]
        self.position = position

    def __eq__(self, other):
        return (self.no_terminal == other.no_terminal and
                self.body == other.body and
                self.position == other.position)

    def __hash__(self):
        return hash((self.no_terminal, tuple(self.body), self.position))

    def __repr__(self):
        if self.position <= len(self.body):
            body_with_dot = ' '.join(self.body[:self.position]) + ' • ' + ' '.join(self.body[self.position:])
        else:
            body_with_dot = ' '.join(self.body) + ' •'
        return f"{self.no_terminal} -> {body_with_dot.strip()}"

    def get_next_symbol(self):
        """Símbolo después del punto, None si está al final."""
        if self.position < len(self.body):
            return self.body[self.position]
        return None

    def is_terminal(self, symbol):
        if symbol in ['+', '-', '*', '/', '(', ')', 'id', 'num']:
            return True
        return symbol.islower() or symbol in ['ε', '+', '-', '*', '/', '(', ')']


class Grammar:
    """Gramática independiente de contexto."""
    def __init__(self, productions):
        self.productions = productions
        self.non_terminals = set(productions.keys())
        self.terminals = self._extract_terminals()

    def _extract_terminals(self):
        terminals = set()
        for _, prods in self.productions.items():
            for prod in prods:
                for symbol in prod:
                    if symbol not in self.non_terminals and symbol != 'ε':
                        terminals.add(symbol)
        return terminals

    def get_productions_for(self, non_terminal):
        return self.productions.get(non_terminal, [])


def CERRADURA(items, grammar, verbose=True):
    """Calcula la cerradura de un conjunto de items LR(0)."""
    closure = set(items)

    if verbose:
        print("\n  [Cálculo paso a paso]")

    changed = True
    while changed:
        changed = False
        for item in list(closure):
            next_symbol = item.get_next_symbol()
            if next_symbol and next_symbol in grammar.non_terminals:
                for production in grammar.get_productions_for(next_symbol):
                    new_item = Item((next_symbol, production), 0)
                    if new_item not in closure:
                        closure.add(new_item)
                        changed = True
                        if verbose:
                            print(f"    Agregado (por '{next_symbol}' en [{item}]): {new_item}")

    if verbose and len(closure) == len(items):
        print("    (No se agregaron items nuevos)")

    return closure


def main():
    grammar_data = {
        'E': [['E', '+', 'T'], ['T']],
        'T': [['T', '*', 'F'], ['F']],
        'F': [['(', 'E', ')'], ['id']]
    }

    grammar = Grammar(grammar_data)

    print("=" * 60)
    print("CALCULADORA DE CERRADURAS (CLOSURE) - Items LR(0)")
    print("=" * 60)
    print("\nGramática cargada:")
    for nt, prods in grammar_data.items():
        for prod in prods:
            print(f"  {nt} -> {' '.join(prod)}")

    print("\n" + "=" * 60)

    while True:
        print("\nOpciones:")
        print("1. Ingresar un item inicial")
        print("2. Ingresar un conjunto de items")
        print("3. Salir")

        opcion = input("\nSeleccione opción: ").strip()

        if opcion == '1':
            print("\nFormato: no_terminal, producción, posición del punto")
            print("Ejemplo: E, E + T, 1  (punto después del primer símbolo)")
            nt = input("No-terminal: ").strip()
            prod_str = input("Producción (separada por espacios): ").strip()
            prod = prod_str.split()
            print(f"Posición del punto (0 = inicio, {len(prod)} = final): ", end="")
            try:
                pos = int(input().strip())
            except ValueError:
                pos = 0

            if nt in grammar.non_terminals and 0 <= pos <= len(prod):
                items = {Item((nt, prod), pos)}
                print(f"\nConjunto de items ingresados ({len(items)}):")
                for item in sorted(items, key=lambda x: (x.no_terminal, x.body)):
                    print(f"  {item}")

                closure = CERRADURA(items, grammar, verbose=True)

                print(f"\nCerradura completa ({len(closure)} items):")
                for item in sorted(closure, key=lambda x: (x.no_terminal, x.body)):
                    print(f"  {item}")
            else:
                print("Error: no-terminal inválido o posición fuera de rango")

        elif opcion == '2':
            print("\nIngrese items uno por uno. Deje el no-terminal vacío para terminar.")

            items = set()
            while True:
                nt = input("\nNo-terminal (vacío para terminar): ").strip()
                if not nt:
                    break
                prod_str = input("Producción (separada por espacios): ").strip()
                prod = prod_str.split()
                print(f"Posición del punto (0 = inicio, {len(prod)} = final): ", end="")
                try:
                    pos = int(input().strip())
                except ValueError:
                    pos = 0

                if nt in grammar.non_terminals and 0 <= pos <= len(prod):
                    items.add(Item((nt, prod), pos))
                    print(f"  Agregado: {Item((nt, prod), pos)}")
                else:
                    print("Error: no-terminal inválido o posición fuera de rango")

            if items:
                print(f"\nConjunto de items ingresados ({len(items)}):")
                for item in sorted(items, key=lambda x: (x.no_terminal, x.body)):
                    print(f"  {item}")

                closure = CERRADURA(items, grammar, verbose=True)

                print(f"\nCerradura completa ({len(closure)} items):")
                for item in sorted(closure, key=lambda x: (x.no_terminal, x.body)):
                    print(f"  {item}")

        elif opcion == '3':
            print("\n¡Hasta luego!")
            break

        else:
            print("Opción no válida")


if __name__ == '__main__':
    main()
