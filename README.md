# estab_prof_actualization
Repositório de Scripts utilizados na atualização mensal dos estabelecimentos e profissionais de Saúde no Ceará

*FLUXOGRAMA DO PROCESSO DE ATUALIZAÇÃO DOS DADOS*
![fluxograma](https://user-images.githubusercontent.com/97004339/205938817-d1351824-d73b-4ea6-93f0-5a55af6a8746.png)

O processo de atualização mensal dos estabelecimentos e profissionais de saúde no Ceará é constituído de três etapas:

1 - Processo de raspagem, tratamento, normalização e injeção dos dados dos espaços é feito usando o arquivo estabelecimentos.py
    - É feita uma limpeza na base para selecionar somente dados de estabelecimentos que atuam no Ceará, bem como a remoção de dados desnecessários com a função ReadAndSaveData().
    - É feita uma normalização dos números de telefones dos estabelecimentos com a função PhoneTreatment().
    - É feita a injeção dos dados no banco PostgreSQL com a função Connect().
    
    
2 - Processo de raspagem e injeção de dados profissionais é feito em uma única etapa utilizando o arquivo profissionais.py

3 - Em cada competência surgem dados de novos profissionais e, nessa terceira etapa, é feita a atualização da tabela de relacionamento CNS-CPF de cada profissional através do arquivo cns_cpf_update.py.
    - Nessa etapa, o script acessa a tabela de profissionais atualizada no banco com a função Connect(), compara com os dados da competência atual e elimina os dados repetidos, restando somente os novos dados da referida competência (linhas 46-51).
    - Uma vez identificados os novos profisssionais, os dados são inseridos no banco de dados com a função Connect2()
    
OBS:

Para iniciar o processo de atualização o arquivo auto_download.py deve ser executado. Ele faz a leitura da competência e chama os arquivos acima quando necessário.

Para tornar esse processo automatizado é necessário usar um orquestrador para executá-lo diariamente, pois, uma vez que a competência é atuailzada o arquivo pára de executar.
