# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize your smoothie :balloon: {st.__version__}")
st.write(
  """Elige tu fruta favorita para tu Smoothie
  """
)
############
name_on_order = st.text_input("Name on Smoothie :")
st.write("The name on your Smoothie Will be:", name_on_order)

conn = st.connection("snowflake")
session = conn.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect (
	'Choose up to 5 ingredients:'
	, my_dataframe
    , max_selections= 5
)
if ingredients_list: #usando python si no es nullo la lista

    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    #solo es variable
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """',
            '""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop() #para la logica
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success(f'Your Smoothie is ordered,{name_on_order} ! ', icon="✅")


#new section
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
     

