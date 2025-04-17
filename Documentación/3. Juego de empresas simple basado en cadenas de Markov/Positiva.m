% COmprueba que la entrada sea mayor que cero.
function salida= Positiva()
salida=input('');
while salida<=0
    fprintf('Ese valor no es correcto, introduzca otra cantidad\n')
    salida=input('');
end
end