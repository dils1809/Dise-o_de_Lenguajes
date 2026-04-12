def get_non_terminals(grammar: dict) -> set:
    return set(grammar.keys())


def get_terminals(grammar: dict) -> set:
    non_terminals = get_non_terminals(grammar)
    terminals = set()
    for productions in grammar.values():
        for production in productions:
            for symbol in production:
                if symbol not in non_terminals and symbol != "ε":
                    terminals.add(symbol)
    return terminals


def get_start_symbol(grammar: dict) -> str:
    return next(iter(grammar))
