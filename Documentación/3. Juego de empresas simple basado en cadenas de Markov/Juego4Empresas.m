clear all; %se vac�an todas las variables
clc %se limpia la pantalla de comandos

%% Cabecera del Programa


 fprintf('\nJuego de empresas para cuatro participantes\n')
 fprintf('\n')

%El usuario puede o cargar una partida antigua o comenzar una nueva

fprintf('�Desea cargar una partida anterior o empezar otra?\n')
fprintf('1) Escriba 1 para cargar una partida antigua.\n')
fprintf('2) Escriba 2 para comenzar una partida nueva.\n')

cargar = Unodos(); %Se comprobando que se ha seleccionado 1 � 2

Empresa=["Mercedes", "Peugeot", "Penhard-Levassor", "Mors"]; %cadena de caracteres para determinar nombre de cada empresa

%% Partida Antigua

if cargar==1 %Si se carga una partida antigua
    fprintf('�Qu� nombre tiene el fichero de entrada?\n')
    fprintf('1) Escriba 1 si tiene el nombre por defecto (Partida.dta).\n')
    fprintf('2) Escriba 2 si tiene otro nombre.\n')
    nombrec= Unodos();

    if nombrec==1
        F1=fopen('Partida.dta','rt');
        while F1==-1
            fprintf('No existe ninguna partida con ese nombre. Escriba el nombre de un fichero v�lido.\n')
            ficheroc=input('','s');
            F1=fopen(ficheroc,'rt');
        end

    else
        fprintf('Escriba el nombre del fichero\n');
        ficheroc=input('','s');
        F1=fopen(ficheroc,'rt');
        while F1==-1
            fprintf('El nombre introducido no es correcto. Vuelva a escribirlo\n')
            ficheroc=input('','s');
            F1=fopen(ficheroc,'rt');
        end
    end

    %fscanf(F1,'%s',23);%Lectura de una cadena en F1 contando 23 entidades, es decir, empezando en la 24.
    [UD]=fscanf(F1,'\n %9d       %9d     %9d    %9d,  ');%N�mero entero con 9 caracteres
    %fscanf(F1,'%s',6);
    [V]=fscanf(F1,'%9d       %9d     %9d    %9d,   ');
    ventasmax=sum(V);
    %fscanf(F1,'%s',6);
    [Ventasreales]=fscanf(F1,'%9d       %9d     %9d    %9d,   ');
    %fscanf(F1,'%s',6);
    [VENTASPENDIENTES]=fscanf(F1,'%9d       %9d     %9d    %9d,   ');
    %fscanf(F1,'%s',5);
    [PVP]=fscanf(F1,'%10f          %10f     %10f    %10f,   ');%N�mero decimal con 10 caracteres
    pvpini=sum(PVP)/4;
    %fscanf(F1,'%s',4);
    [CF]=fscanf(F1,'%10f          %10f     %10f    %10f,   ');
    %fscanf(F1,'%s',4);
    [CV]=fscanf(F1,'%10f          %10f     %10f    %10f,   ');
    %fscanf(F1,'%s',5);
    [STOCK]=  fscanf(F1,'%9d       %9d     %9d    %9d,   ');
    %fscanf(F1,'%s',23);
    [CALM]=  fscanf(F1,'%9d       %9d     %9d    %9d,   ');
    %fscanf(F1,'%s',23);
    [CNOSERV]=  fscanf(F1,'%9d       %9d     %9d    %9d,   ');
    %fscanf(F1,'%s',23);
    [CRUPT]=  fscanf(F1,'%9d       %9d     %9d    %9d,   ');
    %fscanf(F1,'%s',23);
    [INGRESOS]= fscanf(F1,'%14f             %14f         %14f           %14f, ');
    %fscanf(F1,'%s',4);
    [CTOTAL]= fscanf(F1,'%14f             %14f         %14f           %14f, ');
    %fscanf(F1,'%s',3);
    [PRESUPUESTO]= fscanf(F1,'%14f             %14f         %14f           %14f, ');
    %fscanf(F1,'%s',7)
    CM1= fscanf(F1,'%f %f %f %f');
    fscanf(F1,'%s',1);
    CM2=    fscanf(F1,'%f %f %f %f');
    fscanf(F1,'%s',1);
    CM3=    fscanf(F1,'%f %f %f %f');
    fscanf(F1,'%s',1);
    CM4=    fscanf(F1,'%f %f %f %f');
    fscanf(F1,'%s',1);
    CM=[CM1 CM2 CM3 CM4]; % Matriz de Markov
    CM=CM';
    %fscanf(F1,'%s',6);
    [Calm]= fscanf(F1,'%f %f %f %f'); % Coste de Almacenamiento
    fscanf(F1,'%s',1);
    %D=fscanf(F1,'%s',5);
    %cf= fscanf(F1,'%12f');  % Coste Fijo
    %A=fscanf(F1,'%s',2);
    ruptadm= fscanf(F1,'%d');% Ruptura Admitida
    fscanf(F1,'%s',1);
    if ruptadm==2 %el cliente no est� dispuesto a esperar
    %    fscanf(F1,'%s',13);
        [Crupt]=fscanf(F1,'%f %f %f %f'); % Coste de Ruptura
    %    fscanf(F1,'%s',1);
    else          %el cliente s� est� dispuesto a esperar
    %    fscanf(F1,'%s',13);
        [Cnoserv]=fscanf(F1,'%f %f %f %f'); % Coste de NO Servicio
    %    fscanf(F1,'%s',1);
    end
    fclose(F1);
    %clc;

   
