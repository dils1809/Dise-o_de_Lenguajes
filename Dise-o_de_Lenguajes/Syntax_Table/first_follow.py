from grammar import get_non_terminals, get_start_symbol


def compute_first_of_sequence(sequence: list, first_sets: dict, non_terminals: set) -> set:
    result = set()

    if not sequence:
        result.add("ε")
        return result

    for symbol in sequence:
        if symbol == "ε":
            result.add("ε")
            return result
        elif symbol not in non_terminals:
            result.add(symbol)
            return result
        else:
            sym_first = first_sets.get(symbol, set())
            result |= sym_first - {"ε"}
            if "ε" not in sym_first:
                return result

    result.add("ε")
    return result


def compute_all_first(grammar: dict) -> dict:
    non_terminals = get_non_terminals(grammar)
    first_sets = {nt: set() for nt in non_terminals}

    changed = True
    while changed:
        changed = False
        for A in grammar:
            for production in grammar[A]:
                new = compute_first_of_sequence(production, first_sets, non_terminals)
                if not new.issubset(first_sets[A]):
                    first_sets[A] |= new
                    changed = True

    return first_sets


def compute_follow(grammar: dict, first_sets: dict, start: str = None) -> dict:
    non_terminals = get_non_terminals(grammar)
    start_symbol = start if start is not None else get_start_symbol(grammar)

    follow_sets = {nt: set() for nt in non_terminals}
    follow_sets[start_symbol].add("$")

    changed = True
    while changed:
        changed = False
        for A in grammar:
            for production in grammar[A]:
                for i, symbol in enumerate(production):
                    if symbol not in non_terminals:
                        continue

                    beta = production[i + 1:]
                    old_size = len(follow_sets[symbol])

                    if beta:
                        first_beta = compute_first_of_sequence(beta, first_sets, non_terminals)
                        follow_sets[symbol] |= first_beta - {"ε"}
                        if "ε" in first_beta:
                            follow_sets[symbol] |= follow_sets[A]
                    else:
                        follow_sets[symbol] |= follow_sets[A]

                    if len(follow_sets[symbol]) > old_size:
                        changed = True

    return follow_sets
