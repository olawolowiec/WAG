# WAG - working and grounded

CEL
Celem projektu jest stworzenie własnego, interpretowanego języka programowania przy użyciu technologii Python. Prawdopodobnie nie będzie on równie dobry i szybki jak już istniejące języki, ale na pewno poszerzy naszą wiedzę i umiejętności programistyczne.

ZAŁOŻENIA
Jak sama nazwa wskazuje, chcemy aby język był działający i dostosowany do naszych realiów. Planujemy uzyskać to w następujących krokach:
1) Stworzenie Lexera, za pomocą którego zostanie przeprowadzona analiza leksykalna, dzielenie tekstu na tokeny
2) Stworzenie Parsera, za pomocą którego zostanie przeprowadzona analiza składniowa, zamiana listy tokenów w drzewo węzłów (AST)
3) Stworzenie Interpretera, który przy pomocy drzewa węzłów wykona program wejściowy
4) Planowana składnia języka - chcemy aby była prosta i funkcjonalna. Składnia będzie rozwijana wraz z powstawaniem języka, jednak poniżej zamieszczamy przykładowe fragmenty kodu:

function foo(a, b){
	print("a + b = ", a+b);
}

function add(a, b){
	return a+b;
}