%% Datos obtenidos de la Partida Antigua
    
    fprintf('\n---------------------------------------------------------------------------------')
    fprintf('\n                  Datos Almacenados de la partida antigua ')
    fprintf('\n---------------------------------------------------------------------------------')

    fprintf('\n\n\n ________________________________________________________________________________________')
    fprintf('\n|                       |                            Empresa                             |')
    fprintf('\n|         Datos         |________________________________________________________________|')
    fprintf('\n|                       |    Mercedes    |    Peugeot   |Penhard-Levassor|      Mors     |')
    fprintf('\n|_______________________|________________|______________|________________|_______________|')
    fprintf('\n|  Unidades fabricadas  | %9d      | %9d    | %9d      | %9d     |',UD(1,1),UD(2,1),UD(3,1),UD(4,1));
    fprintf('\n| Demanda de la empresa | %9d      | %9d    | %9d      | %9d     |',V(1,1),V(2,1),V(3,1),V(4,1))
    fprintf('\n| Ventas de la empresa  | %9d      | %9d    | %9d      | %9d     |',Ventasreales(1,1),Ventasreales(2,1),Ventasreales(3,1),Ventasreales(4,1))
    fprintf('\n|  Clientes en espera   | %9d      | %9d    | %9d      | %9d     |',VENTASPENDIENTES(1,1),VENTASPENDIENTES(2,1),VENTASPENDIENTES(3,1),VENTASPENDIENTES(4,1))
    fprintf('\n|    Precio de venta    |     %8.2f   |     %8.2f |     %8.2f   |     %8.2f  |',PVP(1,1),PVP(2,1),PVP(3,1),PVP(4,1))
    fprintf('\n|     Costes fijos      | %9d      | %9d    | %9d      | %9d     |',CF(1,1),CF(2,1),CF(3,1),CF(4,1))
    fprintf('\n|   Costes variables    |     %8.2f   |     %8.2f |     %8.2f   |     %8.2f  |',CV(1,1),CV(2,1),CV(3,1),CV(4,1))
    fprintf('\n|   Unidades en stock   | %9d      | %9d    | %9d      | %9d     |',STOCK(1,1),STOCK(2,1),STOCK(3,1),STOCK(4,1))
    fprintf('\n|    Costes de stock    | %9d      | %9d    | %9d      | %9d     |',CALM(1,1),CALM(2,1),CALM(3,1),CALM(4,1))
    fprintf('\n| Costes de no servicio | %9d      | %9d    | %9d      | %9d     |',CNOSERV(1,1),CNOSERV(2,1),CNOSERV(3,1),CNOSERV(4,1))
    fprintf('\n|   Costes de ruptura   | %9d      | %9d    | %9d      | %9d     |',CRUPT(1,1),CRUPT(2,1),CRUPT(3,1),CRUPT(4,1))
    
    fprintf('\n|_______________________|________________|______________|________________|_______________|')
    %  "%8.2f" 6 n�meros enteros y 2 decimales
    fprintf('\n\n\n _________________________________________________________________________________________________________')
    fprintf('\n|                 |                                         Empresa                                       |')
    fprintf('\n|   Resultados    |_______________________________________________________________________________________|')
    fprintf('\n|                 |      Mercedes      |       Peugeot      |  Penhard-Levassor   |          Mors         |')
    fprintf('\n|_________________|____________________|____________________|_____________________|_______________________|')
    fprintf('\n| Ingresos        |  %12.2f      |  %12.2f      |  %12.2f       |  %12.2f         |',INGRESOS(1,1),INGRESOS(2,1),INGRESOS(3,1),INGRESOS(4,1))
    fprintf('\n| Costes totales  |  %12.2f      |  %12.2f      |  %12.2f       |  %12.2f         |',CTOTAL(1,1),CTOTAL(2,1),CTOTAL(3,1),CTOTAL(4,1))
    fprintf('\n| Presupuesto     |  %12.2f      |  %12.2f      |  %12.2f       |  %12.2f         |',PRESUPUESTO(1,1),PRESUPUESTO(2,1),PRESUPUESTO(3,1),PRESUPUESTO(4,1))
    fprintf('\n|_________________|____________________|____________________|_____________________|_______________________| \n')

    fprintf('\n La Matriz de Markov es: [ %.2f %.2f %.2f %.2f; %.2f %.2f %.2f %.2f; %.2f %.2f %.2f %.2f; %.2f %.2f %.2f %.2f]', CM(1,1),CM(1,2),CM(1,3),CM(1,4),CM(2,1),CM(2,2),CM(2,3),CM(2,4),CM(3,1),CM(3,2),CM(3,3),CM(3,4),CM(4,1),CM(4,2),CM(4,3),CM(4,4));
    fprintf('\n El coste de almacenamiento es %4.2f %4.2f %4.2f %4.2f Francos.',Calm(1,1),Calm(2,1),Calm(3,1),Calm(4,1));
    %fprintf(', El coste fijo es %.2f Francos.',cf);
    if ruptadm==2 %el cliente no est� dispuesto a esperar
        fprintf('\n (rupdtadm= 2)El cliente no est� dispuesto a esperar con un coste de ruptura de %.2f %.2f %.2f %.2f',Crupt(1,1),Crupt(2,1),Crupt(3,1),Crupt(4,1));
    else          %el cliente s� est� dispuesto a esperar
        fprintf('\n (rupdtadm= 1)El cliente est� dispuesto a esperar con un coste de no servicio de %.2f %.2f %.2f %.2f',ruptadm(1,1),Cnoserv(2,1),Cnoserv(3,1),Cnoserv(4,1));
    end
    fprintf('\n\nIntroduzca la nueva duración del juego en meses:\n')
    duracion=input('');
    entero=mod(duracion,1); % dividir entre 1 y escoger el resto
    while duracion<=0 || entero~=0
        fprintf('La duración elegida no es v�lida. Escriba otro valor.\n')
        duracion=input('');
        entero=mod(duracion,1);
    end
else %cargar==2 (partida nueva)
   
