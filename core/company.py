# -*- coding: utf-8 -*-
# core/company.py

import numpy as np
from typing import Dict, Any, Optional # Para type hints
# import utils

class Company:
    """
    Representa una empresa participante en la simulación del Juego de Empresas.

    Almacena el estado de la empresa (financiero, inventario, costes) y
    proporciona métodos para simular sus operaciones y decisiones mensuales.
    """

    def __init__(self, config: Dict[str, Any], ruptadm_global: int):
        """
        Inicializa una instancia de Empresa.

        Args:
            config (Dict[str, Any]): Un diccionario con la configuración inicial
                de la empresa. Debe contener claves como: 'nombre',
                'presupuesto_inicial', 'pvp_inicial', 'coste_fijo_mensual',
                'coste_variable_unitario', 'stock_inicial',
                'coste_almacenamiento_unitario', 'coste_ruptura_unitario',
                'coste_no_servicio_unitario'.
            ruptadm_global (int): Indica si los clientes esperan (1) o no (2)
                                  en caso de ruptura de stock. Afecta qué coste se aplica.
        """
        try:
            self.nombre: str = config['nombre']
            self.presupuesto: float = float(config['presupuesto_inicial'])
            self.pvp: float = float(config['pvp_inicial']) # Precio Venta Público actual
            self.coste_fijo: float = float(config['coste_fijo_mensual'])
            self.coste_variable: float = float(config['coste_variable_unitario']) # Puede cambiar
            self.stock: int = int(config['stock_inicial'])
            self.coste_almacenamiento_unitario: float = float(config['coste_almacenamiento_unitario'])
            self.coste_ruptura_unitario: float = float(config['coste_ruptura_unitario'])
            self.coste_no_servicio_unitario: float = float(config['coste_no_servicio_unitario'])
            self.ruptadm: int = ruptadm_global # 1 si cliente espera, 2 si no

            # --- Atributos de Decisión (se establecerán cada mes) ---
            self.marketing_investment: float = 0.0
            self.tech_investment: float = 0.0
            self.unidades_a_producir: int = 0

            # --- Atributos de Estado Operacional ---
            self.ventas_pendientes: int = 0 # Demanda no satisfecha del mes anterior si ruptadm=1

            # --- Atributos para Resultados del Mes Actual (se resetean) ---
            self.ventas_reales_mes: int = 0
            self.ingresos_mes: float = 0.0
            self.coste_produccion_mes: float = 0.0
            self.coste_almacenamiento_mes: float = 0.0
            self.coste_ruptura_mes: float = 0.0
            self.coste_no_servicio_mes: float = 0.0
            self.coste_marketing_mes: float = 0.0 # Calculado a partir de la inversión
            self.coste_tech_mes: float = 0.0      # Calculado a partir de la inversión
            self.coste_total_mes: float = 0.0

            # --- Validación inicial básica ---
            if self.presupuesto < 0 or self.pvp <= 0 or self.coste_fijo < 0 or \
               self.coste_variable < 0 or self.stock < 0 or \
               self.coste_almacenamiento_unitario < 0 or \
               self.coste_ruptura_unitario < 0 or self.coste_no_servicio_unitario < 0:
                raise ValueError(f"Configuración inicial inválida para {self.nombre}: valores negativos no permitidos.")
            if self.ruptadm not in [1, 2]:
                 raise ValueError(f"Configuración inicial inválida para {self.nombre}: ruptadm debe ser 1 o 2.")

        except KeyError as e:
            raise ValueError(f"Falta la clave de configuración '{e}' para la empresa.") from e
        except (ValueError, TypeError) as e:
             raise ValueError(f"Error en el tipo o valor de configuración para {self.nombre}: {e}") from e

    def __str__(self) -> str:
        """Devuelve una representación legible del estado actual de la empresa."""
        return (f"[{self.nombre}] Presup.: {self.presupuesto:.2f} € | "
                f"Stock: {self.stock} uds | PVP: {self.pvp:.2f} € | "
                f"CV: {self.coste_variable:.2f} €")

    def resetear_metricas_mensuales(self) -> None:
        """Resetea los contadores de resultados mensuales antes de un nuevo ciclo."""
        self.ventas_reales_mes = 0
        self.ingresos_mes = 0.0
        self.coste_produccion_mes = 0.0
        self.coste_almacenamiento_mes = 0.0
        self.coste_ruptura_mes = 0.0
        self.coste_no_servicio_mes = 0.0
        # Los costes de MKT y TECH se basan en la inversión decidida
        self.coste_marketing_mes = self.marketing_investment
        self.coste_tech_mes = self.tech_investment
        self.coste_total_mes = 0.0
        # Las unidades a producir se deciden cada mes, no se resetean aquí necesariamente
        # self.unidades_a_producir = 0

    # --- Métodos de Decisión (Implementación inicial simple / Placeholders) ---

    def decidir_estrategias(self, nuevo_pvp: Optional[float] = None,
                           inv_mkt: Optional[float] = None,
                           inv_tech: Optional[float] = None) -> None:
        """
        Establece las decisiones estratégicas (PVP, Mkt, Tech) para el *próximo* ciclo.
        En una implementación interactiva, estos valores vendrían del input del usuario.
        En una implementación automática, vendrían de una lógica de estrategia.
        """
        if nuevo_pvp is not None and nuevo_pvp > 0:
            self.pvp = nuevo_pvp
        if inv_mkt is not None and inv_mkt >= 0:
            self.marketing_investment = inv_mkt
        if inv_tech is not None and inv_tech >= 0:
            self.tech_investment = inv_tech
        # Nota: Estos valores afectarán los cálculos del *siguiente* mes
        # (actualización de matriz M, actualización de CV, costes directos)

    def decidir_produccion(self, demanda_objetivo_mes: int) -> int:
        """
        Decide cuántas unidades producir este mes.
        Lógica MVP: Producir lo necesario para intentar cubrir la demanda objetivo,
                   considerando el stock actual. Podría limitarse por presupuesto
                   o capacidad en una versión más avanzada.

        Args:
            demanda_objetivo_mes (int): La demanda estimada o calculada para esta
                                       empresa este mes.

        Returns:
            int: Número de unidades que se decide producir.
        """
        necesarias = max(0, demanda_objetivo_mes - self.stock)
        # Lógica simple: producir lo necesario.
        # TODO: Añadir limitaciones (presupuesto, capacidad máxima si existe)
        self.unidades_a_producir = necesarias
        # print(f"Debug [{self.nombre}]: Demanda={demanda_objetivo_mes}, Stock={self.stock}, Decide Producir={self.unidades_a_producir}")
        return self.unidades_a_producir

    # --- Métodos de Actualización de Estado y Cálculo ---

    def actualizar_coste_variable(self, nuevo_cv: float) -> None:
        """
        Actualiza el coste variable unitario.
        Este método sería llamado por la simulación después de calcular el
        efecto de la inversión tecnológica usando la fórmula correspondiente.

        Args:
            nuevo_cv (float): El nuevo valor del coste variable unitario.
        """
        if nuevo_cv >= 0:
            self.coste_variable = nuevo_cv
        else:
            print(f"Advertencia [{self.nombre}]: Intento de asignar coste variable negativo ({nuevo_cv}). Se mantiene el anterior ({self.coste_variable}).")


    def calcular_ventas_y_stock(self, demanda_potencial_mes: int) -> int:
        """
        Calcula las ventas reales basadas en la demanda total (potencial + pendiente)
        y la disponibilidad (stock inicial + producción). Actualiza el stock final
        y las ventas pendientes para el próximo mes.

        Args:
            demanda_potencial_mes (int): La demanda calculada para esta empresa
                                        este mes (sin incluir pendientes).

        Returns:
            int: Número de unidades de demanda no satisfecha este mes.
        """
        demanda_total_a_cubrir = demanda_potencial_mes + self.ventas_pendientes
        unidades_disponibles = self.stock + self.unidades_a_producir

        self.ventas_reales_mes = min(demanda_total_a_cubrir, unidades_disponibles)
        self.ventas_reales_mes = max(0, self.ventas_reales_mes) # Asegurar no negativo

        unidades_no_satisfechas = max(0, demanda_total_a_cubrir - unidades_disponibles)

        # Actualizar stock: el que había + producido - vendido
        self.stock = unidades_disponibles - self.ventas_reales_mes
        self.stock = max(0, self.stock) # Asegurar no negativo

        # Actualizar ventas pendientes para el *próximo* mes
        if self.ruptadm == 1: # Si cliente espera
            self.ventas_pendientes = unidades_no_satisfechas
        else: # Si cliente no espera, las ventas se pierden
            self.ventas_pendientes = 0

        # print(f"Debug [{self.nombre}]: DemPot={demanda_potencial_mes}, PendAnt={self.ventas_pendientes_ant}, DemTotal={demanda_total_a_cubrir}, Disp={unidades_disponibles}, Ventas={self.ventas_reales_mes}, StockFin={self.stock}, NoSat={unidades_no_satisfechas}, PendProx={self.ventas_pendientes}")
        return unidades_no_satisfechas


    def calcular_costes_e_ingresos(self, unidades_no_satisfechas: int) -> None:
        """
        Calcula todos los ingresos y costes del mes actual basados en las
        operaciones realizadas (producción, ventas, stock final, etc.).
        """
        # Ingresos
        self.ingresos_mes = self.ventas_reales_mes * self.pvp

        # Costes Variables de Producción
        self.coste_produccion_mes = self.unidades_a_producir * self.coste_variable

        # Coste de Almacenamiento (sobre el stock que queda al FINAL del mes)
        self.coste_almacenamiento_mes = self.stock * self.coste_almacenamiento_unitario

        # Coste por Demanda No Satisfecha
        if unidades_no_satisfechas > 0:
            if self.ruptadm == 1: # Cliente espera -> Coste No Servicio
                self.coste_no_servicio_mes = unidades_no_satisfechas * self.coste_no_servicio_unitario
                self.coste_ruptura_mes = 0.0
            else: # Cliente no espera -> Coste Ruptura
                self.coste_ruptura_mes = unidades_no_satisfechas * self.coste_ruptura_unitario
                self.coste_no_servicio_mes = 0.0
        else:
            self.coste_ruptura_mes = 0.0
            self.coste_no_servicio_mes = 0.0

        # Costes de Decisiones Estratégicas (ya asignados en resetear_metricas o decidir_estrategias)
        self.coste_marketing_mes = self.marketing_investment
        self.coste_tech_mes = self.tech_investment

        # Coste Total Mensual
        self.coste_total_mes = (self.coste_fijo +
                                self.coste_produccion_mes +
                                self.coste_almacenamiento_mes +
                                self.coste_ruptura_mes +
                                self.coste_no_servicio_mes +
                                self.coste_marketing_mes +
                                self.coste_tech_mes)

    def actualizar_presupuesto(self) -> None:
        """
        Actualiza el presupuesto de la empresa al final del mes,
        sumando los ingresos y restando los costes totales del mes.
        """
        beneficio_neto_mes = self.ingresos_mes - self.coste_total_mes
        self.presupuesto += beneficio_neto_mes
        # print(f"Debug [{self.nombre}]: Ing={self.ingresos_mes:.2f}, CostT={self.coste_total_mes:.2f}, Benef={beneficio_neto_mes:.2f}, PresupFin={self.presupuesto:.2f}")

    def __print__(self) -> str:
        """
        Devuelve una representación legible del estado actual de la empresa,
        orientada a la simulación (información más resumida y amigable).
        """
        return (f"Empresa: {self.nombre} | Presupuesto: {self.presupuesto:.2f} € | "
                f"Stock: {self.stock} uds | PVP: {self.pvp:.2f} €")

    def __repr__(self) -> str:
        """
        Devuelve una representación detallada del estado actual de la empresa,
        orientada a depuración (información más técnica y completa).
        """
        return (f"Company(nombre={self.nombre}, presupuesto={self.presupuesto:.2f}, "
                f"pvp={self.pvp:.2f}, coste_fijo={self.coste_fijo:.2f}, "
                f"coste_variable={self.coste_variable:.2f}, stock={self.stock}, "
                f"ruptadm={self.ruptadm})")
