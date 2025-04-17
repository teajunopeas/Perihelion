function [PVP,CM]= PrecioVP(PVP,CM, Empresa, i,j,PVPini)

fprintf('Escriba el nuevo precio de venta al público de la empresa %s \n', Empresa(i))
PVPmod(i,j)=Positiva(); %Positivo (puede no ser entero)

salida=1; %Variable interna de salida de bucle

while PVPmod(i,j)==PVP(i,j) && salida==1;
    fprintf('No ha realizado modificación alguna al precio de venta. ¿Desea continuar?')
    fprintf('\n1) Escriba 1 si desea continuar.')
    fprintf('\n2) Escriba 2 si desea modificar el precio.\n')

    nomodificacion= Unodos(); %Se comprueba si es 1 ó 2.

    if nomodificacion==2
        fprintf('Escriba el nuevo precio de venta al público de la empresa %s\n', Empresa (i))
        PVPmod(i,j)=Positiva(); %Positivo (puede no ser entero)
    else
        salida= 0; %Salta del bucle si no se desea modificar el precio.
    end
end


if salida==1 %Si se han modificado los precios, variarán las ventas
    Vx=0.75*(PVP(i,j)-PVPmod(i,j))/PVPini;
    Vmod(i,j)=CM(i,i)/2*(Vx+sqrt(Vx^2+4)); % "PVPmod" es el nuevo precio de los productos
    ICM=Vmod(i,j)-CM(i,i); %"IV" es el incremento de ventas.
    PVP(i,j)=PVPmod(i,j); %Se fija precio definitivo igual al modificado

    for m=1:4; %Bucle en empresas
        if i==m %Si se trata de la empresa que modificó sus precios
            CM(m,i)=CM(m,i)+ICM; % Se incrementan las ventas de esta empresa
            if CM(m,i)<0 %si es negativo lo hago cero y lo reparto entre los positivos
               CM(m,i)=0;
            end
        else %Si no se trata de la empresa que modificó los precios
            CM(m,i)=CM(m,i)-ICM/3; %Las ventas de las otras empresas varían en sentido contrario equitativamente  
            if CM(m,i)<0 %si es negativo lo hago cero y lo reparto entre los positivos
               CM(m,i)=0;
            end
        end
    end
    scm=sum(CM(:,i));
    CM(:,i)= CM(:,i)/scm;
end
end

