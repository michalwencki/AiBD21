import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb', user='wbauer_adb', password='adb2020')

def film_in_category(category:Union[int,str])->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli categry jest int
        - name: jeżeli category jest str, dokładnie taki jak podana wartość
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)  dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    
    if isinstance(category, int):
        return pd.read_sql('select name, film.title, category.name, language_id from language where language_id in '
                           '(select film_id from film where film_id in '
                           '(select category_id from film_category where category_id in '
                           '(select category_id from category where category_id=@category)))'
                           'order by film.title asc, name asc', con=connection)
    elif isinstance(category, str):
        return pd.read_sql('select name, film.title, category.name, language_id from language where language_id in '
                           '(select film_id from film where film_id in '
                           '(select category_id from film_category where category_id in '
                           '(select category_id from category where name LIKE @category)))'
                           'order by film.title asc, name asc', con=connection)
    else:
        return None
    
def film_in_category_case_insensitive(category:Union[int,str])->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli category jest int
        - name: jeżeli category jest str
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)  dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(category, int):
        return pd.read_sql('select name, film.title, category.name, language_id from language where language_id in '
                           '(select film_id from film where film_id in '
                           '(select category_id from film_category where category_id in '
                           '(select category_id from category where category_id=@category)))'
                           'order by film.title asc, name asc', con=connection)
    elif isinstance(category, str):
        return pd.read_sql('select name, film.title, category.name, language_id from language where language_id in '
                           '(select film_id from film where film_id in '
                           '(select category_id from film_category where category_id in '
                           '(select category_id from category where name ILIKE @category)))'
                           'order by film.title asc, name asc', con=connection)
    else:
        return None
    
def film_cast(title:str)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o obsadę filmu o dokładnie zadanym tytule.
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |
    |0	|Greg       |Chaplin    | 
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    title (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(title, str):
        return pd.read_sql('select first_name, last_name, actor_id from actor where actor_id in '
                           '(select film_id from film_actor where film_id in '
                           '(select film_id from film where title LIKE @title)) '
                           'order by last_name asc, first_name asc', con=connection)
    return None
    

def film_title_case_insensitive(words:list) :
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuły filmów zawierających conajmniej jedno z podanych słów z listy words.
    Przykład wynikowej tabeli:
    |   |title              |
    |0	|Crystal Breaking 	| 
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.

    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    words(list): wartość minimalnej długości filmu
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    for i in range(0, len(words)-1):
        df=pd.read_sql('select title from film where title @words[i]', con=connection)
        if df is not None:
            df_end.append(df)



    return None