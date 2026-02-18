%{
#include <stdio.h>
%}

%%

"//".*                                ;
"/*"([^*]|\*+[^*/])*\*+"/"            ;

\"([^\\\n]|(\\.))*\"                  { printf("CADENA: %s\n", yytext); }

0[xX][0-9a-fA-F]+                     { printf("HEX: %s\n", yytext); }

[0-9]+[eE][+-]?[0-9]+                 { printf("CIENTIFICO: %s\n", yytext); }

[0-9]+"."[0-9]+                       { printf("FLOTANTE: %s\n", yytext); }

[0-9]+                                { printf("ENTERO: %s\n", yytext); }

"=="                                  { printf("IGUALDAD\n"); }
"!="                                  { printf("DIFERENTE\n"); }
"<="                                  { printf("MENOR_IGUAL\n"); }
">="                                  { printf("MAYOR_IGUAL\n"); }

"&&"                                  { printf("AND_LOGICO\n"); }
"||"                                  { printf("OR_LOGICO\n"); }
"!"                                   { printf("NOT\n"); }

"+"                                   { printf("SUMA\n"); }
"-"                                   { printf("RESTA\n"); }
"*"                                   { printf("MULT\n"); }
"/"                                   { printf("DIV\n"); }

"<"                                   { printf("MENOR\n"); }
">"                                   { printf("MAYOR\n"); }
"="                                   { printf("ASIGNACION\n"); }

[A-Za-z_][A-Za-z0-9_]*                { printf("IDENTIFICADOR: %s\n", yytext); }

[ \t\n]+                              ;

.                                     { printf("ERROR LEXICO: %s\n", yytext); }

%%

int main() {
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}