%% Partida Nueva

    %clc;
    fprintf('                Introducción de los datos de partida     \n')
    fprintf('____________________________________________________________________________\n\n')
    fprintf('\nEste juego est� dise�ado para cuatro empresas participantes.')
    fprintf('\nLas condiciones iniciales de partida serán iguales para cada empresa.')
    fprintf('\nLos datos que se introducirán a continuación serán la referencia para empezar la partida.\n')

    %Se solicitan una serie de datos y se comprueba que se cumplan unos requisitos
    fprintf('\nEscriba la duración del juego en meses:\n')
    duracion=input('');
    entero=mod(duracion,1);
    while duracion<=0 || entero~=0
        fprintf('La duración elegida no es v�lida. Escriba otro valor.\n')
        duracion=input('');
        entero=mod(duracion,1);
    end

    %Dimensionamiento de matrices en función de la empresa y el mes

    PRESUPUESTO=zeros (4,duracion+1); %Prespuesto de cada empresa (desde el mes 0 al mes = duración)
    V=zeros (4,duracion+1); %Ventas de cada empresa (desde el mes 0 al mes = duración)
    PVP=zeros (4,duracion+1);% Precio del producto de cada empresa (desde el mes 0 al mes = duración)
    CV=zeros (4,duracion+1);% Coste variable unitario por producto de cada empresa (desde el mes 0 al mes = duración)
    CF=zeros (4,duracion+1);% Coste fijo unitario por producto de cada empresa (desde el mes 0 al mes = duración)
    ventasmedia=zeros (4,1); % Función que determina el valor medio de ventas
    STOCK =zeros(4,duracion+1); %Cantidad en stock de cada producto por empresa y mes (desde el mes 0 al mes = duración)
    INGRESOS=zeros(4,duracion+1); %Ingresos de cada empresa por mes (desde el mes 0 al mes = duración)
    sobran=zeros(4,duracion+1); %Unidades de exceso de fabricación de cada producto (desde el mes 0 al mes = duración)
    faltan=zeros(4,duracion+1);%Unidades de defecto de fabricación de cada producto (desde el mes 0 al mes = duración)
    UD=zeros(4,duracion+1); %Unidades fabricadas de cada producto (desde el mes 0 al mes = duración)
    CTOTAL=zeros(4,duracion+1); %Coste total para cada empresa (desde el mes 0 al mes = duración)
    Calm=zeros(4,duracion+1); %Coste almacenamiento para cada empresa (desde el mes 0 al mes = duración)
    Cnoserv=zeros(4,duracion+1); %Coste de no servicio para cada empresa (desde el mes 0 al mes = duración)
    Crupt=zeros(4,duracion+1); %Coste de ruptura para cada empresa (desde el mes 0 al mes = duración)

    fprintf('\nEscriba el valor de la demanda total del mercado:\n')
    ventasmax=Enteropos(); %Debe ser entero y positivo.

    fprintf('\nEscriba el precio de venta al p�blico inicial del producto (precio de referencia):\n')
    pvp= Positiva(); %Debe ser mayor que 0.
    pvpini=pvp;

    for i=1:4
    fprintf('\nEscriba la cantidad inicial de presupuesto disponible por la empresa %s:\n', Empresa(i))
    presupuesto=Positiva(); %Debe ser mayor que 0.
    PRESUPUESTO(i,1)=presupuesto; % Se guarda el presupuesto de la Empresa en la variable "PRESUPESTO"
    
    PVP(i,1)=pvp; % En la primera columna se introduce el PVP del producto de cada empresa

    fprintf('\nEscriba el coste fijo de la empresa %s: \n', Empresa(i))
    %fprintf('\nT�ngase en cuenta que este valor permanecerá constante durante toda la partida')
    %fprintf('\npor tratarse de un mismo producto, mismos materiales y misma estrategia de referencia.\n')
    cf= Positiva(); %Debe ser mayor que cero y puede no ser entero.
    CF(i,1)=cf; % Se hace lo mismo con los costes variables en "CF".

    fprintf('\nEscriba el coste variable por cada unidad fabricada de la empresa %s: \n', Empresa(i))
    %fprintf('\nTenga en cuenta que al inicio será igual en todas, pero puede variar a lo largo de la partida.\n')
    cv= Positiva(); %Debe ser mayor que cero y puede no ser entero.
    CV(i,1)=cv; % Se hace lo mismo con los costes variables en "CV".

    fprintf('\nEscriba el coste de almacenamiento por unidad de la empresa %s:\n', Empresa(i))
    calm=Positiva(); %Debe ser mayor que cero y puede no ser entero.
    Calm(i,1)=calm; % Se hace lo mismo con los costes de almacenamiento en "Calm".

    fprintf('En caso de ruptura, �Se permite entregar el pedido en el siguiente per�odo?\n')
    fprintf('1) Escriba 1 en caso afirmativo.\n')
    fprintf('2) Escriba 2 en caso contrario.\n')
    ruptadm= Unodos(); % Debe ser 1 � 2.

    if ruptadm==1 %Si el cliente est� dispuesto a esperar
        fprintf('\nEscriba el coste de no servicio de la empresa %s:\n', Empresa(i))
        cnoserv=Positiva(); %mayor que cero y puede ser no entero
        Cnoserv(i,1)=cnoserv;

    else  %ruptadm==2, por lo que el cliente no est� dispuesto a esperar
        fprintf('\nEscriba el coste de ruptura de la empresa %s:\n', Empresa(i))
        crupt=Positiva(); %mayor que cero y puede ser no entero
        Crupt(i,1)=crupt;
    end
    end
    %Matriz de Cadena de Markov inicial (completamente equitativa). 
    %Se divide la unidad en 4 partes iguales para cada una de las empresas.

    CM=[0.25 0.25 0.25 0.25; 0.25 0.25 0.25 0.25; 0.25 0.25 0.25 0.25; 0.25 0.25 0.25 0.25];

    %Se establecen los precios, presupuesto, costes y ventas del primer mes
    ventasmedia(:)=ventasmax/4; % Lee la matriz "ventasmedia" y carga en cada uno de sus valores "ventasmax/4"
    V(:,1)=fix(ventasmedia); % Truncar las ventas medias a un valor entero (escoger sólo la parte entera)
    ventasahora=sum(V(:,1)); % Sumo los valores después del truncamiento
    ventasquedan=ventasmax-ventasahora; % Diferencia entre las ventas máximas establecidas del mercado y las ventas divisibles entre las 4 empresas.
    saco=zeros(4);
    while ventasquedan~=0
        suerte= fix(4*rand(1)+1); % sorteo de las unidades que no sean divisibles. "rand (1)" Matriz Aleatoria.
        % Empresa 1:0-0.25; Empresa 2: 0.25-0.5; Empresa 3: 0.5-0.75; Empresa 4: 0.75-1.
        % Se multiplican estas cantidades por 4 y se le suman 1:
        % Empresa 1: 1-2; Empresa 2: 2-3; Empresa 3: 3-4; Empresa 4: 4-5.
        % Al truncar nos quedamos sólo con el primer valor del rango.
        if saco(suerte)==0 %hacemos que le toque cada vez a una diferente
            V(suerte,j)=V(suerte,j)+1; %y se le suma a la que le toque,
            ventasquedan=ventasquedan-1; %y se resta de las venta pendientes hasta que se agoten
            saco(suerte)=1;
        end
    end

    
    

