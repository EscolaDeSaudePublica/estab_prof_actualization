import datetime
import psycopg2

import Estabelecimentos
import Profissionais
import cns_cpf_update

def main():
    print('Inicializando o processo de busca da competência atual')  

    def GetCompetencia():  #Pega a competência referente ao último mÊs
        today = datetime.date.today()
        month = today.month
        year = today.year
        
        competencia = 202210
        
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
            
        if month < 10:
            competencia = str(year) + '0' + str(month)
        else:
            competencia = str(year) + str(month)
            
        return(competencia)
    
    competencia = GetCompetencia() 
    
    def GetEstabLastCompetency():
        conn = psycopg2.connect(
            dbname = '',
            user = '',
            password = '',
            port = '',
            host = ''
            )
        cur = conn.cursor()
        cur.execute('SELECT competencia FROM cnesEstabelecimentos LIMIT 1')
        last_competencia = cur.fetchone()
        return last_competencia
    
    estab_last_competencia = GetEstabLastCompetency()[0]
    
    if competencia != estab_last_competencia:
        Estabelecimentos.main(competencia)

    def GetProfLastCompetency():
        conn = psycopg2.connect(
            dbname = '',
            user = '',
            password = '',
            port = '',
            host = ''
            )
        cur = conn.cursor()
        cur.execute('SELECT competencia FROM cnesProfissionais LIMIT 1')
        last_competencia = cur.fetchone()
        return last_competencia
    
    prof_last_competencia = GetProfLastCompetency()
    
    if competencia != prof_last_competencia:
        Profissionais.main(competencia)
        cns_cpf_update.main(competencia)
    
if __name__ == '__main__':
    main()