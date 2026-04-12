from grammar import get_terminals

_SEP_WIDTH = 58


def _line(char: str = "=") -> str:
    return char * _SEP_WIDTH


def _prod_str(production: list) -> str:
    return " ".join(production)


def print_grammar(grammar: dict) -> None:
    print(_line())
    print("  GRAMMAR")
    print(_line())
    for nt, productions in grammar.items():
        for idx, prod in enumerate(productions):
            if idx == 0:
                print(f"  {nt:<5} ->  {_prod_str(prod)}")
            else:
                print(f"  {' ' * 5}  |  {_prod_str(prod)}")
    print()


def print_first_sets(first_sets: dict) -> None:
    print(_line())
    print("  FIRST SETS")
    print(_line())
    for nt, first in first_sets.items():
        symbols = ", ".join(sorted(first))
        print(f"  FIRST({nt}) = {{ {symbols} }}")
    print()


def print_follow_sets(follow_sets: dict) -> None:
    print(_line())
    print("  FOLLOW SETS")
    print(_line())
    for nt, follow in follow_sets.items():
        symbols = ", ".join(sorted(follow))
        print(f"  FOLLOW({nt}) = {{ {symbols} }}")
    print()


def print_parsing_table(table: dict, grammar: dict) -> None:
    print(_line())
    print("  LL(1) PARSING TABLE")
    print(_line())

    non_terminals = list(grammar.keys())
    terminals = sorted(get_terminals(grammar)) + ["$"]

    def cell_text(nt: str, term: str) -> str:
        prods = table[nt].get(term)
        if not prods:
            return "-"
        if len(prods) == 1:
            return f"{nt} -> {_prod_str(prods[0])}"
        return f"[CONFLICT x{len(prods)}]"

    nt_col = max(len(nt) for nt in non_terminals)
    col_w = {
        t: max(len(t), *(len(cell_text(nt, t)) for nt in non_terminals))
        for t in terminals
    }

    header = " " * nt_col + "  " + "  ".join(t.center(col_w[t]) for t in terminals)
    print(header)
    print(_line("-"))

    for nt in non_terminals:
        cells = "  ".join(cell_text(nt, t).center(col_w[t]) for t in terminals)
        print(f"{nt.ljust(nt_col)}  {cells}")

    print()


def print_ll1_result(is_ll1_grammar: bool, conflicts: list) -> None:
    print(_line())
    print("  LL(1) ANALYSIS RESULT")
    print(_line())
    if is_ll1_grammar:
        print("  [OK] The grammar IS LL(1).")
    else:
        print("  [!!] The grammar is NOT LL(1).")
        print(f"       {len(conflicts)} conflict(s) detected:\n")
        for A, terminal, productions in conflicts:
            print(f"    M[{A}][{terminal}]  has multiple productions:")
            for prod in productions:
                print(f"        {A} -> {_prod_str(prod)}")
            print()
    print()
