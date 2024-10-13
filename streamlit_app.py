# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose upto five ingredients:",
    my_dataframe
)

ingredients = ''
for ingredient in ingredients_list:
    ingredients+=ingredient+' '

my_insert_stmt = 'insert into smoothies.public.ORDERS (ingredients) values (\''+ingredients+'\');'
time_to_insert = st.button('Submit Order')

if time_to_insert:
    if ingredients:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon='✅')
    else:
        st.write('Please select some ingredients!')
