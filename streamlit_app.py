# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f"Customize your smoothie :balloon: {st.__version__}")
st.write(
    """Elige tu fruta favorita para tu Smoothie"""
)

# Input para el nombre del smoothie
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Conexión a Snowflake
conn = st.connection("snowflake")
session = conn.session()

# Consulta la tabla de frutas
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))


pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

# Selección de ingredientes
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# Si hay ingredientes seleccionados
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(f'{fruit_chosen} Nutrition Information')
        # Llamada a la API
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + str(search_on))
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Armado del insert
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Botón para enviar la orden
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}! ✅')
