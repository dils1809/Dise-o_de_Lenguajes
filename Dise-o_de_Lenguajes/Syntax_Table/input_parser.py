"""
input_parser.py — Load grammars from text, files, or console input.

Text format
-----------
  E  -> T E'
  E' -> + T E' | eps
  F  -> ( E ) | id

Rules:
  - One or more productions per line: NT -> p1 | p2 | ...
  - Use 'eps' or 'epsilon' for the empty string (ε).
  - Lines starting with '#' are comments.
  - A '# start: NT' comment sets the start symbol explicitly;
    otherwise the first non-terminal in the file is used.
  - The same NT can appear on multiple lines; its productions are merged.
"""


_EPSILON_ALIASES = {"eps", "epsilon", "ε"}


def parse_grammar_text(text: str) -> tuple:
    """
    Parse a grammar from a plain-text string.

    Returns:
        (grammar dict, start symbol string)
    Raises:
        ValueError if the text is empty or a line is malformed.
    """
    grammar = {}
    start_override = None
    first_nt = None

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("#"):
            low = line.lower()
            if "start:" in low:
                _, _, value = line.partition(":")
                candidate = value.strip()
                if candidate:
                    start_override = candidate
            continue

        if "->" not in line:
            raise ValueError(f"Missing '->' in rule: '{line}'")

        lhs, _, rhs_str = line.partition("->")
        lhs = lhs.strip()

        if not lhs:
            raise ValueError(f"Empty left-hand side in: '{line}'")

        if first_nt is None:
            first_nt = lhs

        productions = []
        for alt in rhs_str.split("|"):
            symbols = alt.strip().split()
            if not symbols:
                raise ValueError(f"Empty alternative in: '{line}'")
            symbols = ["ε" if s in _EPSILON_ALIASES else s for s in symbols]
            productions.append(symbols)

        if lhs in grammar:
            grammar[lhs].extend(productions)
        else:
            grammar[lhs] = productions

    if not grammar:
        raise ValueError("No grammar rules found in the input.")

    start = start_override if start_override else first_nt
    return grammar, start


def load_grammar_file(path: str) -> tuple:
    """
    Load a grammar from a UTF-8 text file.

    Returns:
        (grammar dict, start symbol string)
    """
    with open(path, "r", encoding="utf-8") as f:
        return parse_grammar_text(f.read())


def input_grammar_interactive() -> tuple:
    """
    Read a grammar rule-by-rule from stdin.
    Enter an empty line to finish.

    Returns:
        (grammar dict, start symbol string)
    """
    print("Enter grammar rules, one per line. Empty line to finish.")
    print("  Format:  NT -> sym1 sym2 | sym3   (use 'eps' for epsilon)")
    print()

    lines = []
    while True:
        try:
            line = input("  > ")
        except EOFError:
            break
        if not line.strip():
            break
        lines.append(line)

    if not lines:
        raise ValueError("No rules were entered.")

    return parse_grammar_text("\n".join(lines))
