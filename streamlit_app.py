import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError 

streamlit.title("My parents new healthy Diner")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list =  my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick you poison: ", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized= pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
  
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice= streamlit.text_input("What fruit would you like information about?")
  #streamlit.write("The user entered",fruit_choice)
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)
    

except URLError as e:
  streamlit.error()

if streamlit.button("Get Fruit list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_cur = my_cnx.cursor()
  my_cur.execute("SELECT * from fruit_load_list")
  my_data_rows = my_cur.fetchall()
  my_cnx.close()
  streamlit.header("The fruit load list contains")
  streamlit.dataframe(my_data_rows)

#streamlit.stop()

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    query = "insert into fruit_load_list values ('"+new_fruit+"')"
    my_cur.execute(query)
    return "Thanks for adding "+new_fruit

add_my_fruit= streamlit.text_input("What fruit would you like to add?")
if streamlit.button("Add a Fruit to the list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_funtion = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_funtion)
  my_cnx.close()