end

F2=fopen('HISTORIAL.dta','w+t'); % Se crea con 'w+t' un archivo de texto

%Núcleo del programa. Parte de modificación de precios, publicidad,...

VENTASPENDIENTES=zeros(4,duracion+1);% Ventas debido a la espera
Ventasreales=zeros(4,duracion+1);% Ventas realmente efectuadas en ese mes
CRUPT=zeros (4,duracion+1); % Coste de ruptura total por empresa y mes
CALM=zeros (4,duracion+1); % Coste de almacenamiento total por empresa y mes
PUB=zeros (4,duracion+1); % Inversión en Marketing
mejoras=zeros(4,duracion+1);
CNOSERV= zeros(4,duracion+1); % Coste de no servicio (desde el mes 0 al mes = duración)

for j=2:1:duracion+1 %Bucle desde el mes 1 (j=2) hasta el último (j=duracion+1).
    %Antes de la modificación, los precios del nuevo mes son los mismos del final del anterior
    %Lo mismo con el resto de variables (ventas, costes, presupuesto, stock...)
    % Se copia el dato del mes anterior en el mes actual para cada una:
    PVP(:,j)=PVP(:,j-1); 
    CV(:,j)=CV(:,j-1); 
    PRESUPUESTO(:,j)= PRESUPUESTO(:,j-1); 
    CMprev=CM; 
    V(:,j)=V(:,j-1); 
    STOCK(:,j)=STOCK (:,j-1); 
    PUB(:,j)=PUB(:,j-1);
    mejoras(:,j)=mejoras(:,j-1);
    CTOTAL(:,j)=0; % inicialmente deben ser cero los costes totales


   
%% Estimación de incremento o decremento de la demanda

%clc;
    fprintf('\n\n                   Comienzo del mes %d         \n',j-1)% "j-1" es el mes que comienza
    fprintf('__________________________________________________________________')
    fprintf('\n\n Se supone que previamente las empresas han realizado un estudio del mercado')
    fprintf('\n que les permite estimar la variación de la demanda en el sector y así valorar cuántas unidades fabricar.')
    fprintf('\n Como resultado:')
    fprintf('\n Se estimará una variación en porcentaje respecto al mes %d, donde el número de ventas fue %d', j-2,ventasmax);%"j-2" es el mes anterior

    fprintf('\n\n EJEMPLO: Si se estima que la demanda variará entre un -10%% y un 5%%');
    fprintf('\n          Se dirá que variaciónn de demanda mínima será -10 (valor expresado en porcentaje).');
    fprintf('\n          Mientras que la variación de demanda máxima será 5 (también expresado en porcentaje).');

    fprintf('\n\n Suponiendo que la demanda no aumentará a más del doble ni disminuirá a menos de la mitad (Intervalo entre -50%% y 200%%)');


    fprintf('\n\n\n Incremento estimado de demanda mínimo (en porcentaje):\n');
    dem_minima=input('');  %Incremento mínimo de demanda (en porcentaje)
    entero=mod(dem_minima,1); % El porcentaje debe ser un valor entero
    while dem_minima< -50 || dem_minima > 200 || entero~=0
        fprintf('\n La demanda mínima del mercado esperada debe tomar un valor entero entre -50 y 200.\n')
        fprintf('El valor introducido no es correcto. Escriba otro porcentaje.\n')
        dem_minima=input('');
        entero=mod(dem_minima,1);
    end


    fprintf ('\n\n\n Incremento estimado de demanda m�ximo (en porcentaje):\n');
    dem_maxima=input(''); %Incremento m�ximo de demanda (en porcentaje)
    entero=mod(dem_maxima,1);  % El porcentaje debe ser un valor entero
    while dem_maxima< -50 || dem_maxima > 200 || entero~=0 || dem_minima>dem_maxima
        fprintf('La demanda m�xima del mercado esperada debe tomar un valor entero entre -50 y 200 e igual o superior a la demanda m�nima\n')
        fprintf('El valor introducido no es correcto. Escriba otro porcentaje.\n')
        dem_maxima=input('');
        entero=mod(dem_maxima,1);
    end

    %la demanda m�nima y la m�xima en ventas se obtiene redondeando
    demandaminima = round(ventasmax*(100+dem_minima)/100); 
    demandamaxima = round(ventasmax*(100+dem_maxima)/100);

        %clc;  
    for i=1:4    
        
