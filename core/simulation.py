# -*- coding: utf-8 -*-
# core/simulation.py

import numpy as np
import random
from typing import List, Dict, Any, Optional
from utils import file_manager, math_utils, helpers

# Importar la clase Company (asumiendo que está en el mismo directorio 'core')
try:
    from .company import Company
except ImportError:
    # Permitir ejecución si company.py está en el mismo directorio (para pruebas)
    from company import Company

# TODO: Importar funciones específicas de core/functions.py cuando se implementen
# from .functions import calcular_efecto_precio_m, calcular_efecto_mkt_m, ...
# from .math_utils import normalizar_columna_m

class Simulation:
    """
    Orquesta la simulación del Juego de Empresas.

    Gestiona las empresas participantes, el estado del mercado (demanda),
    la matriz de transición de Markov, y ejecuta la simulación mes a mes.
    """

    def __init__(self, empresas: List[Company],
                 markov_inicial: np.ndarray,
                 demanda_inicial: int,
                 ruptadm_global: int):
        """
        Inicializa la simulación completa.

        Args:
            lista_configs_empresas: Lista de diccionarios, cada uno con la
                                     configuración para inicializar una Company.
            markov_inicial: Matriz NumPy (NxN) con las probabilidades de
                             transición iniciales.
            demanda_inicial: Demanda total inicial del mercado.
            ruptadm_global: Configuración global (1 o 2) que indica si los
                             clientes esperan en caso de ruptura de stock.
        """
        self.num_empresas: int = len(empresas)
        if self.num_empresas <= 0:
            raise ValueError("La simulación debe tener al menos una empresa.")

        # Validar número de empresas e inicializar
        self.num_empresas: int = len(empresas)
        if self.num_empresas <= 0:
            raise ValueError("La simulación debe tener al menos una empresa.")
        else:
            self.empresas: List[Company] = empresas
        
        # Validar que todos los elementos sean instancias de Company
        if not all(isinstance(empresa, Company) for empresa in empresas):
            raise TypeError("Todos los elementos de la lista deben ser instancias de la clase Company.")

        # Validar y almacenar matriz de Markov
        if markov_inicial.shape != (self.num_empresas, self.num_empresas):
            raise ValueError(f"Dimensiones de matriz Markov ({markov_inicial.shape}) no coinciden con nº empresas ({self.num_empresas})")
        self.markov_matrix: np.ndarray = np.array(markov_inicial, dtype=float)
        self._validar_y_normalizar_matriz_markov() # Asegurar que es estocástica

        # Estado del mercado
        if demanda_inicial < 0:
            raise ValueError("La demanda inicial no puede ser negativa.")
        self.market_demand: int = demanda_inicial
        self.current_month: int = 0
        self.ruptadm: int = ruptadm_global

        # (Opcional) Historial para análisis posterior
        self.historial_presupuesto: List[List[float]] = [[] for _ in range(self.num_empresas)]
        self.historial_stock: List[List[int]] = [[] for _ in range(self.num_empresas)]
        self.historial_ventas: List[List[int]] = [[] for _ in range(self.num_empresas)]
        self.historial_cuota_mercado: List[List[float]] = [[] for _ in range(self.num_empresas)]
        # Guardar estado inicial en historial
        self._guardar_estado_historial()


    def _validar_y_normalizar_matriz_markov(self, matriz: Optional[np.ndarray] = None) -> None:
        """
        Verifica si una matriz es estocástica por columnas y la normaliza si es necesario.
        Opera sobre self.markov_matrix si no se pasa otra matriz.
        """
        target_matrix = matriz if matriz is not None else self.markov_matrix

        if np.any(target_matrix < 0):
            print("Advertencia: Se encontraron valores negativos en la matriz de Markov. Ajustando a 0.")
            target_matrix[target_matrix < 0] = 0

        col_sums = np.sum(target_matrix, axis=0)

        # Columnas con suma cero (problemático) - distribuir equitativamente
        zero_sum_cols = np.where(np.isclose(col_sums, 0))[0]
        if zero_sum_cols.size > 0:
            print(f"Advertencia: Columnas {zero_sum_cols} de la matriz Markov suman cero. Estableciendo distribución equitativa.")
            target_matrix[:, zero_sum_cols] = 1.0 / self.num_empresas
            col_sums = np.sum(target_matrix, axis=0) # Recalcular sumas

        # Normalizar columnas cuya suma no sea (aproximadamente) 1
        non_stochastic_cols = ~np.isclose(col_sums, 1.0)
        if np.any(non_stochastic_cols):
             cols_to_normalize = np.where(non_stochastic_cols)[0]
             # print(f"Advertencia: Normalizando columnas {cols_to_normalize} de la matriz de Markov.")
             # Evitar división por cero en columnas que ya eran cero (aunque se manejó antes)
             valid_sums = col_sums[non_stochastic_cols]
             valid_sums[np.isclose(valid_sums, 0)] = 1.0 # Evita dividir por 0
             target_matrix[:, non_stochastic_cols] /= valid_sums[np.newaxis, :]

        # Re-verificar por si acaso (opcional)
        # final_col_sums = np.sum(target_matrix, axis=0)
        # if not np.allclose(final_col_sums, 1.0):
        #     print("Error crítico: La normalización de la matriz de Markov falló.")


    def _update_markov_matrix(self) -> None:
        """
        Actualiza la matriz de Markov (self.markov_matrix).

        *** ¡¡¡ LÓGICA CENTRAL PENDIENTE !!! ***
        Esta función debe:
        1. Obtener las decisiones relevantes de cada empresa (PVP, MKT inv, TECH inv).
        2. Calcular los efectos individuales de estas decisiones en los elementos
           de la matriz de Markov (probablemente en los m_ii) usando las
           fórmulas de `core/functions.py`.
        3. Aplicar estos cambios a una copia de la matriz actual.
        4. Implementar la lógica de redistribución del cambio en los elementos
           no diagonales de cada columna afectada.
        5. Validar y normalizar la matriz resultante usando
           `self._validar_y_normalizar_matriz_markov()`.
        6. Actualizar `self.markov_matrix` con la nueva matriz calculada.
        """
        # print("Debug: _update_markov_matrix - Lógica pendiente.")
        # TODO: Implementar la lógica de actualización basada en decisiones y fórmulas PDF.
        # Ejemplo placeholder: No hacer nada, la matriz se queda como está.
        
        # Inicializar una nueva matriz de Markov (copia de la actual)
        new_markov_matrix = self.markov_matrix.copy()

        # Aquí iría la lógica de actualización de la matriz basada en decisiones de las empresas
        for i, empresa in enumerate(self.empresas):
            # Obtener decisiones de la empresa (PVP, MKT, TECH)
            pvp = empresa.pvp
            inv_mkt = empresa.marketing_investment
            inv_tech = empresa.tech_investment

            # Calcular efectos en la matriz de Markov (placeholder)
            # Aquí deberías aplicar las fórmulas del PDF para cada empresa
            # Por ejemplo:
            # new_markov_matrix[i, :] = calcular_efecto_precio_m(pvp, inv_mkt, inv_tech)

            # Placeholder: No hacer nada por ahora



        pass
        # Al final, siempre validar/normalizar
        self._validar_y_normalizar_matriz_markov()


    def _calculate_equilibrium(self) -> np.ndarray:
        """
        Calcula el vector de cuota de mercado de equilibrio (autovector para lambda=1).

        Returns:
            Vector NumPy (num_empresas,) con las cuotas de mercado normalizadas.
        """
        try:
            eigvals, eigvecs = np.linalg.eig(self.markov_matrix)
            # Encontrar el índice del autovalor más cercano a 1
            idx_eigen_1 = np.argmin(np.abs(eigvals - 1.0))
            # Tomar el autovector correspondiente (parte real)
            equilibrium_vector = np.real(eigvecs[:, idx_eigen_1])
            # Asegurar no negatividad y normalizar
            equilibrium_vector = np.maximum(equilibrium_vector, 0)
            norma = np.sum(equilibrium_vector)
            if norma < 1e-9:
                print("Advertencia: Norma del autovector de equilibrio casi nula. Usando distribución equitativa.")
                market_share = np.ones(self.num_empresas) / self.num_empresas
            else:
                market_share = equilibrium_vector / norma
            return market_share

        except np.linalg.LinAlgError as e:
            print(f"Error en cálculo de autovectores ({e}). Usando distribución equitativa.")
            return np.ones(self.num_empresas) / self.num_empresas


    def _distribute_demand(self, market_share_vector: np.ndarray) -> np.ndarray:
        """
        Distribuye la demanda total del mercado según las cuotas de mercado.
        Maneja el redondeo para que la suma total coincida.

        Args:
            market_share_vector: Vector con las cuotas de mercado (debe sumar 1).

        Returns:
            Vector NumPy (num_empresas,) con la demanda entera asignada a cada empresa.
        """
        if not np.isclose(np.sum(market_share_vector), 1.0):
             print("Advertencia: El vector de cuota de mercado no suma 1. Normalizando.")
             market_share_vector = market_share_vector / np.sum(market_share_vector)

        demand_float = market_share_vector * self.market_demand
        demand_int = np.floor(demand_float).astype(int)
        demand_remaining = self.market_demand - np.sum(demand_int)

        # Distribuir el resto (redondeo) aleatoriamente
        indices = list(range(self.num_empresas))
        random.shuffle(indices)
        for i in range(int(round(demand_remaining))):
             idx_to_add = indices[i % self.num_empresas]
             demand_int[idx_to_add] += 1

        return demand_int


    def _update_market_demand(self) -> None:
        """
        Actualiza la demanda total del mercado para el *próximo* mes.
        Lógica MVP: Constante.
        TODO: Implementar fluctuación basada en PDF (ej: +/- 10% aleatorio).
        """
        # Ejemplo de fluctuación simple (descomentar para probar):
        fluctuacion = random.uniform(-0.10, 0.10) # +/- 10%
        self.market_demand = max(0, int(round(self.market_demand * (1 + fluctuacion))))

        
        # print(f"Debug: Nueva demanda mercado para mes {self.current_month + 1}: {self.market_demand}")
        pass


    def _get_company_decisions(self) -> None:
        """
        Obtiene las decisiones estratégicas y de producción de cada empresa para el mes actual.
        En esta versión, llama a los métodos placeholder de Company.
        TODO: Implementar lógica interactiva o basada en estrategias predefinidas.
        """
        # print("Debug: Obteniendo decisiones de empresas...")
        for i, empresa in enumerate(self.empresas):
            # 1. Decisiones Estratégicas (PVP, MKT, TECH) - Afectan próximo ciclo o M. Markov actual
            # TODO: Obtener estas decisiones (input usuario, estrategia fija, etc.)
            nuevo_pvp = empresa.pvp # Mantener el actual por defecto
            inv_mkt = empresa.marketing_investment # Mantener la actual por defecto
            inv_tech = empresa.tech_investment # Mantener la actual por defecto
            empresa.decidir_estrategias(nuevo_pvp, inv_mkt, inv_tech)

            # 2. Decisión de Producción - Afecta ciclo actual
            # La demanda objetivo se calculará después del equilibrio
            # Aquí solo preparamos, la llamada real a decidir_produccion se hará luego.
            pass


    def _apply_tech_effect_on_costs(self) -> None:
        """
        Calcula y aplica el efecto de la inversión tecnológica en los costes variables.
        *** ¡¡¡ LÓGICA PENDIENTE !!! ***
        Debe:
        1. Iterar por cada empresa.
        2. Obtener su `tech_investment` actual.
        3. Calcular el nuevo `coste_variable` usando la fórmula logarítmica
           de `core/functions.py` [Ref: PDF Sec 4.1.2.3].
        4. Llamar a `empresa.actualizar_coste_variable(nuevo_cv)`.
        """
        # print("Debug: _apply_tech_effect_on_costs - Lógica pendiente.")
        # TODO: Implementar cálculo y llamada a empresa.actualizar_coste_variable
        pass


    def _guardar_estado_historial(self) -> None:
        """Guarda el estado actual relevante en las listas de historial."""
        try:
            cuotas = self._calculate_equilibrium()
            for i, empresa in enumerate(self.empresas):
                self.historial_presupuesto[i].append(empresa.presupuesto)
                self.historial_stock[i].append(empresa.stock)
                self.historial_ventas[i].append(empresa.ventas_reales_mes) # Ventas del mes que acaba de terminar
                self.historial_cuota_mercado[i].append(cuotas[i])
        except Exception as e:
            print(f"Error al guardar historial en mes {self.current_month}: {e}")


    def run_step(self) -> None:
        """Ejecuta un mes (paso) completo de la simulación."""
        self.current_month += 1
        print(f"\n▶ INICIO MES {self.current_month} ================")

        # 1. Resetear métricas mensuales de las empresas
        for empresa in self.empresas:
            empresa.resetear_metricas_mensuales()

        # 2. Obtener/Establecer Decisiones Estratégicas (PVP, MKT, TECH)
        #    (Estas decisiones influirán en la actualización de M y costes)
        self._get_company_decisions()

        # 3. Aplicar efecto de Inversión Tecnológica en Costes Variables
        self._apply_tech_effect_on_costs() # Actualiza CV de las empresas

        # 4. Actualizar Matriz de Markov (basado en PVP, MKT, TECH)
        #    *** ¡¡¡ LÓGICA CRÍTICA PENDIENTE !!! ***
        self._update_markov_matrix()
        # print("Matriz de Markov actualizada:")
        # print(self.markov_matrix)

        # 5. Calcular equilibrio y cuotas de mercado
        market_shares = self._calculate_equilibrium()
        # print(f"Cuotas de Mercado ({self.current_month}): {np.round(market_shares, 3)}")

        # 6. Distribuir demanda del mercado actual
        demand_per_company = self._distribute_demand(market_shares)
        # print(f"Demanda Asignada ({self.current_month}): {demand_per_company}")

        # 7. Ciclo de Producción, Ventas, Costes y Presupuesto para CADA empresa
        print(f"--- Operaciones Mes {self.current_month} ---")
        for i, empresa in enumerate(self.empresas):
            print(f"-> Procesando {empresa.nombre}...")
            demanda_potencial_mes = demand_per_company[i]

            # a. Decidir producción (basado en demanda asignada y estado actual)
            empresa.decidir_produccion(demanda_potencial_mes)

            # b. Calcular ventas reales y actualizar stock / ventas pendientes
            uds_no_satisfechas = empresa.calcular_ventas_y_stock(demanda_potencial_mes)

            # c. Calcular costes e ingresos del mes
            empresa.calcular_costes_e_ingresos(uds_no_satisfechas)

            # d. Actualizar presupuesto
            empresa.actualizar_presupuesto()

        # 8. Actualizar la demanda total del mercado para el *próximo* mes
        self._update_market_demand()

        # 9. Guardar estado en historial
        self._guardar_estado_historial()

        # 10. (Opcional) Mostrar resultados parciales del mes
        # self.print_monthly_report()

        print(f"◀ FIN MES {self.current_month} ====================")


    def run_simulation(self, num_months: int) -> None:
        """Ejecuta la simulación completa durante un número de meses."""
        print(f"\n===== INICIANDO SIMULACIÓN POR {num_months} MESES =====")
        initial_month = self.current_month
        final_month = initial_month + num_months
        while self.current_month < final_month:
            try:
                self.run_step()
            except Exception as e:
                print(f"\n¡ERROR FATAL EN MES {self.current_month}!")
                print(f"Detalle: {e}")
                import traceback
                traceback.print_exc()
                print("Simulación abortada.")
                break
        else: # Se ejecuta si el bucle while termina normalmente (sin break)
            print("\n===== SIMULACIÓN COMPLETADA NORMALMENTE =====")
            self.print_final_results()


    def print_monthly_report(self) -> None:
        """Imprime un resumen del estado actual de todas las empresas."""
        print(f"\n--- REPORTE MES {self.current_month} ---")
        for empresa in self.empresas:
            print(empresa) # Usa el __str__ de Company
            # Podrías añadir más detalles aquí si quieres
        print(f"Demanda Total Mercado Próximo Mes: {self.market_demand}")
        print("-" * 40)

    def print_final_results(self) -> None:
        """Imprime un resumen final al terminar la simulación."""
        print("\n===== RESULTADOS FINALES =====")
        print(f"Simulación finalizada en el mes {self.current_month}")
        print("-" * 30)
        for i, empresa in enumerate(self.empresas):
            print(f"Empresa: {empresa.nombre}")
            print(f"  Presupuesto Final: {empresa.presupuesto:.2f} €")
            print(f"  Stock Final: {empresa.stock} uds")
            if self.historial_ventas[i]:
                 print(f"  Ventas Totales (aprox): {sum(self.historial_ventas[i])} uds")
            if self.historial_cuota_mercado[i]:
                 print(f"  Cuota Mercado Final (aprox): {self.historial_cuota_mercado[i][-1]:.2%}")
            print("-" * 20)
        # TODO: Añadir más análisis si se desea (beneficio total, etc.)

    # --- Métodos para Guardar/Cargar (Placeholders) ---
    # TODO: Implementar usando file_manager.py o similar
    def save_state(self, filepath: str) -> None:
        """Guarda el estado actual completo de la simulación."""
        print(f"TODO: Implementar guardado de estado en {filepath}")
        # Necesitaría serializar self.empresas, self.markov_matrix, self.market_demand, etc.

    def load_state(self, filepath: str) -> None:
        """Carga el estado de la simulación desde un archivo."""
        print(f"TODO: Implementar carga de estado desde {filepath}")
        # Necesitaría deserializar y restaurar todos los atributos.

