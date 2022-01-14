import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb', user='wbauer_adb', password='adb2020');

def film_in_category(category_id:int)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego id kategorii.
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(category_id, int):
        return pd.read_sql('''SELECT film.title, language.name, category.name
                        FROM film
                        JOIN film_category ON film_category.film_id = film.film_id
                        JOIN category ON category.category_id = film_category.category_id
                        JOIN language ON language.language_id = film.language_id
                        WHERE film_category.category_id = %(katid)s
                        ''', params={'katid':category_id}, con=connection)
    return None


def number_films_in_category(category_id:int)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów w zadanej kategori przez id kategorii.
    Przykład wynikowej tabeli:
    |   |category   |count|
    |0	|Action 	|64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(category_id, int):
        return pd.read_sql('''SELECT count(*), category.name
                        FROM film
                        JOIN film_category ON film_category.film_id = film.film_id
                        JOIN category ON category.category_id = film_category.category_id
                        WHERE film_category.category_id = %(katid)s
                        GROUP BY category.name
                        ''', params={'katid':category_id}, con=connection)
    return None

def number_film_by_length(min_length: Union[int,float] = 0, max_length: Union[int,float] = 1e6 ) :
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów o dla poszczegulnych długości pomiędzy wartościami min_length a max_length.
    Przykład wynikowej tabeli:
    |   |length     |count|
    |0	|46 	    |64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    min_length (int,float): wartość minimalnej długości filmu
    max_length (int,float): wartość maksymalnej długości filmu
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if (isinstance(min_length, (int,float)) and isinstance(max_length, (int,float)) and (min_length<=max_length)):
        return pd.read_sql('''SELECT length, count(*)
                            FROM film
                            WHERE length between %(min)s and %(max)s
                            GROUP BY length
                            ''', params={'min':min_length, 'max':max_length}, con=connection)
    return None

def client_from_city(city:str)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o listę klientów z zadanego miasta przez wartość city.
    Przykład wynikowej tabeli:
    |   |city	    |first_name	|last_name
    |0	|Athenai	|Linda	    |Williams
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    city (str): nazwa miaste dla którego mamy sporządzić listę klientów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(city, str):
        return pd.read_sql('''SELECT customer.first_name, customer.last_name
                            FROM customer
                            JOIN address ON address.address_id = customer.address_id
                            JOIN city ON city.city_id = address.city_id
                            WHERE city = %(name)s
                            GROUP BY customer.last_name, customer.first_name
                            ''', params={'name':city}, con=connection)
    return None

def avg_amount_by_length(length:Union[int,float])->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o średnią wartość wypożyczenia filmów dla zadanej długości length.
    Przykład wynikowej tabeli:
    |   |length |avg
    |0	|48	    |4.295389
    
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    length (int,float): długość filmu dla którego mamy pożyczyć średnią wartość wypożyczonych filmów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(length, (int,float)):
        return pd.read_sql('''SELECT length, avg(rental_rate)
                            FROM film
                            WHERE length = %(dl)s
                            GROUP BY length
                            ''', params={'dl':length}, con=connection)
    
    return None

def client_by_sum_length(sum_min:Union[int,float])->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o sumaryczny czas wypożyczonych filmów przez klientów powyżej zadanej wartości .
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |sum
    |0  |Brian	    |Wyman  	|1265
    
    Tabela wynikowa powinna być posortowane według sumy, imienia i nazwiska klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    sum_min (int,float): minimalna wartość sumy długości wypożyczonych filmów którą musi spełniać klient
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(sum_min, (int,float)):
        return pd.read_sql('''SELECT customer.first_name, customer.last_name, sum(film.length)
                            FROM customer
                            JOIN rental ON rental.customer_id = customer.customer_id
                            JOIN inventory ON inventory.inventory_id = rental.inventory_id
                            JOIN film ON inventory.film_id = film.film_id
                            GROUP BY customer.first_name, customer.last_name
                            HAVING sum(film.length) > %(wartosc)s
                            ORDER BY sum(film.length) DESC, customer.first_name, customer.last_name
                            ''', params={'wartosc':sum_min}, con=connection)
    return None  

def category_statistic_length(name:str)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o statystykę długości filmów w kategorii o zadanej nazwie.
    Przykład wynikowej tabeli:
    |   |category   |avg    |sum    |min    |max
    |0	|Action 	|111.60 |7143   |47 	|185
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    name (str): Nazwa kategorii dla której ma zostać wypisana statystyka
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(name, str):
        return pd.read_sql('''SELECT category.name, count(film.title), avg(film.length), sum(film.length), min(film.length), max(film.length)
                            FROM film
                            JOIN film_category ON film_category.film_id = film.film_id
                            JOIN category ON category.category_id = film_category.category_id
                            WHERE category.name = %(name)s
                            GROUP BY category.name
                            ''', params={'name':name}, con=connection)
    return None