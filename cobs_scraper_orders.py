#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import io
import pandas as pd
#import pymysql
#import mysql.connector
from sqlalchemy import create_engine
import re

import config.cobsDB as DB

login_url = 'https://tiendacobsandcogs.cl/user/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}

data = {
    'name': DB.cobsname,
    'pass': DB.cobspwd,
    'form_id': DB.cobsformid,
    'form_build_id': DB.cobsbuildid,
}

s = requests.Session()
try:
    response = s.post(login_url , data)
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

rx = re.compile(r'A\$\s*([0-9,.]+)')
dictionary = {'\$':'', '\.':''}

# SABANA con TODAS LAS ORDENES (CSV)
csvdata = s.get('https://tiendacobsandcogs.cl/admin/commerce/orders/orders.csv?combine=&order_number=&type=All&state=All&page&_format=csv').text
c=pd.read_csv(io.StringIO(csvdata),parse_dates=['Fecha'])
c['Total'] = c['Total'].replace(dictionary, regex = True)
c['Total pagado'] = c['Total pagado'].replace(dictionary, regex = True)
c['Total'] = pd.to_numeric(c['Total'],errors='coerce')
c['Total pagado'] = pd.to_numeric(c['Total pagado'],errors='coerce')
c.columns = ['order_number','order_date','order_user','order_email','order_state','order_paymentmethod','order_promotion','order_total','order_total_paid','order_items']
#print(c['order_number'])
c['order_number']=c['order_number'].fillna(0.0).astype(int)
#print(c['order_number'])


# SABANA con TODOS LOS MIEMBROS (CSV)
csvdata_forms = s.get('https://tiendacobsandcogs.cl/formularios/formularios.csv?page&_format=csv').text
d=pd.read_csv(io.StringIO(csvdata_forms))
d.columns = ['oi_producto','oi_nombre','oi_apaterno','oi_amaterno','oi_email','oi_rut','oi_order_number','oi_estado'] 
#print(c) # prints all the records and columns
#print(c['order_items']) # prints only single column and all the records

engine = create_engine("mysql+pymysql://"+DB.dbuser+":"+DB.dbpassword+"@"+DB.dbhost+"/"+DB.dbname)
mycon=engine.connect()
#mydb = mysql.connector.connect(
#        host=DB.dbhost,
#        user=DB.dbuser,
#        password=DB.dbpassword,
#        database=DB.dbname
#)
c.to_sql('order',con=mycon,if_exists='replace')
d.to_sql('order_item',con=mycon,if_exists='replace')
mycon.execute('call proc_insertDistinctPersons;')
#mydb.commit()
#mydb.close()