%% Introducción de Datos para el Comienzo del Juego
        
        fprintf('\n               Empresa: %s                   Pr�ximo mes: %d \n', Empresa(i),j-1);
        fprintf('___________________________________________________________________________\n')

        fprintf('\n La demanda del mercado se estima que estará entre %d y %d.', demandaminima,demandamaxima);
        fprintf('\n Durante el pasado mes esta empresa %s vendi� %d de las %d que se vendieron en total.', Empresa(i), V(i,j-1), ventasmax);
        fprintf('\n El presupuesto (capital disponible) actual de la empresa es de %.2f Francos.',PRESUPUESTO(i,j-1))
        fprintf('\n En stock quedan %d unidades.',STOCK(i,j-1))
        fprintf('\n El coste de almacenamiento es %.2f Francos por unidad.',Calm(i,1));
        fprintf('\n Los costes variables en el ultimo mes fueron de %.2f Francos por unidad.',CV(i,j-1));
        if ruptadm==2 %El cliente no est� dispuesto a esperar
            fprintf('\n El clientes no est� dispuesto a esperar con un coste ruptura de %.2f',Crupt(i,1))
        else          %El cliente s� est� dispuesto a esperar
            fprintf('\n El cliente est� dispuesto a esperar con un coste de no servicio de %.2f',Cnoserv(i,1))
        end

        fprintf('\n Teniendo en cuenta las estrategias que se llevarán a cabo durante este mes,\n');
        fprintf('�cu�ntas unidades desea poner a la venta? \n');
        UD(i,j)=Enteropos(); %Se comprueba que sea un entero mayor o igual a 0

        modA=8; % Valor cualquiera distinto de cero para entrar en el bucle
        while modA~=0  %Se muestra por pantalla las posibles estrategias a realizar

            fprintf('\n Establezca la estrategia de la Empresa %s para el mes %d', Empresa(i),j-1);
            fprintf('\n1) Escriba 1 si desea modificar su Precio (precio hasta el momento= %.2f).', PVP(i,j));
            fprintf('\n2) Escriba 2 si desea invertir en Marketing.');
            fprintf('\n3) Escriba 3 si desea invertir en Mejoras Tecnol�gicas');
            fprintf('\n4) Escriba 4 si desea modificar las Unidades que se pretenden vender');
            fprintf('\n\n -------------------- Escriba 0 si no desea hacer nada --------------------\n');


            modA=input('');%Se comprueba si la elección es una entrada v�lida

            while modA~=1 && modA~=2 && modA~=3 && modA~=4 && modA~=0
                fprintf('La elección no es correcta. Escriba un entero entre 0 y 4.\n')
                modA=input('');
            end

            switch modA, % Determina qu� variable se va a comprobar (valores introducidos entre 0 y 4 de modA)
                case 1,%Si se elige 1 (modificar Precios)
                    [PVP,CM]= PrecioVP(PVP,CM,Empresa, i,j,pvpini);
                    % [PVP,V] --> variables que me devuelve la subrutina PrecioVP
                    % (PVP,V,Empresa,i,j,pvpini) --> variables necesarias
                    % para que se ejecute la subrutina PrecioVP

                case 2,%Si se elege 2 (invertir en Marketing)
                    [CTOTAL,CM,PUB]= Marketing(i,j,CM,CTOTAL,PRESUPUESTO,Empresa,PUB,duracion);

                case 3, %Si se elige 3 (invertir en Mejoras Tecnol�gicas)
                    [CTOTAL,CV,CM,mejoras]=Mejoras(i,j,CV,CTOTAL,PRESUPUESTO,Empresa,CM,mejoras,duracion);

                case 4, %Si se elige 4 (modificar N�mero de Unidades)
                    fprintf('\n\n �Cuantas unidades se pondrán a la venta este mes? \n');
                    UD(i,j)=Enteropos(); %Se comprueba que sea un n�mero entero positivo 
            end
        end
        
       

        %Cuando la empresa ya ha modificado sus estrategias, 
        %se comprueba que no existen ventas negativas

        a=find (V (:,j)<0); %Encuentra la posición de los valores negativos.

        if isempty(a)==0 % Matriz no nula, por lo que existen valores negativos. Si no hubiera valores negativos, la matriz seráa nula.

            [V]=Negativo(V,j,a); %Esta función detecta los valores negativos de las ventas 
            % y los sustituye por 0. Las unidades negativas las distribuye de forma
            % equitativa entre el resto de empresas.
        end

        %Despu�s de obtener las nuevas ventas partiendo de la empresa que
        %se est� analizando, se modifica la cadena de Markov de forma "ficticia" 
        %y s�lo teniendo en cuenta las estrategias propias, no las del resto.
        %CM(:,i)=V(:,j)/sum(V(:,j));
        %CM(:,i)=(V(:,j)+CM(:,i)*V(i,j)-CM*V(:,j))/V(i,j);
    end
    % Hasta ahora se han analizado las empresas una a una. 
    % Ahora se empiezan a analizar todas en conjunto.

    %CM= CM*CMprev; %la cadena de Markov será la anterior
    %%%%%%%%% multiplicada por la nueva ficticia creada. ????????

    %Modificación real de la demanda
    aleatorio=rand(1); % 0 --> demanda m�nima; 1 --> demanda m�xima
    porc_suerte= dem_minima + (dem_maxima-dem_minima)*aleatorio; % Porcentaje aleatorio de la demanda entre m�nima y m�xima.
    ventasmax=round(ventasmax*(100+porc_suerte)/100); %Ventas m�ximas del mercado redondeadas.
    [EVect,EVal]=eig(CM);
    cont1=1;
    while (1-EVal(cont1,cont1))^2>1e-10 %B�squeda del autovalor unitario (con cierta tolerancia)
        cont1=cont1+1;
    end
    Norma=sum(EVect(:,cont1));
    PV(:)=EVect(:,cont1)/Norma;
    ventasmedia(:,1)=PV(:)*ventasmax;
    
    %ventasmedia(:,1)=V(:,j-1)*(100+porc_suerte)/100; %Ventas de la empresa (ventas del mes anterior + lo que se incremente o disminuya en este mes)
    %ventasmedia(:,1)=V(:,j)*ventasmax/sum(V(:,j));

    %V(:,j)=fix(CM*ventasmedia); %Te�ricas ventas reales (redondeadas)
    V(:,j)=fix(ventasmedia); %Te�ricas ventas reales (redondeadas)
    ventasahora=sum(V(:,j)); % Se suman todas las ventas.
    ventasquedan=ventasmax-ventasahora;
    saco=zeros(4);
    while ventasquedan>0  %Mientras queden ventas por realizar (mercado no divisible entre 4)
        suerte= fix(4*rand(1)+1); %Se sortean entre las empresas 
        if saco(suerte)==0
            V(suerte,j)=V(suerte,j)+1; %y se le suma a la que le toque,
            ventasquedan=ventasquedan-1; %y se resta de las venta pendientes hasta que se agoten
            saco(suerte)=1;
        end
    end

    Ventasreales(:,j)=V(:,j)+VENTASPENDIENTES(:,j-1);%"V" es el vector de ventas de la demanda
    % "VENTASPENDIENTES" es el vector de las ventas que no se han
    % realizado el mes anterior y que est�n pendientes de los clientes que
    % est�n dispuestos a esperar.
    for i=1:4 %Bucle en empresas
        if UD(i,j)< Ventasreales(i,j) %Si se han fabricado menos unidades de las que se deben vender
            faltan(i,j)=Ventasreales(i,j)-UD(i,j); % Unidades que faltan por vender
            while STOCK(i,j)>0 && faltan(i,j)>0 % Se vende de lo que queda en STOCK hasta que ya no queden
                %m�s existencias o unidades que vender.
                STOCK(i,j)=STOCK(i,j)-1;
                faltan(i,j)=faltan(i,j)-1;
            end


            if faltan(i,j)>0 %Si incluso as� no se atiende a toda la demanda
                %se comprueba si el cliente est� dispuesto a esperar
                Ventasreales(i,j)=Ventasreales(i,j)-faltan(i,j);

                if ruptadm==2 %Si el cliente no est� dispuesto a esperar
                    CRUPT(i,j)=faltan(i,j)*Crupt(i,1); %Se tendrá un coste de ruptura
                else %Si el cliente est� dispuesto a esperar
                    CNOSERV(i,j)=faltan(i,j)*Cnoserv(i,1); %hay un coste de No Servicio.
                    VENTASPENDIENTES(i,j)=faltan(i,j); %Y quedan ventas pendientes para el mes siguiente.
                end
            end
            CALM(i,j)=STOCK(i,j)*Calm(i,1);
        elseif UD(i,j)> Ventasreales(i,j) %Si se han fabricado m�s unidades de las vendidas

            sobran(i,j)=UD(i,j)-Ventasreales(i,j);
            STOCK(i,j)=STOCK(i,j)+sobran(i,j);
            CALM(i,j)=STOCK(i,j)*Calm(i,1);

        else % UD==Ventas reales

            STOCK(i,j)=STOCK(i,j-1);
            CALM(i,j)=STOCK(i,j)*Calm(i,1);

        end

        INGRESOS(i,j)= PVP(i,j)*Ventasreales(i,j);

        CTOTAL(i,j)=CTOTAL(i,j)+CF(i,1)+CV(i,j)*UD(i,j)+CALM(i,j)+CRUPT(i,j)+CNOSERV(i,j);
        PRESUPUESTO(i,j)=PRESUPUESTO(i,j)+INGRESOS(i,j)-CTOTAL(i,j);
    end
    %clc;

    
