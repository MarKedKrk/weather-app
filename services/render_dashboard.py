import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from django.db.models.signals import pre_save


def render_dashboard(file):

    df = pd.read_csv(file)

    st.set_page_config(
        layout="wide",
        page_title="Weather Viewer"
    )

    st.title("Dashboard pogodowy")

    labels = {
        "wind_speed": "Prędkość wiatru",
        "pressure": "Ciśnienie",
        "clouds": "Zachmurzenie"
    }

    st.sidebar.header("Opcje widoku")
    selected_column = st.sidebar.selectbox(
        "Wybierz kolumnę do wykresu",
        ["wind_speed", "pressure", "clouds"],
        format_func=lambda x: labels[x],
    )
    show_table = st.sidebar.checkbox(
        "Pokaż tabelę",
        value=True
    )



    if df.empty:
        st.warning("Brak danych do wyświetlenia")
        return

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['sunrise'] = pd.to_datetime(df['sunrise'])
    df['sunset'] = pd.to_datetime(df['sunset'])

#   Najnowszy rekord pogodowy
    last_row = df.iloc[-1]

    st.subheader('Aktualna pogoda')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        temp = last_row['temperature']
        col1.metric('Temperatura', f'{temp} °C')
    with col2:
        feels_like = last_row['feels_like']
        col2.metric("Temperatura odczuwalna", f'{feels_like} °C')
    with col3:
        pressure = last_row['pressure']
        col3.metric('Ciśnienie', f'{pressure} hPa')
    with col4:
        wind_speed = last_row['wind_speed']
        col4.metric('Prędkość wiatru', f'{wind_speed} km/h')

    st.divider()

    stat1, stat2, stat3, stat4 = st.columns(4)

    with stat1:
        stat1.info(
            f"Średnia temeratura: {df['temperature'].mean():.2f} °C\n\n"
            f"Minimalna temeratura: {df['temperature'].min():.2f} °C\n\n"
            f"Maksymalna temeratura: {df['temperature'].max():.2f} °C\n\n"
        )
    with stat2:
        stat2.warning(
            f"Średnia temeratura odczuwalna: {df['feels_like'].mean():.2f} °C\n\n"
            f"Minimalna temeratura odczuwalna: {df['feels_like'].min():.2f} °C\n\n"
            f"Maksymalna temeratura odczuwalna: {df['feels_like'].max():.2f} °C\n\n"
        )
    with stat3:
        stat3.error(
            f"Średnie ciśnienie: {df['pressure'].mean():.2f} hPa\n\n"
            f"Minimalne ciśnienie: {df['pressure'].min():.2f} hPa\n\n"
            f"Maksymalne ciśnienie: {df['pressure'].max():.2f} hPa\n\n"
        )
    with stat4:
        stat4.success(
            f"Średnie zachmurzenie: {df['clouds'].mean():.2f} %\n\n"
            f"Minimalne zachmurzenie: {df['clouds'].min():.2f} %\n\n"
            f"Maksymalne zachmurzenie: {df['clouds'].max():.2f} %\n\n"
        )

    st.divider()

    st.subheader('Wykresy liniowe')

    line1, line2 = st.columns(2)

    with line1:
        st.markdown("**Temperatura w czasie**")
        st.line_chart(
            df,
            x = "timestamp",
            y = ["temperature", "feels_like"]
        )

    with line2:
        st.markdown(f"**{selected_column} w czasie**")
        st.line_chart(
            df,
            x = "timestamp",
            y = selected_column
        )

    st.divider()

    st.subheader('Wschód i zachód słońca')

    sunrise_col, sunset_col = st.columns(2)

    with sunrise_col:
        sunrise_col.metric(
            "Wschód słońca",
            last_row['sunrise'].strftime("%H:%M"),
        )

    with sunset_col:
        sunset_col.metric(
            "Zachód słońca",
            last_row['sunset'].strftime("%H:%M"),
        )

    st.divider()

    if show_table:
        st.subheader('Tabela danych - Wszystkie rekordy')
        st.dataframe(
            df,
            use_container_width=True,
        )

    else:
        st.subheader('Tabela danych - Ostatnie 10 rekordów')
        st.dataframe(
            df.tail(10),
            use_container_width=True,
            hide_index= True
        )

    st.divider()

    st.subheader('Statystyka')

    numeric_df = df.select_dtypes(include="number")

    if not numeric_df.empty:
        st.dataframe(
            numeric_df.describe(),
            use_container_width=True,
        )

    st.divider()

    st.subheader('Rozkład zachmurzenia')

    st.pyplot(
        df['clouds'].plot.hist(
            bins=10,
            title="Zachmurzenie",
        ).figure
    )