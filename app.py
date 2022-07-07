import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
import requests
st.set_page_config(page_title='Diplomado UniCor', layout='wide')


def plot_heatmap(df: pd.DataFrame, x: str, y: str):
    data_heatmap = (
        df.reset_index()[[x, y, "index"]]
            .groupby([x, y])
            .count()
            .reset_index()
            .pivot(x, y, "index")
            .fillna(0)
    )
    fig = px.imshow(
        data_heatmap,
        color_continuous_scale="Reds",
        aspect="auto",
        title=f"Heatmap {x} vs {y}",
    )
    fig.update_traces(
        hovertemplate="<b><i>"
                      + y
                      + "</i></b>: %{y} <br><b><i>"
                      + x
                      + "</i></b>: %{x} <br><b><i>Conteo interacción variables</i></b>: %{z}<extra></extra>"
    )
    return fig

def dibujar_serie_tiempo(data, x = 'Fechas', y = "confirmados", title="Casos de COVID Confirmados en Colombia" )  :
    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=["red", "blue"],
    )

    fig.update_layout(yaxis_title="Casos confirmados", xaxis_title="Fecha")
    # Esto elimina el color del fondo:
    fig.update_layout({"plot_bgcolor": "rgba(0,0,0,0)", "paper_bgcolor": "rgba(0,0,0,0)"})

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list(
                [
                    dict(step="day", stepmode="backward", label="1 semana", count=7),
                    dict(step="month", stepmode="backward", label="1 mes", count=1),
                    dict(step="month", stepmode="backward", label="3 meses", count=3),
                    dict(step="month", stepmode="backward", label="6 meses", count=6),
                    dict(label="Todos", step="all"),
                ]
            )
        ),
    )
    fig.update_traces(
        hovertemplate="<b><i>"
                      + "Casos confirmados"
                      + "</i></b>: %{y} <br><b><i>"
                      + "Fecha"
                      + "</i></b>: %{x} <extra></extra>"
    )
    return fig

@st.cache(allow_output_mutation=True)
def cargar_datos():
    data = pd.read_csv(
            "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
        )
    data = data[data["Country/Region"] == 'Colombia']
    melted = data.melt(
        var_name="Fechas",
        value_name="confirmados",
        id_vars=["Province/State", "Country/Region", "Lat", "Long"],
    ).copy()
    melted["Fechas"] = melted["Fechas"].apply(
        lambda x: datetime.datetime.strptime(x, "%m/%d/%y")
    )

    return melted

def hacer_request_api(average_monthly_hours, satisfaction_level, salary_level):
    request_data = [{"average_monthly_hours": average_monthly_hours,
                     "satisfaction_level": satisfaction_level,
                     "salary_level": salary_level}]

    data_cleaned = str(request_data).replace("'", '"')

    url_api = "https://api-diplomadopython.herokuapp.com/predict"

    pred = requests.post(url=url_api, data=data_cleaned).text

    pred_df = pd.read_json(pred)
    return pred_df

datos = cargar_datos()
fig = dibujar_serie_tiempo(datos)


col1, col2 = st.columns([1,3])

col1.markdown('''
# Soy un header en markdown

Queda bonito :) 

**Poner en negrilla**
''')

col2.plotly_chart(fig, use_container_width=True)


st.sidebar.header("Controladores cool")

average_monthly_hours = st.sidebar.number_input(label='Average monthly hours', min_value=96, max_value=310,
                                                step=1, value=250)
satisfaction_level = st.sidebar.slider(label='Satisfaction level', min_value=0.0, max_value=1.0,
                                       step=0.01, value=0.39)
salary_level = st.sidebar.selectbox(label = 'Salary level', options = ['low', 'medium', 'high'])

boton_predecir = st.sidebar.button(label="OPRIME PARA PREDECIR")



@st.cache
def cargar_df2():
    return pd.read_csv('datos.csv')

df = cargar_df2()

col1, col2= st.columns(2)

opciones1 = list(df.columns)
heatmapx = col1.selectbox(label="Y del heatmap", options= opciones1)
opciones2 = opciones1.copy()
opciones2.pop(opciones1.index(heatmapx))
heatpmapy = col1.selectbox(label="X del heatmap", options= opciones2)

col2.plotly_chart(plot_heatmap(df, x=heatmapx, y =heatpmapy), use_container_width=True)



if boton_predecir:
    prediccion = hacer_request_api(average_monthly_hours, satisfaction_level, salary_level)
    st.metric(value=f'{prediccion["employee_left"][0]*100}%', label = 'Probabilidad de Renuncia del Empleado')
    st.balloons()

st.markdown(
    """<style> 
    div[data-testid="column"] div[data-testid="stVerticalBlock"]{
    display: flex;
    text-align: center;
    justify-content: center;
    } 

    div[data-testid="column"] {
    display: flex;
    text-align: center;
    justify-content: center;
    } 

    div[data-testid="stVerticalBlock"] div[data-testid="stMarkdownContainer"] h2, h1 {
        justify-content: center;
        text-align: center;
        background-color:#FF4B4B;
        border-radius: 8vh;
    }
    
    div[data-testid="metric-container"] {
        justify-content: center;
        text-align: center;
        background-color:#FF4B4B;
        border-radius: 8vh;
    }

    </style>

""", unsafe_allow_html=True)