%% Tabla Resumen de Producción

    
    fprintf('\n\n\n _____________________________________________________________________________________________')
    fprintf('\n|                       |                            Empresa                                  |')
    fprintf('\n|       Datos           |_____________________________________________________________________|')
    fprintf('\n|                       |       Mercedes     |   Peugeot    |Penhard-Levassor|     Mors       |')
    fprintf('\n|_______________________|____________________|______________|________________|________________|')
    fprintf('\n|  Unidades fabricadas  |    %9d       | %9d    | %9d      | %9d      |',UD(1,j),UD(2,j),UD(3,j),UD(4,j));
    fprintf('\n| Demanda de la empresa |    %9d       | %9d    | %9d      | %9d      |',V(1,j),V(2,j),V(3,j),V(4,j));
    fprintf('\n|  Ventas de la empresa |    %9d       | %9d    | %9d      | %9d      |',Ventasreales(1,j),Ventasreales(2,j),Ventasreales(3,j),Ventasreales(4,j))
    fprintf('\n|  Clientes en espera   |    %9d       | %9d    | %9d      | %9d      |',VENTASPENDIENTES(1,j),VENTASPENDIENTES(2,j),VENTASPENDIENTES(3,j),VENTASPENDIENTES(4,j));
    fprintf('\n|   Precio de venta     |        %8.2f    |     %8.2f |     %8.2f   |     %8.2f   |',PVP(1,j),PVP(2,j),PVP(3,j),PVP(4,j));
    fprintf('\n|     Costes fijos      |    %9d       | %9d    | %9d      | %9d      |',CF(1,1),CF(2,1),CF(3,1),CF(4,1));
    fprintf('\n|   Costes variables    |        %8.2f    |     %8.2f |     %8.2f   |     %8.2f   |',CV(1,j),CV(2,j),CV(3,j),CV(4,j));
    fprintf('\n|   Unidades en stock   |    %9d       | %9d    | %9d      | %9d      |',STOCK(1,j),STOCK(2,j),STOCK(3,j),STOCK(4,j));
    fprintf('\n|    Costes de stock    |    %9d       | %9d    | %9d      | %9d      |',CALM(1,j),CALM(2,j),CALM(3,j),CALM(4,j));
    fprintf('\n| Costes de no servicio |    %9d       | %9d    | %9d      | %9d      |',CNOSERV(1,j),CNOSERV(2,j),CNOSERV(3,j),CNOSERV(4,j));
    fprintf('\n|   Costes de ruptura   |    %9d       | %9d    | %9d      | %9d      |',CRUPT(1,j),CRUPT(2,j),CRUPT(3,j),CRUPT(4,j));
    fprintf('\n|_______________________|____________________|______________|________________|________________|')

%% Tabla Resumen de Cuentas

    
    fprintf('\n\n\n _________________________________________________________________________________________________________')
    fprintf('\n|                 |                                          Empresa                                      |')
    fprintf('\n|   Resultado     |_______________________________________________________________________________________|')
    fprintf('\n|                 |       Mercedes     |       Peugeot      |  Penhard-Levassor   |         Mors          |')
    fprintf('\n|_________________|____________________|____________________|_____________________|_______________________|')
    fprintf('\n| Ingresos        |  %12.2f      | %12.2f       |  %12.2f       |    %12.2f       |',INGRESOS(1,j),INGRESOS(2,j),INGRESOS(3,j),INGRESOS(4,j));
    fprintf('\n| Costes totales  |  %12.2f      | %12.2f       |  %12.2f       |    %12.2f       |',CTOTAL(1,j),CTOTAL(2,j),CTOTAL(3,j),CTOTAL(4,j));
    fprintf('\n| Presupuesto     |  %12.2f      | %12.2f       |  %12.2f       |    %12.2f       |',PRESUPUESTO(1,j),PRESUPUESTO(2,j),PRESUPUESTO(3,j),PRESUPUESTO(4,j));
    fprintf('\n|_________________|____________________|____________________|_____________________|_______________________| \n')

    %Escribinos un HISTORIAL para que todos los meses queden archivados.
    fprintf(F2,'\n El coste de almacenamiento es %4.2f %4.2f %4.2f y %4.2f Francos.',Calm(1,1),Calm(2,1),Calm(3,1),Calm(4,1));
    %fprintf(F2,'\n El coste fijo es %8.2f Francos.',cf);
    if ruptadm==2 %el cliente no est� dispuesto a esperar
        fprintf(F2,'\n (rupdtadm= 2)El cliente no est� dispuesto a esperar con un coste de ruptura de %.2f %.2f %.2f %.2f',Crupt(1,1),Crupt(2,1),Crupt(3,1),Crupt(4,1));
    else          %el cliente s� est� dispuesto a esperar
        fprintf(F2,'\n (rupdtadm= 1)El cliente est� dispuesto a esperar con un coste de no servicio de %.2f %.2f %.2f %.2f',Cnoserv(1,1),Cnoserv(2,1),Cnoserv(3,1),Cnoserv(4,1));
    end

    
