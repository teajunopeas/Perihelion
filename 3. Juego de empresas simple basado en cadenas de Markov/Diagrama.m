function Diagrama(CME)


objsTextos = findobj(CME,'Type','text');  %Encuentra en el diagrama los textos

%El comando "get" devuelve propiedades y valores del objeto y el comando "set" los modifica

viejoStr = get(objsTextos,{'String'}); %Obtenemos los textos de las figuras

Nombre = {'ME:';'PE:';'PL:';'MO:'}; %Texto que aparece antes del porcentaje

nuevoStr = strcat(Nombre,viejoStr); %Compone el nuevo string con el nombre anterior seguido del porcentaje que ya tenía

set(objsTextos,{'String'},nuevoStr)
%Se rescribe con los objetos de textos nuevos sustituyendo los viejos

end









