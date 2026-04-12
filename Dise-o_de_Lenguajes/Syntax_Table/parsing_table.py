from grammar import get_non_terminals
from first_follow import compute_first_of_sequence


def build_parsing_table(grammar: dict, first_sets: dict, follow_sets: dict) -> dict:
    non_terminals = get_non_terminals(grammar)
    table = {nt: {} for nt in non_terminals}

    for A in grammar:
        for production in grammar[A]:
            first_alpha = compute_first_of_sequence(production, first_sets, non_terminals)

            for terminal in first_alpha - {"ε"}:
                table[A].setdefault(terminal, []).append(production)

            if "ε" in first_alpha:
                for terminal in follow_sets[A]:
                    table[A].setdefault(terminal, []).append(production)

    return table


def is_ll1(table: dict) -> tuple:
    conflicts = []
    for A, row in table.items():
        for terminal, productions in row.items():
            if len(productions) > 1:
                conflicts.append((A, terminal, productions))

    return len(conflicts) == 0, conflicts