%% Historial: Tabla Resumen de Producción
    
    fprintf(F2,'\n\n\n\n                       RESULTADOS DEL MES %d        ',j-1);
    fprintf(F2,'\n\n\n ____________________________________________________________________________________________________________');
    fprintf(F2,'\n|                       |                                                   Empresa                          |');
    fprintf(F2,'\n|       Datos           |____________________________________________________________________________________|');
    fprintf(F2,'\n|                       |         Mercedes     |       Peugeot      |  Penhard-Levassor   |       Mors       |');
    fprintf(F2,'\n|_______________________|______________________|____________________|_____________________|__________________|');
    fprintf(F2,'\n| Unidades fabricadas   |    %9d         | %9d          | %9d           | %9d        |',UD(1,j),UD(2,j),UD(3,j),UD(4,j));
    fprintf(F2,'\n| Demanda de la empresa |    %9d         | %9d          | %9d           | %9d        |',V(1,j),V(2,j),V(3,j),V(4,j));
    fprintf(F2,'\n|  Ventas de la empresa |    %9d         | %9d          | %9d           | %9d        |',Ventasreales(1,j),Ventasreales(2,j),Ventasreales(3,j),Ventasreales(4,j));
    fprintf(F2,'\n|  Clientes en espera   |    %9d         | %9d          | %9d           | %9d        |',VENTASPENDIENTES(1,j),VENTASPENDIENTES(2,j),VENTASPENDIENTES(3,j),VENTASPENDIENTES(4,j));
    fprintf(F2,'\n|   Precio de venta     |        %8.2f      |   %8.2f         |     %8.2f        |     %8.2f     |',PVP(1,j),PVP(2,j),PVP(3,j),PVP(4,j));
    fprintf(F2,'\n|     Costes fijos      | %9d      | %9d    | %9d      | %9d     |',CF(1,1),CF(2,1),CF(3,1),CF(4,1));
    fprintf(F2,'\n|   Costes variables    |     %8.2f   |     %8.2f |     %8.2f   |     %8.2f  |',CV(1,j),CV(2,j),CV(3,j),CV(4,j));
    fprintf(F2,'\n|   Unidades en stock   | %9d      | %9d    | %9d      | %9d     |',STOCK(1,j),STOCK(2,j),STOCK(3,j),STOCK(4,j));
    fprintf(F2,'\n|    Costes de stock    | %9d      | %9d    | %9d      | %9d     |',CALM(1,j),CALM(2,j),CALM(3,j),CALM(4,j));
    fprintf(F2,'\n| Costes de no servicio | %9d      | %9d    | %9d      | %9d     |',CNOSERV(1,j),CNOSERV(2,j),CNOSERV(3,j),CNOSERV(4,j));
    fprintf(F2,'\n|   Costes de ruptura   | %9d      | %9d    | %9d      | %9d     |',CRUPT(1,j),CRUPT(2,j),CRUPT(3,j),CRUPT(4,j));
    fprintf(F2,'\n|_______________________|______________________|____________________|_____________________|__________________|');

    
%% Fichero: Tabla Resumen de Cuentas
    
    fprintf(F2,'\n\n\n __________________________________________________________________________________________________________');
    fprintf(F2,'\n|                 |                      Empresa                                                           |');
    fprintf(F2,'\n|   Resultado     |________________________________________________________________________________________|');
    fprintf(F2,'\n|                 |        Mercedes     |      Peugeot       |  Penhard-Levassor   |          Mors         |');
    fprintf(F2,'\n|_________________|_____________________|____________________|_____________________|_______________________|');
    fprintf(F2,'\n| INGRESOS        |  %12.2f       | %12.2f       |  %12.2f       |   %12.2f        |',INGRESOS(1,j),INGRESOS(2,j),INGRESOS(3,j),INGRESOS(4,j));
    fprintf(F2,'\n| COSTES TOTALES  |  %12.2f       | %12.2f       |  %12.2f       |   %12.2f        |',CTOTAL(1,j),CTOTAL(2,j),CTOTAL(3,j),CTOTAL(4,j));
    fprintf(F2,'\n| PRESUPUESTO     |  %12.2f       | %12.2f       |  %12.2f       |   %12.2f        |',PRESUPUESTO(1,j),PRESUPUESTO(2,j),PRESUPUESTO(3,j),PRESUPUESTO(4,j));
    fprintf(F2,'\n|_________________|_____________________|____________________|_____________________|_______________________| \n');


    figure('position',[10,10, 1200,800])

    subplot(2,2,1),
    CME=pie3(CM(:,1)); % Primera columna de la Matriz de Markov
    Diagrama(CME)
    title('Probabilidad de cambio de la empresa %s a:',Empresa(1))

    subplot(2,2,2),
    CME=pie3(CM(:,2)); % Segunda columna de la Matriz de Markov
    Diagrama(CME)
    title('Probabilidad de cambio de la empresa %s a:',Empresa(2))

    subplot(2,2,3),
    CME=pie3(CM(:,3)); % Tercera columna de la Matriz de Markov
    Diagrama(CME)
    title('Probabilidad de cambio de la empresa %s a:',Empresa(3))

    subplot(2,2,4),
    CME=pie3(CM(:,4)); % Cuarta columna de la Matriz de Markov
    Diagrama(CME)
    title('Probabilidad de cambio de la empresa %s a:',Empresa(4))

    if j~=duracion+1
        fprintf('\n\n\nPulse cualquier tecla para pasar al mes siguiente')
    else
        fprintf('_________________________________________________________________\n')
        fprintf('---------------------Fin de la partida-------------------------------\n')
        fprintf('_________________________________________________________________\n')
        fprintf('\nPulse cualquier tecla para continuar  \n')
    end
    pause;

