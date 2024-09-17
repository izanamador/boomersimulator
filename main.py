import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Datos de inflación anual desde 1980 hasta 2024 (porcentajes)
inflacion_salarios_anual = [
    15.59, 14.56, 14.43, 12.19, 11.30, 8.83, 8.80, 5.26, 4.83, 6.79, 6.72, 
    5.94, 5.93, 4.57, 4.72, 4.68, 3.56, 1.97, 1.84, 2.31, 3.43, 3.59, 3.06, 
    3.04, 3.04, 3.37, 3.52, 2.78, 4.09, -0.28, 1.80, 3.20, 2.44, 1.42, -0.15, 
    -0.50, -0.20, 1.96, 1.67, 0.70, -0.32, 3.09, 8.40, 3.56, 3.22
]

# Inflación de viviendas anual desde 1980 hasta 2024 (porcentajes)
inflacion_viviendas_anual = [
    10.3, 10.3, 10.3, 10.3, 10.3, 1.2, 7.7, 9.6, 7.7, 11.1, 17.3, 18.5, 17.2, 
    12.8, 9.1, 4.8, -3.2, -6.3, -3.5, -6.8, -10.0, -5.8, 2.7, 1.8, 1.9, 2.6, 
    3.3, 4.1, 5.0, 6.0, 5.8, 6.7, 8.2, 9.1, 9.7, 6.0, 4.9, 3.7, 4.2, 4.5, 5.0, 
    4.7, 5.2, 6.3, 7.8, 8.0
]

# Convertir porcentajes a fracciones
inflacion_salarios_fracciones = [1 + (i / 100) for i in inflacion_salarios_anual]
inflacion_viviendas_fracciones = [1 + (i / 100) for i in inflacion_viviendas_anual]

# Calcular el factor de inflación acumulada para salarios y viviendas
def calcular_factor_acumulado(inflacion_fracciones):
    factor_acumulado = 1
    for inflacion in inflacion_fracciones:
        factor_acumulado *= inflacion
    return factor_acumulado

factor_inflacion_salarios_acumulado = calcular_factor_acumulado(inflacion_salarios_fracciones)
factor_inflacion_viviendas_acumulado = calcular_factor_acumulado(inflacion_viviendas_fracciones)

# Valores predeterminados
salario_predeterminado = 1200.0  # Salario neto mensual en euros
coste_vivienda_predeterminado = 200000.0  # Precio medio actual de una vivienda en euros

# Función para ajustar el salario
def calcular_salario_ajustado(salario_mensual, factor_inflacion_acumulada):
    salario_anual = salario_mensual * 12
    return salario_anual / factor_inflacion_acumulada / 12

# Función para calcular el coste de la vivienda en el pasado
def calcular_coste_vivienda_pasado(coste_vivienda_actual, factor_inflacion_acumulada):
    return coste_vivienda_actual / factor_inflacion_acumulada

# Función para calcular el tiempo para pagar una casa
def calcular_tiempo_pagar_casa(salario_mensual, coste_vivienda):
    salario_anual = salario_mensual * 12
    if salario_anual > 0:
        return coste_vivienda / (salario_anual / 2)  # Dedicamos la mitad del salario
    else:
        return float('inf')  # Devuelve infinito si el salario es cero

# Título de la app
st.image('logo.png')

# Inputs del usuario
salario_mensual = st.number_input('Introduce tu salario neto mensual (€):', min_value=0.0, format="%.2f", value=salario_predeterminado, step=0.01)
coste_vivienda_actual = st.number_input('Introduce el coste actual de tu vivienda (€):', min_value=0.0, format="%.2f", value=coste_vivienda_predeterminado, step=0.01)

# Botón para calcular
if st.button('Calcular'):
    # Verificar que los inputs no sean cero
    if salario_mensual > 0 and coste_vivienda_actual > 0:
        # Calcula el salario y el coste de vivienda en los años 80
        salario_ajustado = calcular_salario_ajustado(salario_mensual, factor_inflacion_salarios_acumulado)
        coste_vivienda_pasado = calcular_coste_vivienda_pasado(coste_vivienda_actual, factor_inflacion_viviendas_acumulado)

        # Calcula el tiempo para pagar una casa ahora y en el pasado
        tiempo_pagar_casa_actual = calcular_tiempo_pagar_casa(salario_mensual, coste_vivienda_actual)
        tiempo_pagar_casa_pasado = calcular_tiempo_pagar_casa(salario_ajustado, coste_vivienda_pasado)

        # Crear un DataFrame para los gráficos
        data_salario = pd.DataFrame({
            'Categoría': ['Salario Mensual Actual', 'Salario Mensual Años 80'],
            'Euros': [salario_mensual, salario_ajustado]
        })
        
        data_vivienda = pd.DataFrame({
            'Categoría': ['Coste Vivienda Actual', 'Coste Vivienda Años 80'],
            'Euros': [coste_vivienda_actual, coste_vivienda_pasado]
        })

        # Crear gráfico de comparativa de salarios con Plotly
        fig_salario = go.Figure()
        fig_salario.add_trace(go.Bar(
            x=data_salario['Categoría'],
            y=data_salario['Euros'],
            marker_color=['blue', 'lightblue']
        ))
        fig_salario.update_layout(
            title='Comparativa de Salario: Actual vs Años 80',
            xaxis_title='Categoría',
            yaxis_title='Euros',
            template='plotly_dark'
        )

        # Crear gráfico de comparativa de costes de vivienda con Plotly
        fig_vivienda = go.Figure()
        fig_vivienda.add_trace(go.Bar(
            x=data_vivienda['Categoría'],
            y=data_vivienda['Euros'],
            marker_color=['red', 'lightcoral']
        ))
        fig_vivienda.update_layout(
            title='Comparativa de Coste de Vivienda: Actual vs Años 80',
            xaxis_title='Categoría',
            yaxis_title='Euros',
            template='plotly_dark'
        )

        # Mostrar gráficos en Streamlit
        st.plotly_chart(fig_salario)
        st.plotly_chart(fig_vivienda)

        # Tarjetas de tiempo para pagar la vivienda
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Tiempo para pagar la vivienda ahora",
                value=f"{tiempo_pagar_casa_actual:.2f} años",
                delta=f"{tiempo_pagar_casa_actual - tiempo_pagar_casa_pasado:.2f} años"
            )
        with col2:
            st.metric(
                label="Tiempo para pagar la vivienda en los años 80",
                value=f"{tiempo_pagar_casa_pasado:.2f} años",
                delta=f"{tiempo_pagar_casa_pasado - tiempo_pagar_casa_actual:.2f} años"
            )

    else:
        st.warning("Por favor, introduce valores válidos para el salario y el coste de la vivienda.")
