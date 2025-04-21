% Se detectan los términos negativos
function [V]=Negativo(V,j,a)
d=size(a);
Sumaneg= sum(V(a,j)); %Se suman todos los valores positivos
for m=1:4;
    if a(:)==m
        V(m,j)=0;
    else
        V(m,j)= V(m,j)-Sumaneg/(4-d(1));

    end
end
end

% Como se anulan estos valores negativos,
% el resto de empresas disminuirá sus ventas de forma proporcional 
% sin llegar a tener ventas negativas.