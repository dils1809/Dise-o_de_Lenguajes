import sys
import argparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from first_follow import compute_all_first, compute_follow
from parsing_table import build_parsing_table, is_ll1
from utils import (
    print_grammar,
    print_first_sets,
    print_follow_sets,
    print_parsing_table,
    print_ll1_result,
)


def analyze_grammar(title: str, grammar: dict, start: str = None) -> None:
    """
    Run the full LL(1) analysis pipeline for a grammar.

    Args:
        title   : label printed in the output header
        grammar : dict mapping non-terminals to their productions
        start   : start symbol; defaults to the first key in grammar
    """
    print("\n" + "#" * 60)
    print(f"  {title}")
    if start:
        print(f"  Start symbol: {start}")
    print("#" * 60)

    print_grammar(grammar)

    first_sets = compute_all_first(grammar)
    print_first_sets(first_sets)

    follow_sets = compute_follow(grammar, first_sets, start)
    print_follow_sets(follow_sets)

    table = build_parsing_table(grammar, first_sets, follow_sets)
    print_parsing_table(table, grammar)

    result, conflicts = is_ll1(table)
    print_ll1_result(result, conflicts)


# ── Default test grammars ────────────────────────────────────────────────────

# Grammar 1 — Arithmetic Expressions (LL(1))
grammar1 = {
    "E":  [["T", "E'"]],
    "E'": [["+", "T", "E'"], ["ε"]],
    "T":  [["F", "T'"]],
    "T'": [["*", "F", "T'"], ["ε"]],
    "F":  [["(", "E", ")"], ["id"]],
}

# Grammar 2 — Simple Statement Language (LL(1))
grammar2 = {
    "P":  [["S", "L"]],
    "L":  [["S", "L"], ["ε"]],
    "S":  [["id", "=", "E", ";"], ["return", "E", ";"]],
    "E":  [["id"], ["num"]],
}

# Grammar 3 — Left-Recursive Arithmetic (NOT LL(1))
grammar3 = {
    "E": [["E", "+", "T"], ["T"]],
    "T": [["T", "*", "F"], ["F"]],
    "F": [["(", "E", ")"], ["id"]],
}


# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="LL(1) Parser Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python main.py                          # run 3 built-in grammars\n"
            "  python main.py -f grammars/arithmetic.txt\n"
            "  python main.py -i                       # type grammar in console\n"
            "  python main.py -f my.txt --start S      # override start symbol\n"
        ),
    )
    parser.add_argument(
        "-f", "--file",
        metavar="PATH",
        help="load grammar from a text file",
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="enter grammar interactively in the console",
    )
    parser.add_argument(
        "--start",
        metavar="NT",
        help="override the start symbol (used with -f or -i)",
    )
    args = parser.parse_args()

    if args.file:
        from input_parser import load_grammar_file
        grammar, detected_start = load_grammar_file(args.file)
        start = args.start or detected_start
        analyze_grammar(f"Grammar from '{args.file}'", grammar, start)

    elif args.interactive:
        from input_parser import input_grammar_interactive
        grammar, detected_start = input_grammar_interactive()
        start = args.start or detected_start
        analyze_grammar("Custom grammar", grammar, start)

    else:
        analyze_grammar("Grammar 1 -- Arithmetic Expressions  (LL(1))",        grammar1)
        analyze_grammar("Grammar 2 -- Simple Statement Language  (LL(1))",     grammar2)
        analyze_grammar("Grammar 3 -- Left-Recursive Arithmetic  (NOT LL(1))", grammar3)


if __name__ == "__main__":
    main()
