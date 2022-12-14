import pandas as pd
from tqdm import tqdm 
import psycopg2
from psycopg2 import Error

def main(comp):
    competencia = comp
    
    df = pd.read_csv(f'data/{competencia}.csv')
    df = df[['CNS','NOME']].drop_duplicates().astype(str)
    df.rename(columns = {'CNS':'cns','NOME':'nome'}, inplace = True)
    
    #h = host, db = database, u = user, p = port, pw = password
    def Connect(h, db, u, p, pw): 
        global df_prof
        print("Conectando ao Banco de Dados")
        
        try:
            conn = psycopg2.connect(
                host = h,
                database = db,
                user = u,
                port = p,
                password = pw
                )
            
            cur = conn.cursor()
            cur.execute("SELECT version();")
            rec = cur.fetchone()
            print("You are connected to - ", rec, "\n")
            
            sql = 'SELECT * FROM cns_prof_cpf'
            
            df_prof = pd.read_sql(sql, conn)
                   
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
        
        finally:
            if (conn):
                cur.close()
                conn.close()
                print("PostgreSQL connection is closed")
                
        return df_prof
        
    df_prof = Connect('','','','','')
    df_prof = df_prof[['cns','cpf']]
    
    dados_novos = pd.merge(df, df_prof, how= 'left', on= 'cns')
    dados_novos = dados_novos.loc[(dados_novos.cpf.isnull())]
    dados_novos = dados_novos.drop_duplicates()
    
    def Connect2(h, db, u, p, pw): 
        global dados_novos
        print("Conectando ao Banco de Dados")
        
        try:
            conn = psycopg2.connect(
                host = h,
                database = db,
                user = u,
                port = p,
                password = pw
                )
            
            cur = conn.cursor()
            cur.execute("SELECT version();")
            rec = cur.fetchone()
            print("You are connected to - ", rec, "\n")
            
            print("Inserting the Data en PostgreSQL table")
            
            for i in tqdm(dados_novos.index):
                sql = ''' INSERT INTO cns_prof_cpf
                (CNS, NOME, CPF)
                values ('%s','%s','%s') ''' % (dados_novos["cns"][i],
                dados_novos["nome"][i],dados_novos["cpf"][i])
        
                cur.execute(sql)
            
            conn.commit()
            print("Table was succesfullt updated")
                           
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
        
        finally:
            if (conn):
                cur.close()
                conn.close()
                print("PostgreSQL connection is closed")
                
    Connect2('','','','','')   
    
if __name__ == '__main__':
    main()

