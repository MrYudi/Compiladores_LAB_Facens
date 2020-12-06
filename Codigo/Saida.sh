#!/bin/bash
val=0
echo "primeiro valor"
read n1
echo "segundo valor"
read n2

echo "1.Adição"
echo "2.Subtração"
echo "3.Multiplicação"
echo "4.Divisão"

read opcao
case $opcao in
1)val=$(echo " $n1 + $n2" | bc -l)
echo $val;;
2)val=$(echo "$n1 - $n2" | bc -l)
echo $val;;
3)val=$(echo "$n1 * $n2" | bc -l)
echo $val;;
4)val=$(echo "$n1 / $n2" | bc -l)
echo $val;;
*)echo "escolha inválida"
esac
fi
done