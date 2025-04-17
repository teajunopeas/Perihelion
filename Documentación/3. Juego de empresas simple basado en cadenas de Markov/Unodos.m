% Comprueba que la entrada sea 1 ó 2
function salida= Unodos()
salida=input('');
while salida~=1 && salida~=2
    fprintf('Ese valor no es correcto, debe ser 1 o 2\n')
    salida=input('');
end
end