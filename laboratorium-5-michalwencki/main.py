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
        return pd.read_sql('''select language.name, film.title, category.name
                            from language
                            join film on film.language_id=language.language_id
                            join film_category on film_category.film_id=film.film_id
                            join category on category.category_id=film_category.category_id 
                            where film_category.category_id=%(category)s
                            order by film.title asc, language.name asc''',params={'category':category}, con=connection)
    elif isinstance(category, str):
        return pd.read_sql('''select language.name, film.title, category.name
                            from language
                            join film on film.language_id=language.language_id
                            join film_category on film_category.film_id=film.film_id
                            join category on category.category_id=film_category.category_id 
                            where category.name LIKE %(category)s
                            order by film.title asc, language.name asc''',params={'category':category}, con=connection)
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
        return pd.read_sql('''select language.name, film.title, category.name
                            from language
                            join film on film.language_id=language.language_id
                            join film_category on film_category.film_id=film.film_id
                            join category on category.category_id=film_category.category_id 
                            where film_category.category_id=%(category)s
                            order by film.title asc, language.name asc''',params={'category':category}, con=connection)
    elif isinstance(category, str):
        return pd.read_sql('''select language.name, film.title, category.name
                            from language
                            join film on film.language_id=language.language_id
                            join film_category on film_category.film_id=film.film_id
                            join category on category.category_id=film_category.category_id 
                            where category.name ILIKE %(category)s
                            order by film.title asc, language.name asc''',params={'category':category}, con=connection)
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
        return pd.read_sql('''select actor.first_name, actor.last_name from actor
                            join film_actor on film_actor.actor_id = actor.actor_id
                            join film on film.film_id = film_actor.film_id
                            where film.title LIKE %(title)s
                            order by actor.last_name asc, actor.first_name asc''',params={'title':title}, con=connection)
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
    if isinstance(words,list):
        string = '|'.join(words)
        return pd.read_sql('''SELECT title
                            FROM film
                            WHERE title ~* %(title)s
                            ORDER BY title ASC''', params={'title':string}, con=connection)
    return None