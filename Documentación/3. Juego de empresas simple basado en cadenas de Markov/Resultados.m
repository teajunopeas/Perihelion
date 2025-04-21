% Se Representan los resultados en varios diagramas 
% obtenidos desde el inicio (mes cero) hasta el mes final (duración)
function Resultados(V, CM, duracion,UD, PRESUPUESTO,CV)

%Diagrama de barras de la distribución de ventas posibles

x=0:duracion; % "x" representa la variable TIEMPO

figure('position',[5,50, 700,450])% Posición de cada una de las figuras en la pantalla.
% De esta forma las vemos todas a la vez
% Diagrama de Barras
subplot(2,2,1)
bar(V(:,duracion+1)) % (2,2,1) se divide en 2 filas, 2 columnas y se coloca en la posición 1.
% "bar" diagrama de barras del �ltimo mes.
set(gca,'xticklabel',str2mat('Mercedes','Peugeot','Penhard-L','Mors'))
title('Ventas posibles por empresa')
xlabel('Empresas')
ylabel('Ventas posibles')
grid on

%Diagrama de barras para las unidades fabricadas

subplot(2,2,2), bar(UD(:,duracion+1)) % aqu� est� colocado en la posición 2.
set(gca,'xticklabel',str2mat('Mercedes','Peugeot','Penhard-L','Mors'))
title('Unidades fabricadas por empresa')
xlabel('Empresas')
ylabel('Unidades fabricadas')
grid on
set(gca,'YGrid','on')

%Diagrama de barras para el presupuesto

subplot(2,2,3:4), bar(PRESUPUESTO(:,duracion+1)) % ocupa tanto la posición 3 como la 4.
set(gca,'xticklabel',str2mat('Mercedes','Peugeot','Penhard-L','Mors')) % "str2mat" nombra a cada una de las empresas debajo del lugar correspondiente.
title('Presupuesto de la empresa')
xlabel('Empresas')
ylabel('Presupuesto')
grid on
set(gca,'YGrid','on')

%Diagrama sectorial tridimensional para la probabilidad de cambio

figure('position',[10,500, 700,220])

subplot(2,2,1),
CME=pie3(CM(:,1)); % primera columna de la Matriz de Markov
Diagrama(CME)
title('Probabilidad de cambio de la empresa Mercedes a:')

subplot(2,2,2),
CME=pie3(CM(:,2)); % segunda columna de la Matriz de Markov
Diagrama(CME)
title('Probabilidad de cambio de la empresa Peugeot a:')


subplot(2,2,3),
CME=pie3(CM(:,3)); % tercera columna de la Matriz de Markov
Diagrama(CME)
title('Probabilidad de cambio de la empresa Penhard-L a:')

subplot(2,2,4),
CME=pie3(CM(:,4)); % cuarta columna de la Matriz de Markov
Diagrama(CME)
title('Probabilidad de cambio de la empresa Mors a:')







%Diagrama de evolución (dividido en 4 filas y 1 columna)

figure('position',[710,0, 530,720])
subplot(4,1,1), plot(x,PRESUPUESTO)
ylabel('PRESUPUESTO')
xlabel('TIEMPO')
legend('Mercedes','Peugeot','Penhard-L','Mors');
subplot(4,1,2), plot(x,V)
ylabel('VENTAS')
xlabel('TIEMPO')
legend('Mercedes','Peugeot','Penhard-L','Mors');
subplot(4,1,3), plot(x,CV)
ylabel('COSTE VARIABLE')
xlabel('TIEMPO')
legend('Mercedes','Peugeot','Penhard-L','Mors');
subplot(4,1,4), plot(x,UD)
ylabel('UNIDADES')
xlabel('TIEMPO')
legend('Mercedes','Peugeot','Penhard-L','Mors');

end