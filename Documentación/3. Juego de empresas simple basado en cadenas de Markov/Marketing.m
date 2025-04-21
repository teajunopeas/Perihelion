%Efecto del Marketing.
function [CTOTAL,CM,PUB]=Marketing(i,j,CM,CTOTAL,PRESUPUESTO,Empresa,PUB,duracion)

if PRESUPUESTO (i,j)<=0

    fprintf('Si la empresa se encuentra en números rojos, no se permite realizar inversiones  \n')

else
    fprintf('¿Desea modificar la inversión en Marketing del mes pasado?')
    fprintf('\n1) Teclee un 1 si desea modificarla.')
    fprintf('\n2) Teclee un 2 si no desea modificarla.\n')
    modificacion= Unodos(); %Comprobamos si es 1 ó 2
    if modificacion==1

        fprintf('Introduzca la inversión en Marketing que desea realizar la empresa %s\n',Empresa(i))
        PUB(i,j)=input(''); %Pedimos la inversión en Marketing
        while PUB(i,j)<0  || PUB(i,j)> PRESUPUESTO(i,j)%La inversión en Marketing debe ser positiva (no entero) y está limitada por el presupuesto
            fprintf('Ese valor no es correcto, introduzca otra cantidad\n')
            fprintf('Debe ser positivo y no superior a su presupuesto actual: %.2f \n', PRESUPUESTO(i,j));
            PUB(i,j)=input('');
        end

        salida=1; %Variable de salida
        while PUB(i,j)==0 && salida==1
            fprintf('No se ha invertido nada en Marketing. ¿Es eso correcto?')
            fprintf('\n1) Teclee un 1 si es correcto.')
            fprintf('\n2) Teclee un 2 si desea modificar la cantidad.\n')
            nomodificacion= Unodos(); %Comprobamos si es 1 o 2

            if nomodificacion==2

                fprintf('Introduzca la cantidad que desea invertir la empresa %s\n',Empresa(i))
                PUB(i,j)=input('');
                while PUB(i,j)<0  || PUB(i,j)> PRESUPUESTO(i,j)%La inversion en Marketing debe ser positiva (no entero) y está limitada por el presupuesto
                    fprintf('Ese valor no es correcto, introduzca otro valor\n')
                    fprintf('Debe ser positivo y no superior a su presupuesto actual: %.2f \n', PRESUPUESTO(i,j));
                    PUB(i,j)=input('');
                end
            else
                salida=0;

            end

        end
    end

    %Las ventas son modificadas por el Marketing

    REF= max(PRESUPUESTO(:,j-1))/duracion;
    k_M=(0.2*CM(i,i))/log(1+(0.1*REF/(0.1*REF+1)));

    if PUB(i,j)>0.1*REF
        ICM=k_M*log(1+(0.1*REF/(0.1*REF+1)));
    else
        ICM=k_M*log(1+(PUB(i,j)/(0.1*REF+1)));
    end
% Al invertir en Marketing, cada una de las empresas influyen en las ventas del resto.
    for m=1:4; %Bucle en empresas
        if i==m  %Si la empresa m ha invertido
            CM(m,i)=CM(m,i)+ICM; %Sus ventas se incrementan en IV
            if CM(m,i)<0 %si es negativo lo hago cero y lo reparto entre los positivos
               CM(m,i)=0;
            end
        else 
            CM(m,i)=CM(m,i)-ICM/3; %Mientras que en el resto en incremento es en sentido contrario y equitativo
            if CM(m,i)<0 %si es negativo lo hago cero y lo reparto entre los positivos
               CM(m,i)=0;
            end
        end
    end
    scm=sum(CM(:,i));
    CM(:,i)= CM(:,i)/scm;
    CTOTAL(i,j)=CTOTAL(i,j)+PUB(i,j);
end
end