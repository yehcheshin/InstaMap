import pandas as pd
import random
import sqlalchemy
import psycopg2
import datetime
import sys

def read_file(path):
    return pd.read_csv(path)       

def read_db():
    try:
        query = 'SELECT * from stores_informations;'
        # Connect to postgres server on HH
        host_ = "your_host"
        database_ = "pl_project"
        user_ = "postgres"
        password_ = 'HHcs1932'
        
        # Build connection
        print('conneting...')
        connection = psycopg2.connect(host = host_, port = 5432, database = database_, user = user_, password = password_)
        cursor = connection.cursor()
        
        # execute query 
        
        #cursor.execute(build_original_table_query)
        df_dict = {'store' : [], 'Latitude' : [], 'Longitude' : []}

        cursor.execute(query)
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            df_dict['store'].append(row[0])
            df_dict['Longitude'].append(row[2])
            df_dict['Latitude'].append(row[3])

        df = pd.DataFrame(df_dict)
        df.to_csv('./utils_py/store_from_DB.csv', index=False)


    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            
def store_to_txt():
    sep = '@'
    result = ['NTHU' + sep + '24.7961' + sep + '120.9967' + '\n']
    df = read_file('store_from_DB.csv')
    choose = int(sys.argv[1])
    rand = random.sample(list(range(10000)), k=choose)
    count = 1
    for i, row in df.iterrows():
        if i in rand:
            store = row['store'].replace('\n', '_')
            Latitude = str(row['Latitude'])
            Longitude = str(row['Longitude'])
            if count < choose:
                result.append(store + sep + Latitude + sep + Longitude + '\n')
            else:
                result.append(store + sep + Latitude + sep + Longitude)
            choose += 1
    f = open('ig', 'w')
    f.writelines(result)
    f.close()
    
if __name__=='__main__':
    read_db()
#store_to_txt()
