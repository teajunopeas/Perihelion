# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os # Para limpiar la consola (equivalente a clc)
import math
import random

# Requirements: numpy, matplotlib, tk (para la interfaz gráfica)

# --- Funciones Auxiliares (Traducción de funciones MATLAB) ---

# Equivalente a clc (limpia la pantalla)
def clc():
    os.system('cls' if os.name == 'nt' else 'clear')

# Función para gráficos de pastel (similar a Diagrama en MATLAB)
def diagrama_pastel(ax, data, title, labels_prefix):
    """Genera un gráfico de pastel en un eje dado."""
    # Asegurarse de que los datos sumen 1 o normalizar si no
    data_sum = np.sum(data)
    if not np.isclose(data_sum, 1.0):
        print(f"Advertencia: Los datos para '{title}' no suman 1 (suma={data_sum}). Normalizando.")
        if data_sum <= 1e-9: # Evitar división por cero o normalizar ceros
             # Si todos son cero, mostrar como equitativo o vacío
             print(f"Advertencia: Suma de datos es cero o muy pequeña en '{title}'. Mostrando vacío.")
             ax.text(0.5, 0.5, 'Datos cero', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
             ax.set_title(title)
             return # No graficar nada si la suma es cero
        else:
            data = data / data_sum

    # Crear etiquetas con prefijos y porcentajes
    labels = [f"{prefix} {val:.1%}" for prefix, val in zip(labels_prefix, data)]

    # Filtrar datos muy pequeños para evitar errores/warnings en pie y leyenda
    threshold = 1e-6 # Umbral pequeño
    valid_indices = (i for i, d in enumerate(data) if d >= threshold)

    if not valid_indices: # Si todos los datos son cero o muy pequeños
        print(f"Advertencia: No hay datos válidos (>= {threshold}) para graficar en '{title}'.")
        ax.text(0.5, 0.5, 'Datos muy pequeños', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_title(title)
        return

    # Extraer solo los datos y etiquetas válidos
    valid_data = (data[i] for i in valid_indices)
    valid_labels = (labels[i] for i in valid_indices)

    # --- CORRECCIÓN AQUÍ ---
    # Llamar a ax.pie solo esperando 'wedges' ya que labels y autopct son None
    wedges = ax.pie(valid_data, labels=None, autopct=None, startangle=90)[0]
    '''
    ax.pie devuelve (wedges, texts) o (wedges, texts, autotexts) o solo wedges
    Acceder al primer elemento [0] si devuelve tupla, o usar directamente si solo devuelve wedges.
    Para estar seguros, asignamos el resultado y tomamos el primer elemento si es una tupla/lista.
    '''

    pie_result = ax.pie(valid_data, labels=None, autopct=None, startangle=90)
    # Determinar qué devolvió pie() basado en el tipo/longitud del resultado
    if isinstance(pie_result, (list, tuple)):
        wedges = pie_result[0] # Asumimos que wedges es siempre el primero
    else:
        # Si no es lista/tupla, es probable que sea solo wedges (menos común)
        # Esta parte es defensiva, el comportamiento estándar es devolver tupla
         print("Advertencia: ax.pie no devolvió una tupla/lista como se esperaba.")
         # Intentar usar el resultado directamente como wedges podría fallar
         # Una alternativa más segura es rehacer la llamada pidiendo explícitamente solo wedges si fuera posible,
         # pero la API estándar no ofrece eso. La forma más robusta es asignar a una variable y verificar.
         # Sin embargo, la causa más probable del error original es que `autopct=None` cambia la tupla devuelta.
         # Vamos a probar con la asignación original pero esperando solo 2 valores si labels=None
         # wedges, texts = ax.pie(valid_data, labels=valid_labels, autopct=None, startangle=90) # Si pasáramos labels
         # O, como tenemos labels=None y autopct=None:
         wedges = ax.pie(valid_data, labels=None, autopct=None, startangle=90)[0] # Tomamos solo wedges


    # --- FIN CORRECCIÓN ---

    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Añadir leyenda con las etiquetas formateadas (usando las etiquetas válidas)
    if valid_labels: # Solo añadir leyenda si hay etiquetas válidas
         ax.legend(wedges, valid_labels, title="Empresas", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # --- CORRECCIÓN AQUÍ ---
    # Eliminar o comentar esta línea ya que autotexts no se genera con autopct=None
    # plt.setp(autotexts, size=8, weight="bold")
    # --- FIN CORRECCIÓN ---

    ax.set_title(title)


# Comprueba que la entrada sea un entero mayor o igual a cero.
def entero_positivo():
    """Pide al usuario un entero >= 0 y lo valida."""
    while True:
        try:
            salida = input('')
            valor = int(salida)
            if valor >= 0:
                return valor
            else:
                print('Ese valor no es correcto, debe ser mayor o igual a cero. Introduzca otro valor')
        except ValueError:
            print('Entrada inválida. Por favor, introduzca un número entero.')

# Comprueba que la entrada sea un número positivo (float o int).
def numero_positivo():
    """Pide al usuario un número > 0 y lo valida."""
    while True:
        try:
            salida = input('')
            valor = float(salida)
            if valor > 0:
                return valor
            else:
                print('Ese valor no es correcto, debe ser positivo. Introduzca otro valor')
        except ValueError:
            print('Entrada inválida. Por favor, introduzca un número.')

# Comprueba que la entrada sea 1 ó 2
def uno_o_dos():
    """Pide al usuario que introduzca 1 o 2 y lo valida."""
    while True:
        try:
            salida = input('')
            valor = int(salida)
            if valor == 1 or valor == 2:
                return valor
            else:
                print('Ese valor no es correcto, debe ser 1 o 2')
        except ValueError:
            print('Entrada inválida. Por favor, introduzca 1 o 2.')

# Efecto del Marketing.
def marketing(i, j, CM, CTOTAL, PRESUPUESTO, Empresa, PUB, duracion):
    """Calcula el efecto de la inversión en marketing."""
    # i: índice de la empresa (0 a 3)
    # j: índice del mes actual (1 a duracion)
    presupuesto_actual = PRESUPUESTO[i, j] # Presupuesto al inicio del mes j

    if presupuesto_actual <= 0:
        print('Si la empresa se encuentra en números rojos, no se permite realizar inversiones')
        # No se modifica PUB[i, j], se mantiene el del mes anterior
        # No se modifica CTOTAL[i,j], se mantiene en 0 o lo que tuviera
        # No se modifica CM
        return CTOTAL, CM, PUB # Devuelve los valores sin cambios relevantes aquí
    print('¿Desea modificar la inversión en Marketing del mes pasado?')
    print('1) Teclee un 1 si desea modificarla.')
    print('2) Teclee un 2 si no desea modificarla.')
    modificacion = uno_o_dos()

    pub_actual = 0.0 # Inversión en este paso

    if modificacion == 1:
        print(f'Introduzca la inversión en Marketing que desea realizar la empresa {Empresa[i]}')
        while True:
            try:
                pub_input = input('')
                pub_actual = float(pub_input)
                if 0 <= pub_actual <= presupuesto_actual:
                    break
                else:
                    print('Ese valor no es correcto, introduzca otra cantidad')
                    print(f'Debe ser positivo y no superior a su presupuesto actual: {presupuesto_actual:.2f}')
            except ValueError:
                 print('Entrada inválida. Por favor, introduzca un número.')

        PUB[i, j] = pub_actual # Guardar la nueva inversión

        # Preguntar si es correcto si la inversión es cero
        while PUB[i, j] == 0:
            print('No se ha invertido nada en Marketing. ¿Es eso correcto?')
            print('1) Teclee un 1 si es correcto.')
            print('2) Teclee un 2 si desea modificar la cantidad.')
            nomodificacion = uno_o_dos()
            if nomodificacion == 2:
                print(f'Introduzca la cantidad que desea invertir la empresa {Empresa[i]}')
                while True:
                   try:
                       pub_input = input('')
                       pub_actual = float(pub_input)
                       if 0 <= pub_actual <= presupuesto_actual:
                           PUB[i, j] = pub_actual
                           break
                       else:
                           print('Ese valor no es correcto, introduzca otra cantidad')
                           print(f'Debe ser positivo y no superior a su presupuesto actual: {presupuesto_actual:.2f}')
                   except ValueError:
                        print('Entrada inválida. Por favor, introduzca un número.')
            else:
                 # Si es correcto que sea 0, salimos del bucle while PUB[i, j] == 0
                 break
    else:
        # Si no se modifica, PUB[i,j] ya tiene el valor del mes anterior copiado
        pub_actual = PUB[i,j]


    # Aplicar efecto del marketing si hubo inversión (o si se mantuvo la del mes pasado > 0)
    if pub_actual > 0:
         # Presupuesto del mes anterior para REF (j-1)
         # Usamos max sobre todos los presupuestos al *inicio* del mes anterior (columna j-1)
         presupuestos_mes_anterior = PRESUPUESTO[:, j-1]
         # Evitar error si todos los presupuestos anteriores son <= 0
         if np.any(presupuestos_mes_anterior > 0):
             ref_budget = np.max(presupuestos_mes_anterior[presupuestos_mes_anterior > 0])
         else:
             ref_budget = 1 # Un valor por defecto pequeño si no hay presupuestos positivos
         # Ajuste para evitar división por cero o log(0) si ref_budget es muy pequeño
         ref_budget = max(ref_budget, 1e-6)

         REF = ref_budget / max(duracion, 1) # Evitar división por cero si duración es 0
         REF = max(REF, 1e-9) # Asegurar que REF sea positivo

         denominador_log = (0.1 * REF / (0.1 * REF + 1))
         # Evitar log(0) o log(negativo)
         if denominador_log <= 0:
             denominador_log = 1e-9 # Un valor pequeño y positivo

         # Usamos CM original (antes de cualquier cambio en este mes) para k_M
         # El código MATLAB usa CM(i,i), asumiré que se refiere a la CM antes de este cálculo
         # Necesitamos la CM *antes* de que cualquier empresa haga marketing este mes.
         # Pasamos CM_prev a la función o la recalculamos si es necesario.
         # Asumamos que CM pasada a la función es la del inicio del mes (copia de CM del mes j-1).

         # Asegurar que CM[i,i] sea positivo para el cálculo de k_M
         cm_diag = max(CM[i,i], 1e-9)

         k_M = (0.2 * cm_diag) / math.log(1 + denominador_log)
         k_M = max(k_M, 0) # Asegurar que k_M no sea negativo

         icm = 0
         if pub_actual > 0.1 * REF:
             # Evitar log(0) o log(negativo)
             argumento_log = 1 + (0.1 * REF / (0.1 * REF + 1))
             icm = k_M * math.log(max(argumento_log, 1e-9))
         else:
             # Evitar log(0) o log(negativo)
             argumento_log = 1 + (pub_actual / (0.1 * REF + 1))
             icm = k_M * math.log(max(argumento_log, 1e-9))

         icm = max(icm, 0) # Asegurar que el incremento no sea negativo

         # Crear una copia de CM para modificarla
         CM_new = CM.copy()

         # Aplicar el incremento/decremento
         num_empresas = CM.shape[0]
         if num_empresas > 1:
             decremento_otras = icm / (num_empresas - 1)
         else:
             decremento_otras = 0

         for m in range(num_empresas):
             if i == m:
                 CM_new[m, i] += icm
             else:
                 CM_new[m, i] -= decremento_otras

         # Asegurar que no haya valores negativos y normalizar la columna i
         CM_new[:, i] = np.maximum(CM_new[:, i], 0) # Pone negativos a 0
         col_sum = np.sum(CM_new[:, i])
         if col_sum > 1e-9: # Evitar división por cero
             CM_new[:, i] /= col_sum
         else:
             # Si la suma es cero (todos los elementos eran <=0), re-distribuir equitativamente
             print(f"Advertencia: La columna {i} de CM sumó cero después del marketing. Redistribuyendo.")
             CM_new[:, i] = 1.0 / num_empresas

         CM = CM_new # Actualizar la matriz CM original

    # Actualizar coste total con la inversión en PUB de este mes
    CTOTAL[i, j] += pub_actual # Sumar la inversión al coste de este mes

    return CTOTAL, CM, PUB

# Efecto de Mejoras Tecnológicas
def mejoras_tecnologicas(i, j, CV, CTOTAL, PRESUPUESTO, Empresa, CM, mejoras, duracion):
    """Calcula el efecto de la inversión en mejoras tecnológicas."""
    presupuesto_actual = PRESUPUESTO[i, j]

    if presupuesto_actual <= 0:
        print('Si la empresa no tiene capital disponible, no se permite invertir en Mejoras Tecnológicas')
        return CTOTAL, CV, CM, mejoras

    print('¿Desea modificar la inversión en Mejoras Tecnológicas del mes pasado?')
    print('1) Teclee un 1 si desea modificarla.')
    print('2) Teclee un 2 si no desea modificarla.')
    modificacion = uno_o_dos()

    mejora_actual = 0.0

    if modificacion == 1:
        print(f'Introduzca la inversión en Mejoras Tecnológicas que desea realizar la empresa {Empresa[i]}')
        while True:
            try:
                mejora_input = input('')
                mejora_actual = float(mejora_input)
                if 0 <= mejora_actual <= presupuesto_actual:
                    break
                else:
                    print('Ese valor no es correcto, introduzca otra cantidad')
                    print(f'Debe ser positiva y no superior a su presupuesto actual: {presupuesto_actual:.2f}')
            except ValueError:
                 print('Entrada inválida. Por favor, introduzca un número.')

        mejoras[i, j] = mejora_actual

        while mejoras[i, j] == 0:
            print('No se ha invertido nada en Mejoras Tecnológicas. ¿Es eso correcto?')
            print('1) Teclee un 1 si es correcto.')
            print('2) Teclee un 2 si desea modificar la cantidad.')
            nomodificacion = uno_o_dos()
            if nomodificacion == 2:
                 print(f'Introduzca la cantidad que desea invertir la empresa {Empresa[i]}')
                 while True:
                    try:
                        mejora_input = input('')
                        mejora_actual = float(mejora_input)
                        if 0 <= mejora_actual <= presupuesto_actual:
                            mejoras[i, j] = mejora_actual
                            break
                        else:
                            print('Ese valor no es correcto, introduzca otra cantidad')
                            print(f'Debe ser positiva y no superior a su presupuesto actual: {presupuesto_actual:.2f}')
                    except ValueError:
                         print('Entrada inválida. Por favor, introduzca un número.')
            else:
                 break
    else:
        mejora_actual = mejoras[i,j] # Usa el valor copiado del mes anterior


    # Aplicar efecto de las mejoras si hubo inversión
    if mejora_actual > 0:
        # Usamos max sobre todos los presupuestos al *inicio* del mes anterior (columna j-1)
        presupuestos_mes_anterior = PRESUPUESTO[:, j-1]
        if np.any(presupuestos_mes_anterior > 0):
            ref_budget = np.max(presupuestos_mes_anterior[presupuestos_mes_anterior > 0])
        else:
            ref_budget = 1 # Valor por defecto

        ref_budget = max(ref_budget, 1e-6)
        REF = ref_budget / max(duracion, 1)
        REF = max(REF, 1e-9)

        # CV(i,1) se usa en MATLAB, es el coste variable INICIAL.
        # Aseguramos que sea positivo
        cv_inicial = max(CV[i, 0], 1e-9) # CV[i,0] es el CV inicial (mes 0)

        # Calculamos k_Tc, asegurando que el argumento del log sea > 0
        argumento_log_ktc = 0.075 * REF + 1
        if argumento_log_ktc <= 1: # log(1)=0, log(<1) < 0. Queremos log(>1)
            argumento_log_ktc = 1 + 1e-9 # ligeramente mayor que 1
        k_Tc = (0.05 * cv_inicial) / math.log(argumento_log_ktc)
        k_Tc = max(k_Tc, 0)

        k_Tv = 0.1

        icv = 0
        icm = 0
        ref_mejoras = 0.075 * REF

        # Usamos CM[i,i] antes de la modificación por mejoras
        cm_diag = max(CM[i,i], 1e-9)

        if mejora_actual > ref_mejoras:
            # Argumento log para ICV
            argumento_log_icv = ref_mejoras + 1
            if argumento_log_icv <= 1: argumento_log_icv = 1 + 1e-9
            icv = k_Tc * math.log(argumento_log_icv)
            icm = k_Tv * cm_diag # Impacto máximo en CM
        else:
            # Argumento log para ICV
            argumento_log_icv = mejora_actual + 1
            if argumento_log_icv <= 1: argumento_log_icv = 1 + 1e-9
            icv = k_Tc * math.log(argumento_log_icv)
            # Impacto en CM proporcional a la inversión relativa
            if ref_mejoras > 1e-9: # Evitar división por cero
                 icm = k_Tv * (mejora_actual / ref_mejoras) * cm_diag
            else:
                 icm = 0 # Si la referencia es cero, no hay impacto relativo

        icv = max(icv, 0) # La reducción de coste no puede ser negativa
        icm = max(icm, 0) # El incremento en CM no puede ser negativo

        # Aplicar reducción de Coste Variable
        CV[i, j] = max(CV[i, j] - icv, 0) # El coste variable no puede ser negativo

        # Aplicar efecto en la Matriz de Markov (CM)
        CM_new = CM.copy()
        num_empresas = CM.shape[0]
        if num_empresas > 1:
            decremento_otras = icm / (num_empresas - 1)
        else:
            decremento_otras = 0

        for m in range(num_empresas):
            if i == m:
                CM_new[m, i] += icm
            else:
                CM_new[m, i] -= decremento_otras

        # Asegurar que no haya valores negativos y normalizar la columna i
        CM_new[:, i] = np.maximum(CM_new[:, i], 0)
        col_sum = np.sum(CM_new[:, i])
        if col_sum > 1e-9:
            CM_new[:, i] /= col_sum
        else:
            print(f"Advertencia: La columna {i} de CM sumó cero después de mejoras. Redistribuyendo.")
            CM_new[:, i] = 1.0 / num_empresas

        CM = CM_new # Actualizar la matriz CM

    # Actualizar coste total con la inversión en mejoras
    CTOTAL[i, j] += mejora_actual

    return CTOTAL, CV, CM, mejoras


# Modificación del Precio de Venta al Público (PVP)
def precio_vp(PVP, CM, Empresa, i, j, PVPini):
    """Modifica el PVP y calcula el efecto en la cuota de mercado (CM)."""
    pvp_actual = PVP[i, j] # Precio antes de la modificación (ya copiado de j-1)
    print(f'Escriba el nuevo precio de venta al público de la empresa {Empresa[i]} (actual: {pvp_actual:.2f})')
    pvp_mod = numero_positivo() # Pide un nuevo precio positivo

    # Verificar si el precio realmente cambió
    if not np.isclose(pvp_mod, pvp_actual):
         # Calcular Vx y Vmod (cambio en cuota de mercado)
         # Asegurar que PVPini no sea cero
         pvpini_safe = max(PVPini, 1e-9)
         vx = 0.75 * (pvp_actual - pvp_mod) / pvpini_safe

         # Usar CM[i,i] antes de la modificación de precio
         cm_diag_prev = max(CM[i, i], 1e-9) # Evitar división por cero si CM[i,i] es 0

         # Calcular vmod (nueva cuota para la empresa i en su columna)
         # La fórmula en MATLAB es: Vmod(i,j)=CM(i,i)/2*(Vx+sqrt(Vx^2+4));
         # Esto parece calcular la *nueva* cuota CM[i,i], no el incremento.
         try:
            termino_sqrt = vx**2 + 4
            if termino_sqrt < 0: termino_sqrt = 0 # Evitar raíz de negativo
            vmod_i_i = (cm_diag_prev / 2) * (vx + math.sqrt(termino_sqrt))
            vmod_i_i = max(vmod_i_i, 0) # La cuota no puede ser negativa
         except ValueError:
             print(f"Error en cálculo de Vmod para {Empresa[i]}. Vx={vx}, CM_diag={cm_diag_prev}")
             vmod_i_i = cm_diag_prev # Si hay error, no cambiar la cuota

         icm = vmod_i_i - cm_diag_prev # Incremento (puede ser negativo si sube precio)

         # Actualizar el precio
         PVP[i, j] = pvp_mod

         # Actualizar la matriz CM
         CM_new = CM.copy()
         num_empresas = CM.shape[0]

         if num_empresas > 1:
             # El incremento icm se aplica a CM(i,i)
             # El decremento (-icm) se reparte entre las otras empresas en la columna i
             decremento_otras = -icm / (num_empresas - 1)
         else:
             decremento_otras = 0

         for m in range(num_empresas):
             if i == m:
                 CM_new[m, i] += icm
             else:
                 CM_new[m, i] += decremento_otras # Sumamos porque decremento_otras puede ser negativo

         # Asegurar que no haya valores negativos y normalizar la columna i
         CM_new[:, i] = np.maximum(CM_new[:, i], 0)
         col_sum = np.sum(CM_new[:, i])
         if col_sum > 1e-9:
             CM_new[:, i] /= col_sum
         else:
             print(f"Advertencia: La columna {i} de CM sumó cero después del cambio de precio. Redistribuyendo.")
             CM_new[:, i] = 1.0 / num_empresas

         CM = CM_new # Actualizar CM

    else:
        print("El precio no ha sido modificado.")
        # PVP y CM no cambian

    return PVP, CM


# Representa los resultados finales
def resultados_finales(V, CM, duracion, UD, PRESUPUESTO, CV, Empresa):
    """Genera los gráficos de resultados al final de la simulación."""
    meses = np.arange(duracion + 1) # Eje x (0 a duracion)
    n_empresas = len(Empresa)
    colores = plt.cm.viridis(np.linspace(0, 1, n_empresas)) # Colores para las empresas

    # --- Gráfico 1: Resumen final (Barras) ---
    fig1, axs1 = plt.subplots(2, 2, figsize=(12, 10))
    fig1.suptitle('Resumen al Final del Juego (Mes {})'.format(duracion))

    # Ventas posibles (demanda) último mes
    axs1[0, 0].bar(Empresa, V[:, duracion], color=colores)
    axs1[0, 0].set_title('Demanda estimada por empresa')
    axs1[0, 0].set_ylabel('Demanda estimada')
    axs1[0, 0].grid(True, axis='y')

    # Unidades fabricadas último mes
    axs1[0, 1].bar(Empresa, UD[:, duracion], color=colores)
    axs1[0, 1].set_title('Unidades fabricadas por empresa')
    axs1[0, 1].set_ylabel('Unidades fabricadas')
    axs1[0, 1].grid(True, axis='y')

    # Presupuesto último mes
    # Combinar los dos subplots inferiores
    gs = axs1[1, 0].get_gridspec()
    # Eliminar los ejes inferiores originales
    for ax in axs1[1, :]:
        ax.remove()
    ax_presupuesto = fig1.add_subplot(gs[1, :]) # Crear un eje que ocupe toda la fila inferior
    ax_presupuesto.bar(Empresa, PRESUPUESTO[:, duracion], color=colores)
    ax_presupuesto.set_title('Presupuesto de la empresa')
    ax_presupuesto.set_ylabel('Presupuesto')
    ax_presupuesto.grid(True, axis='y')

    fig1.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajustar para el título principal

    # --- Gráfico 2: Matriz de Markov (Pasteles) ---
    fig2, axs2 = plt.subplots(2, 2, figsize=(12, 8))
    fig2.suptitle('Probabilidad de Cambio (Matriz de Markov Final)')
    labels_prefix = ['ME:', 'PE:', 'PL:', 'MO:'] # Nombres cortos para etiquetas

    # Graficar cada columna de CM como un pastel
    for i in range(n_empresas):
        ax = axs2[i // 2, i % 2]
        titulo = f'Prob. cambio desde {Empresa[i]} a:'
        # Asegurarse de que CM[:, i] tenga la forma correcta y no contenga NaNs
        datos_pastel = CM[:, i]
        if np.isnan(datos_pastel).any():
             print(f"Advertencia: NaN encontrado en CM columna {i}. Reemplazando con 0.")
             datos_pastel = np.nan_to_num(datos_pastel) # Reemplaza NaN con 0
        diagrama_pastel(ax, datos_pastel, titulo, labels_prefix)

    fig2.tight_layout(rect=[0, 0.03, 1, 0.95])

    # --- Gráfico 3: Evolución Temporal (Líneas) ---
    fig3, axs3 = plt.subplots(4, 1, figsize=(10, 12), sharex=True)
    fig3.suptitle('Evolución Temporal de Indicadores')

    # Presupuesto
    for i in range(n_empresas):
        axs3[0].plot(meses, PRESUPUESTO[i, :], label=Empresa[i], color=colores[i])
    axs3[0].set_ylabel('PRESUPUESTO')
    axs3[0].legend()
    axs3[0].grid(True)

    # Ventas (Demanda estimada V)
    for i in range(n_empresas):
        axs3[1].plot(meses, V[i, :], label=Empresa[i], color=colores[i])
    axs3[1].set_ylabel('DEMANDA (V)')
    axs3[1].legend()
    axs3[1].grid(True)

    # Coste Variable
    for i in range(n_empresas):
        axs3[2].plot(meses, CV[i, :], label=Empresa[i], color=colores[i])
    axs3[2].set_ylabel('COSTE VARIABLE (CV)')
    axs3[2].legend()
    axs3[2].grid(True)

    # Unidades Fabricadas
    for i in range(n_empresas):
        axs3[3].plot(meses, UD[i, :], label=Empresa[i], color=colores[i])
    axs3[3].set_ylabel('UNIDADES FABRICADAS (UD)')
    axs3[3].set_xlabel('Mes')
    axs3[3].legend()
    axs3[3].grid(True)

    fig3.tight_layout(rect=[0, 0.03, 1, 0.95])

    plt.show() # Mostrar todas las figuras

# --- Programa Principal ---

clc()
print('\nJuego de empresas para cuatro participantes\n')

Empresa = ["Mercedes", "Peugeot", "Penhard-Levassor", "Mors"]
n_empresas = len(Empresa)

# Variables para almacenar los datos a lo largo del tiempo
# Se inicializarán adecuadamente si es partida nueva o se cargarán
PRESUPUESTO = None
V = None # Demanda estimada
PVP = None
CV = None
CF = None
STOCK = None
INGRESOS = None
UD = None # Unidades Fabricadas
CTOTAL = None
Calm = None # Coste unitario almacenamiento
Cnoserv = None # Coste unitario no servicio
Crupt = None # Coste unitario ruptura
VENTASPENDIENTES = None
Ventasreales = None
CRUPT_TOTAL = None # Coste total ruptura por mes
CALM_TOTAL = None # Coste total almacenamiento por mes
CNOSERV_TOTAL = None # Coste total no servicio por mes
PUB = None # Inversion Marketing
mejoras = None # Inversion Mejoras
CM = None # Matriz Markov

duracion = 0
pvpini = 0.0
ventasmax = 0 # Demanda total del mercado en el mes anterior
ruptadm = 1 # 1: espera, 2: no espera


print('¿Desea cargar una partida anterior o empezar otra?')
print('1) Escriba 1 para cargar una partida antigua.')
print('2) Escriba 2 para comenzar una partida nueva.')
cargar = uno_o_dos()

# --- Cargar Partida Antigua ---
if cargar == 1:
    print('¿Qué nombre tiene el fichero de entrada?')
    print('1) Escriba 1 si tiene el nombre por defecto (Partida.dta).')
    print('2) Escriba 2 si tiene otro nombre.')
    nombrec = uno_o_dos()
    ficheroc = ''
    if nombrec == 1:
        ficheroc = 'Partida.dta'
    else:
        while True:
            ficheroc = input('Escriba el nombre del fichero (ej: mi_partida.dta):\n')
            if os.path.exists(ficheroc):
                break
            else:
                print(f'No se encuentra el fichero "{ficheroc}". Inténtelo de nuevo.')

    print(f"Cargando datos desde {ficheroc}...")
    try:
        # Leer el archivo línea por línea e interpretar los datos
        # Esto es una aproximación, el formato exacto de fscanf es complejo de replicar
        # Asumimos que cada línea contiene datos para las 4 empresas separados por espacios
        # y que las matrices están guardadas fila por fila o columna por columna según el fprintf.
        # El fprintf en MATLAB guarda columna por columna para las matrices 2D.
        # Necesitaremos leer y luego reestructurar.

        with open(ficheroc, 'rt') as F1:
            lines = F1.readlines()

        # Quitar espacios en blanco y líneas vacías
        lines = [line.strip() for line in lines if line.strip()]

        # Interpretar las líneas - Esto requiere conocer el orden exacto de guardado
        # Basado en el código fprintf al guardar:
        # 1-11: Datos de producción (UD, V, VentasReales, Pendientes, PVP, CF, CV, STOCK, CALM_Total, CNOSERV_Total, CRUPT_Total) - 1 línea por dato
        # 12-14: Resultados (INGRESOS, CTOTAL, PRESUPUESTO) - 1 línea por dato
        # 15: Matriz CM (formato especial)
        # 16: Costes unitarios Calm
        # 17: ruptadm
        # 18: Costes unitarios Crupt o Cnoserv

        if len(lines) < 18:
            raise ValueError("El archivo de guardado parece incompleto.")

        # Función auxiliar para parsear línea de 4 números
        def parse_line_floats(line):
             parts = line.split()
             if len(parts) < 4: raise ValueError(f"Línea incompleta: '{line}'")
             # Intentar convertir los primeros 4 a float
             return np.array([float(p) for p in parts[:4]])
        def parse_line_ints(line):
             parts = line.split()
             if len(parts) < 4: raise ValueError(f"Línea incompleta: '{line}'")
              # Intentar convertir los primeros 4 a int
             return np.array([int(p) for p in parts[:4]])


        # Leer los datos del último mes guardado (índice 0 para estas variables temporales)
        ud_last = parse_line_ints(lines[0])
        v_last = parse_line_ints(lines[1])
        ventasreales_last = parse_line_ints(lines[2])
        ventaspendientes_last = parse_line_ints(lines[3])
        pvp_last = parse_line_floats(lines[4])
        cf_last = parse_line_ints(lines[5]) # CF parece guardarse como int aunque se pide como positivo? Ajustar si es float.
        cv_last = parse_line_floats(lines[6])
        stock_last = parse_line_ints(lines[7])
        calm_total_last = parse_line_ints(lines[8]) # Asumo que son los costes totales del mes, no unitarios
        cnoserv_total_last = parse_line_ints(lines[9])# Asumo que son los costes totales del mes, no unitarios
        crupt_total_last = parse_line_ints(lines[10])# Asumo que son los costes totales del mes, no unitarios

        ingresos_last = parse_line_floats(lines[11])
        ctotal_last = parse_line_floats(lines[12])
        presupuesto_last = parse_line_floats(lines[13])

        # Leer Matriz CM
        cm_line = lines[14].replace(';', '').split() # Quita ';' y divide por espacio
        if len(cm_line) < 16: raise ValueError("Línea de matriz CM incompleta.")
        cm_values = [float(v) for v in cm_line[:16]]
        CM = np.array(cm_values).reshape((4, 4)) # Asume orden por defecto (fila) - MATLAB guarda por columna en fprintf
        # Corregir si fprintf guarda por columna:
        # CM = np.array(cm_values).reshape((4, 4), order='F') # 'F' for Fortran/MATLAB column-major order

        # Leer costes unitarios Calm
        calm_unit_line = lines[15].replace(';', '').split()
        if len(calm_unit_line) < 4: raise ValueError("Línea de costes Calm incompleta.")
        Calm_unit = np.array([float(v) for v in calm_unit_line[:4]])

        # Leer ruptadm
        ruptadm_line = lines[16].replace(';', '').split()
        if not ruptadm_line: raise ValueError("Línea de ruptadm vacía.")
        ruptadm = int(ruptadm_line[0])

        # Leer costes Crupt o Cnoserv
        cost_line = lines[17].replace(';', '').split()
        if len(cost_line) < 4: raise ValueError("Línea de costes Crupt/Cnoserv incompleta.")
        cost_unit_values = np.array([float(v) for v in cost_line[:4]])
        Crupt_unit = np.zeros(n_empresas)
        Cnoserv_unit = np.zeros(n_empresas)
        if ruptadm == 2:
            Crupt_unit = cost_unit_values
        else:
            Cnoserv_unit = cost_unit_values

        # --- Inicializar matrices para la nueva simulación ---
        print('\n\nIntroduzca la nueva duración del juego en meses:')
        while True:
             duracion_nueva = entero_positivo()
             if duracion_nueva > 0:
                 duracion = duracion_nueva
                 break
             else:
                 print("La duración debe ser mayor que cero.")

        # Crear arrays con tamaño para la nueva duración + estado inicial
        # El estado inicial (columna 0) será el estado final cargado
        PRESUPUESTO = np.zeros((n_empresas, duracion + 1))
        V = np.zeros((n_empresas, duracion + 1), dtype=int)
        PVP = np.zeros((n_empresas, duracion + 1))
        CV = np.zeros((n_empresas, duracion + 1))
        CF = np.zeros((n_empresas, duracion + 1)) # CF parece constante, pero lo guardamos por mes por si acaso
        STOCK = np.zeros((n_empresas, duracion + 1), dtype=int)
        INGRESOS = np.zeros((n_empresas, duracion + 1))
        UD = np.zeros((n_empresas, duracion + 1), dtype=int)
        CTOTAL = np.zeros((n_empresas, duracion + 1))
        # Los costes unitarios son constantes (o cambian poco)
        Calm = np.zeros((n_empresas, duracion + 1))
        Cnoserv = np.zeros((n_empresas, duracion + 1))
        Crupt = np.zeros((n_empresas, duracion + 1))
        # Variables auxiliares y de estado
        VENTASPENDIENTES = np.zeros((n_empresas, duracion + 1), dtype=int)
        Ventasreales = np.zeros((n_empresas, duracion + 1), dtype=int)
        CRUPT_TOTAL = np.zeros((n_empresas, duracion + 1))
        CALM_TOTAL = np.zeros((n_empresas, duracion + 1))
        CNOSERV_TOTAL = np.zeros((n_empresas, duracion + 1))
        PUB = np.zeros((n_empresas, duracion + 1)) # ¿Se guarda PUB? No parece. Asumir 0 inicial.
        mejoras = np.zeros((n_empresas, duracion + 1)) # ¿Se guarda mejoras? No parece. Asumir 0 inicial.


        # Cargar los datos del último mes guardado en la columna 0 de las nuevas matrices
        PRESUPUESTO[:, 0] = presupuesto_last
        V[:, 0] = v_last
        PVP[:, 0] = pvp_last
        CV[:, 0] = cv_last
        CF[:, 0] = cf_last # CF puede ser constante, verificar si se cargó bien
        STOCK[:, 0] = stock_last
        INGRESOS[:, 0] = ingresos_last # Esto es del mes anterior, ¿debería ser 0?
        UD[:, 0] = ud_last           # Ídem
        CTOTAL[:, 0] = ctotal_last     # Ídem
        VENTASPENDIENTES[:, 0] = ventaspendientes_last
        Ventasreales[:, 0] = ventasreales_last
        CRUPT_TOTAL[:, 0] = crupt_total_last
        CALM_TOTAL[:, 0] = calm_total_last
        CNOSERV_TOTAL[:, 0] = cnoserv_total_last
        # PUB y mejoras no se guardan, se asumen 0 o se inicializan de otra forma si es necesario
        PUB[:, 0] = 0 # O quizás debería ser el último valor usado? Depende de la lógica deseada.
        mejoras[:, 0] = 0

        # Cargar costes unitarios (asumiendo que son constantes o el valor inicial aplica)
        for k in range(duracion + 1):
             Calm[:, k] = Calm_unit
             Crupt[:, k] = Crupt_unit
             Cnoserv[:, k] = Cnoserv_unit

        # PVP inicial de referencia
        pvpini = np.mean(pvp_last) # O quizás el pvp inicial original si estuviera guardado?
        # Demanda total del último mes guardado
        ventasmax = np.sum(v_last)

        print("\nDatos cargados. Estado inicial (Mes 0):")
        # Mostrar tabla resumen del estado cargado (similar al código MATLAB)
        print('\n--- Datos Almacenados (Estado Inicial Mes 0) ---')
        print('________________________________________________________________________________________')
        print('|                       |                            Empresa                             |')
        print('|         Datos         |________________________________________________________________|')
        print('|                       |    Mercedes    |    Peugeot   |Penhard-Levassor|      Mors     |')
        print('|_______________________|________________|______________|________________|_______________|')
        print(f'|  Unidades fabricadas  | {UD[0,0]:>14d} | {UD[1,0]:>12d} | {UD[2,0]:>14d} | {UD[3,0]:>13d} |')
        print(f'| Demanda de la empresa | {V[0,0]:>14d} | {V[1,0]:>12d} | {V[2,0]:>14d} | {V[3,0]:>13d} |')
        print(f'| Ventas de la empresa  | {Ventasreales[0,0]:>14d} | {Ventasreales[1,0]:>12d} | {Ventasreales[2,0]:>14d} | {Ventasreales[3,0]:>13d} |')
        print(f'|  Clientes en espera   | {VENTASPENDIENTES[0,0]:>14d} | {VENTASPENDIENTES[1,0]:>12d} | {VENTASPENDIENTES[2,0]:>14d} | {VENTASPENDIENTES[3,0]:>13d} |')
        print(f'|    Precio de venta    | {PVP[0,0]:>14.2f} | {PVP[1,0]:>12.2f} | {PVP[2,0]:>14.2f} | {PVP[3,0]:>13.2f} |')
        print(f'|     Costes fijos      | {CF[0,0]:>14.0f} | {CF[1,0]:>12.0f} | {CF[2,0]:>14.0f} | {CF[3,0]:>13.0f} |') # Asumiendo CF es entero
        print(f'|   Costes variables    | {CV[0,0]:>14.2f} | {CV[1,0]:>12.2f} | {CV[2,0]:>14.2f} | {CV[3,0]:>13.2f} |')
        print(f'|   Unidades en stock   | {STOCK[0,0]:>14d} | {STOCK[1,0]:>12d} | {STOCK[2,0]:>14d} | {STOCK[3,0]:>13d} |')
        print(f'|    Costes de stock    | {CALM_TOTAL[0,0]:>14.0f} | {CALM_TOTAL[1,0]:>12.0f} | {CALM_TOTAL[2,0]:>14.0f} | {CALM_TOTAL[3,0]:>13.0f} |') # Coste total
        print(f'| Costes de no servicio | {CNOSERV_TOTAL[0,0]:>14.0f} | {CNOSERV_TOTAL[1,0]:>12.0f} | {CNOSERV_TOTAL[2,0]:>14.0f} | {CNOSERV_TOTAL[3,0]:>13.0f} |') # Coste total
        print(f'|   Costes de ruptura   | {CRUPT_TOTAL[0,0]:>14.0f} | {CRUPT_TOTAL[1,0]:>12.0f} | {CRUPT_TOTAL[2,0]:>14.0f} | {CRUPT_TOTAL[3,0]:>13.0f} |') # Coste total
        print('|_______________________|________________|______________|________________|_______________|')
        print('\n--- Resultados (Estado Inicial Mes 0) ---')
        print('_________________________________________________________________________________________________________')
        print('|                 |                                         Empresa                                       |')
        print('|   Resultados    |_______________________________________________________________________________________|')
        print('|                 |      Mercedes      |       Peugeot      |  Penhard-Levassor   |          Mors         |')
        print('|_________________|____________________|____________________|_____________________|_______________________|')
        print(f'| Ingresos        | {INGRESOS[0,0]:>18.2f} | {INGRESOS[1,0]:>18.2f} | {INGRESOS[2,0]:>19.2f} | {INGRESOS[3,0]:>21.2f} |')
        print(f'| Costes totales  | {CTOTAL[0,0]:>18.2f} | {CTOTAL[1,0]:>18.2f} | {CTOTAL[2,0]:>19.2f} | {CTOTAL[3,0]:>21.2f} |')
        print(f'| Presupuesto     | {PRESUPUESTO[0,0]:>18.2f} | {PRESUPUESTO[1,0]:>18.2f} | {PRESUPUESTO[2,0]:>19.2f} | {PRESUPUESTO[3,0]:>21.2f} |')
        print('|_________________|____________________|____________________|_____________________|_______________________| \n')

        print(f'\nLa Matriz de Markov es:\n{CM}')
        print(f'Costes unitarios de almacenamiento: {Calm_unit}')
        #print(f', El coste fijo es %.2f Francos.',cf); # CF ahora está en la matriz CF
        if ruptadm == 2:
            print(f'(ruptadm= 2) El cliente NO espera. Coste unitario ruptura: {Crupt_unit}')
        else:
            print(f'(ruptadm= 1) El cliente SÍ espera. Coste unitario no servicio: {Cnoserv_unit}')

    except Exception as e:
        print(f"\nError al cargar el archivo '{ficheroc}': {e}")
        print("No se pudo cargar la partida. Saliendo.")
        exit()


# --- Partida Nueva ---
else: # cargar == 2
    clc()
    print('                Introducción de los datos de partida     ')
    print('____________________________________________________________________________\n')
    print('\nEste juego está diseñado para cuatro empresas participantes.')
    print('Las condiciones iniciales de partida serán iguales para cada empresa.')
    print('Los datos que se introducirán a continuación serán la referencia para empezar la partida.\n')

    print('\nEscriba la duración del juego en meses:')
    while True:
        duracion_input = entero_positivo()
        if duracion_input > 0:
            duracion = duracion_input
            break
        else:
            print("La duración debe ser mayor que cero.")

    # Dimensionamiento de matrices
    PRESUPUESTO = np.zeros((n_empresas, duracion + 1))
    V = np.zeros((n_empresas, duracion + 1), dtype=int)
    PVP = np.zeros((n_empresas, duracion + 1))
    CV = np.zeros((n_empresas, duracion + 1))
    CF = np.zeros((n_empresas, duracion + 1))
    STOCK = np.zeros((n_empresas, duracion + 1), dtype=int)
    INGRESOS = np.zeros((n_empresas, duracion + 1))
    UD = np.zeros((n_empresas, duracion + 1), dtype=int)
    CTOTAL = np.zeros((n_empresas, duracion + 1))
    Calm = np.zeros((n_empresas, duracion + 1)) # Coste unitario
    Cnoserv = np.zeros((n_empresas, duracion + 1)) # Coste unitario
    Crupt = np.zeros((n_empresas, duracion + 1)) # Coste unitario
    VENTASPENDIENTES = np.zeros((n_empresas, duracion + 1), dtype=int)
    Ventasreales = np.zeros((n_empresas, duracion + 1), dtype=int)
    CRUPT_TOTAL = np.zeros((n_empresas, duracion + 1))
    CALM_TOTAL = np.zeros((n_empresas, duracion + 1))
    CNOSERV_TOTAL = np.zeros((n_empresas, duracion + 1))
    PUB = np.zeros((n_empresas, duracion + 1))
    mejoras = np.zeros((n_empresas, duracion + 1))

    print('\nEscriba el valor de la demanda total del mercado inicial:')
    ventasmax = entero_positivo() # Demanda total en el mes 0

    print('\nEscriba el precio de venta al público inicial del producto (precio de referencia):')
    pvp_inicial = numero_positivo()
    pvpini = pvp_inicial # Guardar referencia inicial

    # Inicializar ruptadm (se pide dentro del bucle ahora)
    ruptadm = 0 # Se definirá en el bucle

    # Pedir datos iniciales para cada empresa
    for i in range(n_empresas):
        print(f'\n--- Datos Iniciales para {Empresa[i]} ---')
        print(f'Escriba la cantidad inicial de presupuesto disponible por la empresa {Empresa[i]}:')
        presupuesto = numero_positivo()
        PRESUPUESTO[i, 0] = presupuesto

        PVP[i, 0] = pvp_inicial

        print(f'Escriba el coste fijo de la empresa {Empresa[i]}:')
        cf = numero_positivo()
        CF[i, 0] = cf
        # Asumir que el coste fijo es constante para toda la simulación
        CF[i, 1:] = cf

        print(f'Escriba el coste variable por cada unidad fabricada de la empresa {Empresa[i]}:')
        cv = numero_positivo()
        CV[i, 0] = cv

        print(f'Escriba el coste de almacenamiento por unidad de la empresa {Empresa[i]}:')
        calm = numero_positivo()
        Calm[i, :] = calm # Coste de almacenamiento constante

        # Preguntar sobre ruptura solo una vez si es igual para todas, o dentro si es por empresa
        # El código MATLAB lo pide para *cada* empresa, así que lo mantenemos así.
        print('En caso de ruptura, ¿Se permite entregar el pedido en el siguiente período?')
        print('1) Escriba 1 en caso afirmativo.')
        print('2) Escriba 2 en caso contrario.')
        ruptadm_empresa = uno_o_dos()
        # Necesitamos una política general, usamos la de la primera empresa o pedimos una general?
        # El código MATLAB parece usar una única variable 'ruptadm' globalmente después.
        # Vamos a pedirla una vez fuera del bucle y aplicarla a todas.
        if i == 0:
            ruptadm = ruptadm_empresa # Usar la respuesta de la primera empresa para todas

        if ruptadm == 1: # Cliente espera
            print(f'Escriba el coste de no servicio de la empresa {Empresa[i]}:')
            cnoserv = numero_positivo()
            Cnoserv[i, :] = cnoserv # Coste no servicio constante
            Crupt[i, :] = 0 # No hay coste de ruptura si espera
        else: # Cliente no espera (ruptadm == 2)
             print(f'Escriba el coste de ruptura de la empresa {Empresa[i]}:')
             crupt = numero_positivo()
             Crupt[i, :] = crupt # Coste ruptura constante
             Cnoserv[i, :] = 0 # No hay coste no servicio si no espera

    # Matriz de Markov inicial (equitativa)
    CM = np.full((n_empresas, n_empresas), 1.0 / n_empresas)

    # Reparto inicial de ventas (demanda V en mes 0)
    if ventasmax > 0 and n_empresas > 0:
        ventas_base = ventasmax // n_empresas
        ventas_resto = ventasmax % n_empresas
        V[:, 0] = ventas_base
        # Repartir el resto aleatoriamente
        indices_resto = random.sample(range(n_empresas), ventas_resto)
        for idx in indices_resto:
            V[idx, 0] += 1
    else:
         V[:, 0] = 0 # Si no hay ventas o empresas, la demanda es 0

    # Inicializar otras variables para el mes 0 que dependen de V o decisiones
    # En mes 0, asumimos no se fabrica, no hay ventas reales, ni costes asociados a producción/ventas
    UD[:, 0] = 0
    Ventasreales[:, 0] = 0
    VENTASPENDIENTES[:, 0] = 0
    STOCK[:, 0] = 0 # Sin stock inicial
    INGRESOS[:, 0] = 0
    CTOTAL[:, 0] = CF[:, 0] # Coste total inicial es solo el fijo
    CALM_TOTAL[:, 0] = 0
    CRUPT_TOTAL[:, 0] = 0
    CNOSERV_TOTAL[:, 0] = 0
    PUB[:, 0] = 0
    mejoras[:, 0] = 0
    # Presupuesto inicial ya fue pedido. No restar costes fijos aún.
    # El presupuesto se actualizará al final del primer ciclo (mes 1).

# --- Archivo Historial ---
try:
    F2 = open('HISTORIAL.txt', 'w') # Abrir en modo escritura ('w') para empezar limpio
    print("Historial iniciado en HISTORIAL.txt")
except IOError as e:
    print(f"No se pudo crear/abrir el archivo de historial: {e}")
    F2 = None # Marcar que no se pudo abrir

# --- Bucle Principal del Juego ---
for j in range(1, duracion + 1): # Bucle desde el mes 1 hasta 'duracion'
    mes_actual = j - 1
    print(f"\n\n{'='*60}")
    print(f"                   Comienzo del Mes {mes_actual}")
    print(f"{'='*60}")

    # Copiar estado del mes anterior al actual (inicio del mes j)
    PVP[:, j] = PVP[:, j-1]
    CV[:, j] = CV[:, j-1]
    # El presupuesto al inicio del mes j es el final del mes j-1
    PRESUPUESTO[:, j] = PRESUPUESTO[:, j-1]
    STOCK[:, j] = STOCK[:, j-1]
    PUB[:, j] = PUB[:, j-1] # Copia inversión anterior como base
    mejoras[:, j] = mejoras[:, j-1] # Copia inversión anterior como base
    # Los costes unitarios Calm, Crupt, Cnoserv se asumen constantes o ya están en[:, j]
    # Los costes totales se reinician para este mes
    CTOTAL[:, j] = CF[:, 0] # Iniciar coste total con el fijo
    CALM_TOTAL[:, j] = 0
    CRUPT_TOTAL[:, j] = 0
    CNOSERV_TOTAL[:, j] = 0
    INGRESOS[:, j] = 0
    VENTASPENDIENTES[:, j] = 0 # Se calculan al final del mes anterior, pero se resetean aquí? No, se usan.
    # V[:, j] se calculará después de las decisiones
    # UD[:, j] se decidirá ahora
    # Ventasreales[:, j] se calculará al final

    # Guardar CM del inicio del mes para cálculos internos
    CM_inicio_mes = CM.copy()


    # --- Estimación de la demanda ---
    print('\nSe supone que previamente las empresas han realizado un estudio del mercado')
    print('que les permite estimar la variación de la demanda en el sector y así valorar cuántas unidades fabricar.')
    print(f'Como resultado:')
    # Usar ventasmax del mes anterior (calculado al final del bucle anterior)
    print(f'Se estimará una variación en porcentaje respecto al mes {mes_actual-1}, donde la demanda total fue {ventasmax}')

    print('\nEJEMPLO: Si se estima que la demanda variará entre un -10% y un 5%')
    print('         Se dirá que variación de demanda mínima será -10 (valor expresado en porcentaje).')
    print('         Mientras que la variación de demanda máxima será 5 (también expresado en porcentaje).')
    print('\nSuponiendo que la demanda no aumentará a más del doble ni disminuirá a menos de la mitad (Intervalo entre -50% y 100%)') 
    # Ajustado de 200% a 100%

    dem_minima_pct = 0
    dem_maxima_pct = 0
    while True:
        print('\n\nIncremento estimado de demanda mínimo (en porcentaje, ej: -10):')
        try:
            dem_min_input = input('')
            dem_minima_pct = int(dem_min_input)
            if -50 <= dem_minima_pct <= 100: # Rango ajustado
                break
            else:
                print('\nLa demanda mínima esperada debe tomar un valor entero entre -50 y 100.')
        except ValueError:
            print('Entrada inválida. Introduzca un número entero.')

    while True:
        print('\nIncremento estimado de demanda máximo (en porcentaje, ej: 20):')
        try:
            dem_max_input = input('')
            dem_maxima_pct = int(dem_max_input)
            if -50 <= dem_maxima_pct <= 100 and dem_maxima_pct >= dem_minima_pct: # Rango ajustado y >= min
                 break
            else:
                 print('\nLa demanda máxima esperada debe tomar un valor entero entre -50 y 100, y ser >= que la mínima.')
        except ValueError:
            print('Entrada inválida. Introduzca un número entero.')


    # Demanda del mercado estimada (rango)
    demandaminima = round(ventasmax * (100 + dem_minima_pct) / 100)
    demandamaxima = round(ventasmax * (100 + dem_maxima_pct) / 100)
    demandaminima = max(0, demandaminima) # No puede ser negativa
    demandamaxima = max(0, demandamaxima) # No puede ser negativa

    # --- Decisiones de cada empresa ---
    clc()
    CM_despues_decisiones = CM_inicio_mes.copy() # Empezamos con la CM de inicio de mes

    for i in range(n_empresas):
        print(f"\n{'*'*20} Empresa: {Empresa[i]} | Mes: {mes_actual} {'*'*20}")
        print('___________________________________________________________________________\n')

        print(f'La demanda TOTAL del mercado se estima entre {demandaminima} y {demandamaxima}.')
        # Demanda estimada para esta empresa el mes pasado V[i, j-1]
        # Ventas reales mes pasado Ventasreales[i, j-1]
        print(f'Mes pasado ({mes_actual-1}): Demanda estimada={V[i, j-1]}, Ventas reales={Ventasreales[i, j-1]}, Demanda total={ventasmax}')
        print(f'Presupuesto disponible actual: {PRESUPUESTO[i, j]:.2f}') # Presupuesto al inicio del mes j
        print(f'Stock actual: {STOCK[i, j]} unidades.') # Stock al inicio del mes j
        print(f'Coste unitario almacenamiento: {Calm[i, j]:.2f}')
        print(f'Coste variable unitario actual: {CV[i, j]:.2f}') # CV al inicio mes j
        if ruptadm == 2:
            print(f'Política: Cliente NO espera. Coste unitario ruptura: {Crupt[i, j]:.2f}')
        else:
            print(f'Política: Cliente SÍ espera. Coste unitario no servicio: {Cnoserv[i, j]:.2f}')

        print('\nTeniendo en cuenta las estrategias que se llevarán a cabo durante este mes,')
        print('¿cuántas unidades desea fabricar/poner a la venta?')
        UD[i, j] = entero_positivo() # Unidades a fabricar/disponibilizar este mes

        # Bucle para estrategias adicionales
        while True:
            print(f'\n--- Estrategias Adicionales Empresa {Empresa[i]} para Mes {mes_actual} ---')
            print(f'1) Modificar Precio de Venta (actual: {PVP[i, j]:.2f})')
            print(f'2) Invertir en Marketing (mes pasado: {PUB[i, j]:.2f})')
            print(f'3) Invertir en Mejoras Tecnológicas (mes pasado: {mejoras[i, j]:.2f})')
            print(f'4) Modificar Unidades a Fabricar/Vender (actual: {UD[i, j]})')
            print('\n0) ---- Terminar estrategias para este mes ----')

            while True:
                try:
                    modA = input('Seleccione una opción (0-4): ')
                    opcion = int(modA)
                    if 0 <= opcion <= 4:
                        break
                    else:
                        print("Opción inválida.")
                except ValueError:
                    print("Entrada inválida.")

            if opcion == 0:
                break # Salir del bucle de estrategias
            elif opcion == 1:
                # Pasar la CM que se está modificando en este bucle
                PVP, CM_despues_decisiones = precio_vp(PVP, CM_despues_decisiones, Empresa, i, j, pvpini)
            elif opcion == 2:
                # Pasar la CM que se está modificando
                # Pasar el presupuesto inicial del mes j: PRESUPUESTO[:, j]
                # Pasar CTOTAL del mes j para actualizarlo: CTOTAL[:, j]
                CTOTAL, CM_despues_decisiones, PUB = marketing(i, j, CM_despues_decisiones, CTOTAL, PRESUPUESTO, Empresa, PUB, duracion)
            elif opcion == 3:
                 # Pasar la CM que se está modificando
                 # Pasar el presupuesto inicial del mes j: PRESUPUESTO[:, j]
                 # Pasar CTOTAL del mes j para actualizarlo: CTOTAL[:, j]
                 CTOTAL, CV, CM_despues_decisiones, mejoras = mejoras_tecnologicas(i, j, CV, CTOTAL, PRESUPUESTO, Empresa, CM_despues_decisiones, mejoras, duracion)
            elif opcion == 4:
                 print('\n¿Cuántas unidades se pondrán a la venta este mes?')
                 UD[i, j] = entero_positivo()

        clc() # Limpiar pantalla para la siguiente empresa

    # Actualizar la matriz CM global con los cambios acumulados de todas las empresas
    CM = CM_despues_decisiones.copy()

    # --- Cálculo de la Demanda Real y Ventas ---

    # Modificación real de la demanda total del mercado
    aleatorio = random.random() # Entre 0 y 1
    porc_suerte = dem_minima_pct + (dem_maxima_pct - dem_minima_pct) * aleatorio
    ventasmax_nuevo = round(ventasmax * (100 + porc_suerte) / 100)
    ventasmax_nuevo = max(0, ventasmax_nuevo) # Asegurar que no sea negativa
    ventasmax = ventasmax_nuevo # Actualizar para el próximo mes y cálculos actuales

    # Calcular el vector de estado estacionario (probabilidad a largo plazo) de CM
    try:
        eigenvalues, eigenvectors = np.linalg.eig(CM)
        # Encontrar el autovector asociado al autovalor 1 (o cercano a 1)
        indice_ev1 = np.argmin(np.abs(eigenvalues - 1.0))
        pv_estacionario = np.real(eigenvectors[:, indice_ev1]) # Tomar la parte real

        # Normalizar el autovector para que sume 1
        pv_estacionario = pv_estacionario / np.sum(pv_estacionario)
        pv_estacionario = np.maximum(pv_estacionario, 0) # Asegurar no negativos por errores numéricos
        pv_estacionario = pv_estacionario / np.sum(pv_estacionario) # Re-normalizar

        # Calcular la demanda estimada para cada empresa basado en estado estacionario y ventasmax nuevas
        V[:, j] = pv_estacionario * ventasmax

    except np.linalg.LinAlgError:
         print("Advertencia: Error al calcular autovalores/vectores de CM. Usando distribución equitativa.")
         V[:, j] = ventasmax / n_empresas # Fallback

    # Redondear y ajustar para que la suma sea exactamente ventasmax
    V[:, j] = np.floor(V[:, j]) # Usar floor como 'fix' en MATLAB
    ventas_asignadas = int(np.sum(V[:, j]))
    ventas_quedan = ventasmax - ventas_asignadas

    if ventas_quedan > 0 and n_empresas > 0:
        # Repartir las unidades restantes aleatoriamente
        indices_resto = random.sample(range(n_empresas), min(ventas_quedan, n_empresas)) 
    
        # Asegurar que no pidamos más muestras que elementos hay
        # Si quedan más ventas que empresas, podemos dar una a cada una y repetir
        q = 0
        while ventas_quedan > 0:
            idx = indices_resto[q % len(indices_resto)] # Ciclar por los índices si es necesario
            V[idx, j] += 1
            ventas_quedan -= 1
            q += 1
            if q > n_empresas * 2 and ventas_quedan > 0: # Safety break para evitar bucles infinitos
                 print("Advertencia: Problema repartiendo ventas restantes.")
                 # Asignar el resto a la primera empresa
                 V[0,j] += ventas_quedan
                 break


    # --- Cálculo de Ventas Reales, Stock, Costes e Ingresos ---
    # Demanda total para la empresa i este mes = Demanda nueva (V[i,j]) + Pendientes del mes anterior (VENTASPENDIENTES[i, j-1])
    demanda_a_cubrir = V[:, j] + VENTASPENDIENTES[:, j-1]
    unidades_disponibles = UD[:, j] + STOCK[:, j] # Unidades fabricadas + stock inicial

    for i in range(n_empresas):
        if unidades_disponibles[i] >= demanda_a_cubrir[i]:
            # Suficientes unidades
            Ventasreales[i, j] = demanda_a_cubrir[i]
            unidades_vendidas_fabricadas = min(UD[i, j], Ventasreales[i, j])
            unidades_vendidas_stock = Ventasreales[i, j] - unidades_vendidas_fabricadas

            STOCK[i, j] = unidades_disponibles[i] - Ventasreales[i, j] # Stock final
            VENTASPENDIENTES[i, j] = 0 # Toda la demanda cubierta
            CRUPT_TOTAL[i, j] = 0
            CNOSERV_TOTAL[i, j] = 0

        else:
            # No hay suficientes unidades
            Ventasreales[i, j] = unidades_disponibles[i] # Vende todo lo disponible
            faltan = demanda_a_cubrir[i] - Ventasreales[i, j]
            STOCK[i, j] = 0 # Stock final es cero

            if ruptadm == 2: # Cliente no espera
                CRUPT_TOTAL[i, j] = faltan * Crupt[i, j]
                CNOSERV_TOTAL[i, j] = 0
                VENTASPENDIENTES[i, j] = 0
            else: # Cliente sí espera (ruptadm == 1)
                CRUPT_TOTAL[i, j] = 0
                CNOSERV_TOTAL[i, j] = faltan * Cnoserv[i, j]
                VENTASPENDIENTES[i, j] = faltan # Quedan pendientes para el mes siguiente

        # Coste de Almacenamiento (sobre stock final)
        CALM_TOTAL[i, j] = STOCK[i, j] * Calm[i, j]

        # Ingresos
        INGRESOS[i, j] = PVP[i, j] * Ventasreales[i, j]

        # Coste Total (ya incluye Fijo, PUB y Mejoras)
        # Añadir: Variable, Almacenamiento, Ruptura, No Servicio
        CTOTAL[i, j] += CV[i, j] * UD[i, j] # Coste variable de lo fabricado
        CTOTAL[i, j] += CALM_TOTAL[i, j]
        CTOTAL[i, j] += CRUPT_TOTAL[i, j]
        CTOTAL[i, j] += CNOSERV_TOTAL[i, j]

        # Presupuesto Final del Mes j
        # Presupuesto inicial mes j = PRESUPUESTO[i, j] (que era el final de j-1)
        # Presupuesto final mes j = Presup inicial + Ingresos - Costes Totales
        # Guardamos el resultado en la columna j
        PRESUPUESTO[i, j] = PRESUPUESTO[i, j] + INGRESOS[i, j] - CTOTAL[i, j]


    # --- Mostrar Resumen del Mes ---
    clc()
    print(f'\n\n--- Resultados del Mes {mes_actual} ---')
    # Tabla Resumen de Producción
    print('\n--- Datos de Producción ---')
    print('_____________________________________________________________________________________________')
    print('|                       |                            Empresa                                  |')
    print('|       Datos           |_____________________________________________________________________|')
    print('|                       |       Mercedes     |   Peugeot    |Penhard-Levassor|     Mors       |')
    print('|_______________________|____________________|______________|________________|________________|')
    print(f'|  Unidades fabricadas  | {UD[0,j]:>18d} | {UD[1,j]:>12d} | {UD[2,j]:>14d} | {UD[3,j]:>14d} |')
    print(f'| Demanda de la empresa | {V[0,j]:>18d} | {V[1,j]:>12d} | {V[2,j]:>14d} | {V[3,j]:>14d} |')
    print(f'|  Ventas de la empresa | {Ventasreales[0,j]:>18d} | {Ventasreales[1,j]:>12d} | {Ventasreales[2,j]:>14d} | {Ventasreales[3,j]:>14d} |')
    print(f'|  Clientes en espera   | {VENTASPENDIENTES[0,j]:>18d} | {VENTASPENDIENTES[1,j]:>12d} | {VENTASPENDIENTES[2,j]:>14d} | {VENTASPENDIENTES[3,j]:>14d} |')
    print(f'|   Precio de venta     | {PVP[0,j]:>18.2f} | {PVP[1,j]:>12.2f} | {PVP[2,j]:>14.2f} | {PVP[3,j]:>14.2f} |')
    print(f'|     Costes fijos      | {CF[0,j]:>18.2f} | {CF[1,j]:>12.2f} | {CF[2,j]:>14.2f} | {CF[3,j]:>14.2f} |')
    print(f'|   Costes variables    | {CV[0,j]:>18.2f} | {CV[1,j]:>12.2f} | {CV[2,j]:>14.2f} | {CV[3,j]:>14.2f} |')
    print(f'|   Unidades en stock   | {STOCK[0,j]:>18d} | {STOCK[1,j]:>12d} | {STOCK[2,j]:>14d} | {STOCK[3,j]:>14d} |')
    print(f'|    Costes de stock    | {CALM_TOTAL[0,j]:>18.2f} | {CALM_TOTAL[1,j]:>12.2f} | {CALM_TOTAL[2,j]:>14.2f} | {CALM_TOTAL[3,j]:>14.2f} |')
    print(f'| Costes de no servicio | {CNOSERV_TOTAL[0,j]:>18.2f} | {CNOSERV_TOTAL[1,j]:>12.2f} | {CNOSERV_TOTAL[2,j]:>14.2f} | {CNOSERV_TOTAL[3,j]:>14.2f} |')
    print(f'|   Costes de ruptura   | {CRUPT_TOTAL[0,j]:>18.2f} | {CRUPT_TOTAL[1,j]:>12.2f} | {CRUPT_TOTAL[2,j]:>14.2f} | {CRUPT_TOTAL[3,j]:>14.2f} |')
    print('|_______________________|____________________|______________|________________|________________|')

    # Tabla Resumen de Cuentas
    print('\n--- Resumen de Cuentas ---')
    print('_________________________________________________________________________________________________________')
    print('|                 |                                          Empresa                                      |')
    print('|   Resultado     |_______________________________________________________________________________________|')
    print('|                 |       Mercedes     |       Peugeot      |  Penhard-Levassor   |         Mors          |')
    print('|_________________|____________________|____________________|_____________________|_______________________|')
    print(f'| Ingresos        | {INGRESOS[0,j]:>18.2f} | {INGRESOS[1,j]:>18.2f} | {INGRESOS[2,j]:>19.2f} | {INGRESOS[3,j]:>21.2f} |')
    print(f'| Costes totales  | {CTOTAL[0,j]:>18.2f} | {CTOTAL[1,j]:>18.2f} | {CTOTAL[2,j]:>19.2f} | {CTOTAL[3,j]:>21.2f} |')
    print(f'| Presupuesto     | {PRESUPUESTO[0,j]:>18.2f} | {PRESUPUESTO[1,j]:>18.2f} | {PRESUPUESTO[2,j]:>19.2f} | {PRESUPUESTO[3,j]:>21.2f} |')
    print('|_________________|____________________|____________________|_____________________|_______________________| \n')


    # --- Escribir en Historial ---
    if F2:
        try:
            F2.write(f'\n\n--- RESULTADOS DEL MES {mes_actual} ---\n')
            F2.write('\n--- Datos de Producción ---\n')
            F2.write('Empresa             |   Mercedes |    Peugeot | Penhard-L. |       Mors |\n')
            F2.write('--------------------|------------|------------|------------|------------|\n')
            F2.write(f'Unidades fabricadas | {UD[0,j]:>10d} | {UD[1,j]:>10d} | {UD[2,j]:>10d} | {UD[3,j]:>10d} |\n')
            F2.write(f'Demanda estimada (V)| {V[0,j]:>10d} | {V[1,j]:>10d} | {V[2,j]:>10d} | {V[3,j]:>10d} |\n')
            F2.write(f'Ventas reales       | {Ventasreales[0,j]:>10d} | {Ventasreales[1,j]:>10d} | {Ventasreales[2,j]:>10d} | {Ventasreales[3,j]:>10d} |\n')
            F2.write(f'Clientes en espera  | {VENTASPENDIENTES[0,j]:>10d} | {VENTASPENDIENTES[1,j]:>10d} | {VENTASPENDIENTES[2,j]:>10d} | {VENTASPENDIENTES[3,j]:>10d} |\n')
            F2.write(f'Precio venta (PVP)  | {PVP[0,j]:>10.2f} | {PVP[1,j]:>10.2f} | {PVP[2,j]:>10.2f} | {PVP[3,j]:>10.2f} |\n')
            F2.write(f'Coste Fijo (CF)     | {CF[0,j]:>10.2f} | {CF[1,j]:>10.2f} | {CF[2,j]:>10.2f} | {CF[3,j]:>10.2f} |\n')
            F2.write(f'Coste Variable (CV) | {CV[0,j]:>10.2f} | {CV[1,j]:>10.2f} | {CV[2,j]:>10.2f} | {CV[3,j]:>10.2f} |\n')
            F2.write(f'Stock final         | {STOCK[0,j]:>10d} | {STOCK[1,j]:>10d} | {STOCK[2,j]:>10d} | {STOCK[3,j]:>10d} |\n')
            F2.write(f'Coste Stock Total   | {CALM_TOTAL[0,j]:>10.2f} | {CALM_TOTAL[1,j]:>10.2f} | {CALM_TOTAL[2,j]:>10.2f} | {CALM_TOTAL[3,j]:>10.2f} |\n')
            F2.write(f'Coste No Serv Total | {CNOSERV_TOTAL[0,j]:>10.2f} | {CNOSERV_TOTAL[1,j]:>10.2f} | {CNOSERV_TOTAL[2,j]:>10.2f} | {CNOSERV_TOTAL[3,j]:>10.2f} |\n')
            F2.write(f'Coste Ruptura Total | {CRUPT_TOTAL[0,j]:>10.2f} | {CRUPT_TOTAL[1,j]:>10.2f} | {CRUPT_TOTAL[2,j]:>10.2f} | {CRUPT_TOTAL[3,j]:>10.2f} |\n')
            F2.write('--------------------|------------|------------|------------|------------|\n')

            F2.write('\n--- Resumen de Cuentas ---\n')
            F2.write('Resultado           |   Mercedes |    Peugeot | Penhard-L. |       Mors |\n')
            F2.write('--------------------|------------|------------|------------|------------|\n')
            F2.write(f'Ingresos            | {INGRESOS[0,j]:>10.2f} | {INGRESOS[1,j]:>10.2f} | {INGRESOS[2,j]:>10.2f} | {INGRESOS[3,j]:>10.2f} |\n')
            F2.write(f'Costes Totales      | {CTOTAL[0,j]:>10.2f} | {CTOTAL[1,j]:>10.2f} | {CTOTAL[2,j]:>10.2f} | {CTOTAL[3,j]:>10.2f} |\n')
            F2.write(f'Presupuesto Final   | {PRESUPUESTO[0,j]:>10.2f} | {PRESUPUESTO[1,j]:>10.2f} | {PRESUPUESTO[2,j]:>10.2f} | {PRESUPUESTO[3,j]:>10.2f} |\n')
            F2.write('--------------------|------------|------------|------------|------------|\n')

            F2.write(f'\nMatriz CM al final del mes {mes_actual}:\n{CM}\n')
            F2.write(f'Costes unitarios: Calm={Calm[:,j]}, Crupt={Crupt[:,j]}, Cnoserv={Cnoserv[:,j]}\n')
            F2.write(f'Política Ruptura (ruptadm): {ruptadm}\n')
            F2.write(f'Inversión PUB: {PUB[:,j]}\n')
            F2.write(f'Inversión Mejoras: {mejoras[:,j]}\n')

        except IOError as e:
             print(f"Error al escribir en el archivo de historial: {e}")
             if F2: F2.close()
             F2 = None # Marcar que ya no se puede escribir

    # --- Gráfico de Pastel de CM (opcional, puede ralentizar) ---
    # Descomentar si se quiere ver el gráfico de CM cada mes
    # fig_cm_mes, axs_cm_mes = plt.subplots(2, 2, figsize=(10, 7))
    # fig_cm_mes.suptitle(f'Matriz de Markov - Mes {mes_actual}')
    # labels_prefix = ['ME:', 'PE:', 'PL:', 'MO:']
    # for i in range(n_empresas):
    #     ax = axs_cm_mes[i // 2, i % 2]
    #     titulo = f'Prob. cambio desde {Empresa[i]} a:'
    #     datos_pastel = CM[:, i]
    #     if np.isnan(datos_pastel).any(): datos_pastel = np.nan_to_num(datos_pastel)
    #     diagrama_pastel(ax, datos_pastel, titulo, labels_prefix)
    # fig_cm_mes.tight_layout(rect=[0, 0.03, 1, 0.95])
    # plt.show() # Mostrar este gráfico y esperar a que se cierre


    # Pausa para pasar al siguiente mes
    if j < duracion + 1:
        input(f'\n\n--- Fin del Mes {mes_actual}. Presiona Enter para pasar al Mes {mes_actual+1} ---')
    else:
        print('\n_________________________________________________________________')
        print('--------------------- Fin de la partida -----------------------')
        print('_________________________________________________________________\n')
        input('Presiona Enter para ver los gráficos finales y terminar...')


# --- Fin del Juego ---

# Cerrar archivo historial si está abierto
if F2:
    F2.close()
    print("Archivo HISTORIAL.txt cerrado.")

# Mostrar gráficos finales
resultados_finales(V, CM, duracion, UD, PRESUPUESTO, CV, Empresa)

# --- Guardar Partida ---
print('\n¿Desea guardar el estado final de la partida?')
print('1) Escriba 1 para guardar.')
print('2) Escriba 2 para salir sin guardar.')
guardar = uno_o_dos()

if guardar == 1:
    print('¿Qué nombre desea darle al fichero de guardado?')
    print('1) Escriba 1 para elegir el nombre por defecto (Partida_py.dta).')
    print('2) Escriba 2 para poner otro nombre.')
    nombre = uno_o_dos()
    fichero_guardar = ''
    if nombre == 1:
        fichero_guardar = 'Partida_py.dta'
    else:
        fichero_guardar = input('Escriba el nombre del fichero (ej: mi_partida_final.dta):\n')

    try:
        with open(fichero_guardar, 'w') as F1:
            # Guardar datos del último mes (columna j = duracion)
            # Usar un formato similar al de MATLAB para posible compatibilidad (o uno más simple)
            # Formato simple: una línea por variable, valores separados por espacio

            # Datos Producción (último mes)
            F1.write(' '.join(map(str, UD[:, duracion])) + '\n') # UD
            F1.write(' '.join(map(str, V[:, duracion])) + '\n') # V (demanda)
            F1.write(' '.join(map(str, Ventasreales[:, duracion])) + '\n') # Ventas Reales
            F1.write(' '.join(map(str, VENTASPENDIENTES[:, duracion])) + '\n') # Pendientes
            F1.write(' '.join(map(lambda x: f"{x:.2f}", PVP[:, duracion])) + '\n') # PVP
            F1.write(' '.join(map(str, CF[:, duracion].astype(int))) + '\n') # CF (como int?)
            F1.write(' '.join(map(lambda x: f"{x:.2f}", CV[:, duracion])) + '\n') # CV
            F1.write(' '.join(map(str, STOCK[:, duracion])) + '\n') # Stock
            F1.write(' '.join(map(lambda x: f"{x:.2f}", CALM_TOTAL[:, duracion])) + '\n') # CALM Total
            F1.write(' '.join(map(lambda x: f"{x:.2f}", CNOSERV_TOTAL[:, duracion])) + '\n') # CNOSERV Total
            F1.write(' '.join(map(lambda x: f"{x:.2f}", CRUPT_TOTAL[:, duracion])) + '\n') # CRUPT Total

            # Resultados (último mes)
            F1.write(' '.join(map(lambda x: f"{x:.2f}", INGRESOS[:, duracion])) + '\n') # Ingresos
            F1.write(' '.join(map(lambda x: f"{x:.2f}", CTOTAL[:, duracion])) + '\n') # Coste Total
            F1.write(' '.join(map(lambda x: f"{x:.2f}", PRESUPUESTO[:, duracion])) + '\n') # Presupuesto

            # Matriz CM (aplanada)
            F1.write(' '.join(map(lambda x: f"{x:.6f}", CM.flatten(order='C'))) + '\n') # Guardar por filas (C order)

            # Costes unitarios (usar los del último mes, asumiendo constancia o último valor válido)
            F1.write(' '.join(map(lambda x: f"{x:.2f}", Calm[:, duracion])) + '\n') # Calm unitario
            F1.write(f'{ruptadm}\n') # ruptadm
            # Guardar Crupt o Cnoserv unitarios dependiendo de ruptadm
            if ruptadm == 2:
                 F1.write(' '.join(map(lambda x: f"{x:.2f}", Crupt[:, duracion])) + '\n') # Crupt unitario
            else:
                 F1.write(' '.join(map(lambda x: f"{x:.2f}", Cnoserv[:, duracion])) + '\n') # Cnoserv unitario

            # Guardar PUB y mejoras (no se guardaban en MATLAB, pero podría ser útil)
            F1.write(' '.join(map(lambda x: f"{x:.2f}", PUB[:, duracion])) + '\n') # PUB último mes
            F1.write(' '.join(map(lambda x: f"{x:.2f}", mejoras[:, duracion])) + '\n') # Mejoras último mes
            # Guardar PVPini y ventasmax inicial si se quisiera restaurar exactamente
            # F1.write(f'{pvpini}\n')
            # F1.write(f'{V[0,0]}\n') # Guardar demanda inicial?

        print(f"Partida guardada correctamente en '{fichero_guardar}'")

    except IOError as e:
        print(f"Error al guardar la partida en '{fichero_guardar}': {e}")

print("\nFin del programa.")