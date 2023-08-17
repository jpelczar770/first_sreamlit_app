import streamlit
import pandas 
import snowflake.connector
import requests
from urllib.error import URLError


streamlit.title('Healthy Diner')

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


def get_fruityvice_data(choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
  streamlit.header("Fruityvice Fruit Advice!") 
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit you'd like to get information about")
  else:
    back_from_func = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_func)
except URLError as e:
  streamlit.error()
  



streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()

if streamlit.button("Get Fruit Load List"):
  my_cnx = snowflake.connector.connect(snowflake.connector.connect(**streamlit.secrets["snowflake"]))
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)


# add_fruit = streamlit.text_input('What fruit would you like to add?')
# my_cur.execute("insert into fruit_load_list values ('" + add_fruit + "')")
# streamlit.write('Thanks for adding:  ', add_fruit)









