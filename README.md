# Лабораторная работа 3. Разработка синтаксического анализатора (парсера)
## Цель работы
Изучить назначение и принципы работы синтаксического анализатора в 
структуре компилятора. Спроектировать грамматику, построить соответствующую схему 
метода анализа грамматики и выполнить программную реализацию парсера с нейтрализацией 
синтаксических ошибок методом Айронса. Интегрировать разработанный модуль в ранее 
созданный графический интерфейс языкового процессора.
## Сведения об авторе
Лабораторную работу выполнила студентка группы АВТ-313, Ижболдина Виолетта
## Вариант задания
### Вариант:
87, Лямбда-выражение на языке Swift
### Примеры корректных строк: 
1. let calc = { (a: Int, b: Int, c: Int) -> Int in \
    return a + (b * c)\
};
2. let simple = { (s: String) -> String in return s };

## Разработка грамматики
1.     <START>  -> ‘LET’   <LET>
2.     <LET>   ->  ‘  ’   <SPACE_1>
3.     <SPACE_1> ->  <IDENTIFIER>   <VAR_NAME>
4.     <VAR_NAME>   ->  ‘=’   <ASSIGN>
5.     <ASSIGN>   -> { <LBRACE>
6.     <LBRACE>  ->(<LPAREN>
7.     <LPAREN>  ->  <PARAM> <PARAM_LIST>
8.     <PARAM>   -> <IDENTIFIER>   :   <TYPE>   
9.     <TYPE>   -> Int | String| Float  | Bool
10.     <PARAM_LIST> ->  , <LPAREN>  |  ) <RPAREN>
11.     <RPAREN>    ->   ->   <ARROW>
12.     <ARROW>  ->   <TYPE>   <RETURN_TYPE>
13.     <RETURN_TYPE>  ->   ‘ ’  <SPACE_2>
14.     <SPACE_2> ->   in  <IN> 
15.     <IN>   ->   ‘ ’  <SPACE_3>
16.     <SPACE_3>   ->  return  <RETURN>
17.     <RETURN>   ->  ‘  ’   <SPACE_4>
18.     <SPACE_4>   ->  <EXPR>  <CLOSE>
19.     <EXPR>    ->   <TERM> <EXPR_TAIL>
20.     <EXPR_TAIL>    ->   +  <TERM><EXPR_TAIL> | -<TERM> <EXPR_TAIL> | ε
21.     <TERM>  ->  <FACTOR>   <TERM_TAIL>
22.     <TERM_TAIL>    ->   * <FACTOR><TERM_TAIL> | /<FACTOR> <TERM_TAIL> | ε
23.     <FACTOR>   ->  <IDENTIFIER>  |  <NUMBER>  | (<EXPR> )
24.     <CLOSE>  -> } <END>
25.     <END>  ->  ;
26.     <IDENTIFIER>   ->  letter <ID_TAIL>
27.     <ID_TAIL>   ->  letter<ID_TAIL> | digit<ID_TAIL> | ε
28.     <NUMBER>   ->  digit <NUM_TAIL>
29.     <NUM_TAIL>   ->  digit<NUM_TAIL> | ε
## Классификация грамматики (по Хомскому).
Данная грамматика является контекстно-свободной.
## Метод анализа 
Выбран метод рекурсивного спуска. Это нисходящий алгоритм, 
где для каждого нетерминала грамматики создается отдельная функция.

## Диагностика и нейтрализация синтаксических ошибок
В программе реализован метод Айронса.

## Тестовые примеры
Корректная строка
![test1_lab3.jpg](images/test1_lab3.jpg)

Строка с одной ошибкой
![test2_lab3.jpg](images/test2_lab3.jpg)

Строка с несколькими ошибками
![test3_lab3.jpg](images/test3_lab3.jpg)

Строка без первого ключевого слова 
![test4_lab3.jpg](images/test4_lab3.jpg)