end

Resultados(V, CM, duracion,UD, PRESUPUESTO,CV)

%clc;

fprintf('�Desea guardar la partida? \n')
fprintf('1) Escriba 1 para guardar la partida.\n')
fprintf('2) Escriba 2 para salir sin guardar la partida.\n')
guardar=input('');
while guardar~=1 && guardar~=2
    fprintf('Ese valor no es correcto. Escriba 1 o 2\n')
    guardar=input('');
end
if guardar==1
    fprintf('�Qu� nombre desea darle al fichero?\n')
    fprintf('1) Escriba 1 para elegir el nombre por defecto (Partida.dta).\n')
    fprintf('2) Escriba 2 para poner otro nombre.\n')
    nombre=Unodos();
    if nombre==1
        F1=fopen('Partida.dta','w+t');
    else  %si nombre==2
        fichero=input('','s');
        F1=fopen(fichero,'w+t');
    end

%% Fichero: Tabla Resumen de Producción

    %fprintf(F1,'\n\n\n ____________________________________________________________________________________________________________');
    %fprintf(F1,'\n|                       |                                                   Empresa                          |');
    %fprintf(F1,'\n|       Datos           |____________________________________________________________________________________|');
    %fprintf(F1,'\n|                       |         Mercedes     |       Peugeot      |  Penhard-Levassor   |       Mors       |');
    %fprintf(F1,'\n|_______________________|______________________|____________________|_____________________|__________________|');
    fprintf(F1,'\n %9d          %9d           %9d            %9d',UD(1,j),UD(2,j),UD(3,j),UD(4,j));
    fprintf(F1,'\n %9d          %9d           %9d            %9d',V(1,j),V(2,j),V(3,j),V(4,j));
    fprintf(F1,'\n %9d          %9d           %9d            %9d',Ventasreales(1,j),Ventasreales(2,j),Ventasreales(3,j),Ventasreales(4,j));
    fprintf(F1,'\n %9d          %9d           %9d            %9d',VENTASPENDIENTES(1,j),VENTASPENDIENTES(2,j),VENTASPENDIENTES(3,j),VENTASPENDIENTES(4,j));
    fprintf(F1,'\n %8.2f      %8.2f         %8.2f          %8.2f',PVP(1,j),PVP(2,j),PVP(3,j),PVP(4,j));
    fprintf(F1,'\n %9d          %9d           %9d            %9d',CF(1,1),CF(2,1),CF(3,1),CF(4,1));
    fprintf(F1,'\n %8.2f      %8.2f         %8.2f          %8.2f',CV(1,j),CV(2,j),CV(3,j),CV(4,j));
    fprintf(F1,'\n %9d          %9d           %9d            %9d',STOCK(1,j),STOCK(2,j),STOCK(3,j),STOCK(4,j));
    fprintf(F1,'\n %9d          %9d           %9d            %9d',CALM(1,j),CALM(2,j),CALM(3,j),CALM(4,j));
    fprintf(F1,'\n %9d          %9d           %9d            %9d',CNOSERV(1,j),CNOSERV(2,j),CNOSERV(3,j),CNOSERV(4,j));
    fprintf(F1,'\n %9d          %9d           %9d            %9d',CRUPT(1,j),CRUPT(2,j),CRUPT(3,j),CRUPT(4,j));
    %fprintf(F1,'\n|_______________________|______________________|____________________|_____________________|__________________|');
 
    
%% Fichero: Tabla Resumen de Cuentas
    
    %fprintf(F1,'\n\n\n __________________________________________________________________________________________________________');
    %fprintf(F1,'\n|                 |                      Empresa                                                           |');
    %fprintf(F1,'\n|   Resultado     |________________________________________________________________________________________|');
    %fprintf(F1,'\n|                 |        Mercedes     |      Peugeot       |  Penhard-Levassor   |          Mors         |');
    %fprintf(F1,'\n|_________________|_____________________|____________________|_____________________|_______________________|');
    fprintf(F1,'\n %12.2f      %12.2f         %12.2f          %12.2f',INGRESOS(1,j),INGRESOS(2,j),INGRESOS(3,j),INGRESOS(4,j));
    fprintf(F1,'\n %12.2f      %12.2f         %12.2f          %12.2f',CTOTAL(1,j),CTOTAL(2,j),CTOTAL(3,j),CTOTAL(4,j));
    fprintf(F1,'\n %12.2f      %12.2f         %12.2f          %12.2f',PRESUPUESTO(1,j),PRESUPUESTO(2,j),PRESUPUESTO(3,j),PRESUPUESTO(4,j));
    %fprintf(F1,'\n|_________________|_____________________|____________________|_____________________|_______________________| \n');


    fprintf(F1,'\n %f %f %f %f;  %f %f %f %f;  %f %f %f %f;  %f %f %f %f;', CM(1,1),CM(1,2),CM(1,3),CM(1,4),CM(2,1),CM(2,2),CM(2,3),CM(2,4),CM(3,1),CM(3,2),CM(3,3),CM(3,4),CM(4,1),CM(4,2),CM(4,3),CM(4,4));
    fprintf(F1,'\n %4.2f %4.2f %4.2f  %4.2f; ',Calm(1,1),Calm(2,1),Calm(3,1),Calm(4,1));
    fprintf(F1,'\n %d; ',ruptadm);
    %fprintf(F1,'\n El coste fijo es %8.2f Francos.',cf);
    if ruptadm==2 %el cliente no est� dispuesto a esperar
        fprintf(F1,'\n %.2f %.2f %.2f %.2f',Crupt(1,1),Crupt(2,1),Crupt(3,1),Crupt(4,1));
    else          %el cliente s� est� dispuesto a esperar
        fprintf(F1,'\n  %.2f %.2f %.2f %.2f',Cnoserv(1,1),Cnoserv(2,1),Cnoserv(3,1),Cnoserv(4,1));
    end
    fclose(F1);
    fclose(F2);
end

