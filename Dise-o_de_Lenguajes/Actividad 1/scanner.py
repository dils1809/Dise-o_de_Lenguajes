class Token:
    def __init__(self, tipo, lexema, linea, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f"[{self.linea},{self.columna}] {self.tipo} -> {self.lexema}"

class TablaSimbolos:
    def __init__(self):
        self.simbolos = set()

    def agregar(self, nombre):
        self.simbolos.add(nombre)

    def mostrar(self):
        return list(self.simbolos)

class Scanner:
    def __init__(self, codigo):
        self.codigo = codigo
        self.pos = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []
        self.tabla = TablaSimbolos()

        self.reservadas = {
            "public", "class", "static", "void", "int", "double",
            "if", "else", "return", "private", "new"
        }

    def actual(self):
        if self.pos < len(self.codigo):
            return self.codigo[self.pos]
        return None

    def avanzar(self):
        if self.actual() == '\n':
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1
        self.pos += 1

    def analizar(self):
        while self.actual() is not None:
            c = self.actual()

            # Ignorar espacios
            if c.isspace():
                self.avanzar()
                continue

            # Identificadores o palabras reservadas
            if c.isalpha():
                self.leer_identificador()
                continue

            # Números
            if c.isdigit():
                self.leer_numero()
                continue

            # Cadenas
            if c == '"':
                self.leer_cadena()
                continue

            # Comentarios //
            if c == '/' and self.peek() == '/':
                self.saltar_comentario()
                continue

            # Operadores y símbolos
            self.tokens.append(Token("SIMBOLO", c, self.linea, self.columna))
            self.avanzar()

    def peek(self):
        if self.pos + 1 < len(self.codigo):
            return self.codigo[self.pos + 1]
        return None

    def leer_identificador(self):
        inicio_col = self.columna
        lexema = ""

        while self.actual() and (self.actual().isalnum() or self.actual() == '_'):
            lexema += self.actual()
            self.avanzar()

        if lexema in self.reservadas:
            tipo = "PALABRA_RESERVADA"
        else:
            tipo = "IDENTIFICADOR"
            self.tabla.agregar(lexema)

        self.tokens.append(Token(tipo, lexema, self.linea, inicio_col))

    def leer_numero(self):
        inicio_col = self.columna
        lexema = ""
        punto = False

        while self.actual() and (self.actual().isdigit() or self.actual() == '.'):
            if self.actual() == '.':
                if punto:
                    break
                punto = True
            lexema += self.actual()
            self.avanzar()

        tipo = "CONSTANTE_REAL" if punto else "CONSTANTE_ENTERA"
        self.tokens.append(Token(tipo, lexema, self.linea, inicio_col))

    def leer_cadena(self):
        inicio_col = self.columna
        self.avanzar()  # saltar "

        lexema = ""
        while self.actual() and self.actual() != '"':
            lexema += self.actual()
            self.avanzar()

        self.avanzar()  # cerrar "

        self.tokens.append(Token("LITERAL_CADENA", lexema, self.linea, inicio_col))

    def saltar_comentario(self):
        while self.actual() and self.actual() != '\n':
            self.avanzar()

with open("PotionBrewer.java", "r", encoding="utf-8") as f:
    codigo = f.read()

scanner = Scanner(codigo)
scanner.analizar()

print("TOKENS:")
for t in scanner.tokens:
    print(t)

print("\nTABLA DE SÍMBOLOS:")
for s in scanner.tabla.mostrar():
    print(s)
