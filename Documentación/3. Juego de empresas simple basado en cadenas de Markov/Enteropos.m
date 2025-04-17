% Comprueba que la entrada sea un entero mayor o igual a cero.
function salida= Enteropos()
salida=input('');
entero=mod(salida,1);
while salida<0 || entero~=0
    fprintf('Ese valor no es correcto, introduzca otro valor\n')
    salida=input('');
    entero=mod(salida,1);
end
end