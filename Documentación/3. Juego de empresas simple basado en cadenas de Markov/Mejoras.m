
function [CTOTAL,CV,CM,mejoras]=Mejoras(i,j,CV,CTOTAL,PRESUPUESTO,Empresa,CM,mejoras,duracion)

if PRESUPUESTO(i,j)<=0

    fprintf('Si la empresa no tiene capital disponible, no se permite invertir en Mejoras Tecnológicas\n')

else
    fprintf('¿Desea modificar la inversión en Mejoras Tecnológicas del mes pasado?')
    fprintf('\n1) Teclee un 1 si desea modificarla.')
    fprintf('\n2) Teclee un 2 si no desea modificarla.\n')
    modificacion= Unodos(); %Comprobamos si es 1 ó 2
    
    if modificacion==1
    
        fprintf('Introduzca la inversión en Mejoras Tecnológicas que desea realizar la empresa %s\n',Empresa(i))
        mejoras(i,j)=input(''); %Se introduce la inversión
        while mejoras(i,j)<0|| mejoras(i,j)> PRESUPUESTO(i,j) %la inversión debe ser positiva (puede no ser entero)
            fprintf('Ese valor no es correcto, introduzca otra cantidad\n')
            fprintf('Debe ser positiva y no superior a su presupuesto actual: %.2f \n', PRESUPUESTO(i,j));
            mejoras(i,j)=input('');
        end

        salida=1; %Variable de salida

        while mejoras(i,j)==0 && salida==1
            fprintf('No se ha invertido nada en Mejoras Tecnológicas. ¿Es eso correcto?')
            fprintf('\n1) Teclee un 1 si es correcto.')
            fprintf('\n2) Teclee un 2 si desea modificar la cantidad.\n')
            nomodificacion= unodos(); %Comprobamos si es 1 ó 2

            if nomodificacion==2

                fprintf('Introduzca la cantidad que desea invertir la empresa %s\n',Empresa (i))
                mejoras(i,j)=input('');
                while mejoras(i,j)<0|| mejoras(i,j)> PRESUPUESTO(i,j) %la inversión debe ser mayor o igual a 0 (puede ser no entero)
                    fprintf('Ese valor no es correcto, introduzca otra cantidad\n')
                    fprintf('Debe ser positiva y no superior a su presupuesto actual: %.2f \n', PRESUPUESTO(i,j));
                    mejoras(i,j)=input('');
                end
            else
            salida=0;
            end
        end
    end
    REF=max(PRESUPUESTO(:,j-1))/duracion; % Esta variable "REF" representa el mayor presupuesto, 
    % que servirá de referencia para calcular la cantidad de costes variables que se disminuye.

    k_Tc=(0.05*CV(i,1))/log(0.075*REF+1);
    k_Tv=0.1;

    if mejoras(i,j) > 0.075*REF
        ICV=k_Tc*log(0.075*REF+1);
        ICM=k_Tv*CM(i,i);
    else
        ICV=k_Tc*log(mejoras(i,j)+1);
        ICM=k_Tv*mejoras(i,j)/0.075/REF*CM(i,i);
    end

    CV(i,j)=CV(i,j)-ICV; % "ICV" es la cantidad de costes variables que se "ahorra". 
    % "CV" representa los nuevos costes variables
    CTOTAL(i,j)=CTOTAL(i,j)+mejoras(i,j);
    
    for m=1:4; %Bucle en empresas
        if i==m  %Si la empresa m ha invertido en mejoras tecnológicas
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
end
end
