
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode




# ===========================================================================
# Identificar a Logomarca | Login e Senha
# ===========================================================================
imagem = "GRUPO_IMERGE.png"
st.set_page_config(page_icon="logo110.png", layout="wide",page_title="Grupo Imerge | Gerenciador Financeiro")
st.markdown(" # 🏢​ GERENCIADOR  ORÇAMENTO 📈​📉​📊​​ ")
# ===========================================================================




# ===========================================================================
# Importar DataFrame
# ===========================================================================


df = pd.read_excel('Relatório_FinanceiroAnalit_v0.1.xlsx',sheet_name='TRATADA')




dfo = pd.read_excel('orçamentoplanilha.xlsx')
dfo = dfo.drop('Orçamento do mês',axis= 1)
dfo['Orçado'] = dfo['Orçado'].astype('float')






# ===========================================================================
# Tratar DataFrame
# ===========================================================================
df.drop(0,inplace =True)
df.drop(1,inplace =True)
df.columns = ['Emissão',
 'Prorrogado',
 'Entrada',
 'Tipo Doc.',
 'Valor por Doc',
 'Retenções',
 'Descontos',
 'Baixas',
 'Saldo em Aberto',
 'Saldo Variação',
 'Tipo',
 'DataBaixa',
 'valorBaixa',
 'Classe',
 'Valor por Classe',
 'Centro De Custo',
 'Valor Por CC',
 'Projeto',
 'Valor por Projeto']
df["Prorrogado"] = pd.to_datetime(df["Prorrogado"], errors="coerce")
df["Emissão"] = pd.to_datetime(df["Emissão"], errors="coerce")
df["DataBaixa"] = pd.to_datetime(df["DataBaixa"], errors="coerce")
df["Entrada"] = pd.to_datetime(df["Entrada"], errors="coerce")

df.drop('Retenções',axis=1,inplace=True)
df.drop('Descontos',axis=1,inplace=True)

df['Valor Por CC']= df['Valor Por CC'].astype('float')
df['Baixas']= df['Baixas'].astype('float')
df['Valor por Projeto']= df['Valor por Projeto'].astype('float')
pm = df.loc[df['Tipo Doc.']=='PM']
df = df.loc[df['Tipo Doc.']!='PM']
# ===========================================================================
MATRIZ = {"CARLOS":"020386", "LUIZ":"112233", "LUIZ_AQUINO":"335566"}
COLUNAS = {"CARLOS":["Centro de Custo","col3"], "LUIZ":["col1"],}

FILTRO_101 = {"CARLOS":["Marketing","Comercial","Crédito e Repasse"], "LUIZ":["Obra"],}


LOGIN = st.sidebar.text_input("LOGIN")
SENHA = st.sidebar.text_input("SENHA", type="password") 
lista_ok = []
lista_resposta = []
for i in MATRIZ.keys():
    if LOGIN == i:
        lista_ok.append(i)
        lista_resposta.append("Login correto")
        POSICAO=lista_resposta[lista_resposta.index("Login correto")]
        POSICAO_=lista_ok[lista_ok.index(LOGIN)]
        if SENHA == MATRIZ[POSICAO_]:
            
            df["fil"] = 0
            try:
                try:
                    df.loc[df["Centro De Custo"] == FILTRO_101[LOGIN][0],"fil"] = 1
                    df.loc[df["Centro De Custo"] == FILTRO_101[LOGIN][1],"fil"] = 1
                    df.loc[df["Centro De Custo"] == FILTRO_101[LOGIN][2],"fil"] = 1

                    df = df.loc[df["fil"] == 1]
                except:
                    df.loc[df["Centro De Custo"] == FILTRO_101[LOGIN][0],"fil"] = 1
                    df.loc[df["Centro De Custo"] == FILTRO_101[LOGIN][1],"fil"] = 1
                    df = df.loc[df["fil"] == 1]
            except:
                df.loc[df["Centro De Custo"] == FILTRO_101[LOGIN][0],"fil"] = 1
                df = df.loc[df["fil"] == 1]

            # ===========================================================================
            # Orçado
            # ===========================================================================
            
            
            orcado = 350000
                        

            # ===========================================================================
            # Sidebar
            # ===========================================================================

            def conversor_moeda_brasil(my_value):
                a = '{:,.2f}'.format(float(my_value))
                b = a.replace(',','v')
                c = b.replace('.',',')
                return c.replace('v','.')

            st.sidebar.image(imagem, width=100, use_column_width=True)
            st.sidebar.markdown("Análise o Orçamento executado")
            with st.sidebar.expander("## FILTRO DE DATAS ##"):
                with st.form(key="proc77"):
                    start_date = st.date_input("Data de Inicio", value=pd.to_datetime("2022-05-01", format="%Y-%m-%d"))
                    end_date = st.date_input("Data Final", value=pd.to_datetime("today", format="%Y-%m-%d"))
                    start = start_date.strftime("%Y-%m-%d")
                    end = end_date.strftime("%Y-%m-%d")
                    LISTA_CENTRO_CUSTO = []
                    for i in df["Centro De Custo"].unique():
                        LISTA_CENTRO_CUSTO.append(i)
                    CENTRO_DE_CUSTO = st.selectbox("CENTRO DE CUSTO", options= LISTA_CENTRO_CUSTO)
                    BT_001 = st.form_submit_button(" 📄​ FILTRAR 🕟​ ")
                if BT_001:
                    try:
                        FILTRO_001 = df.loc[(df["Centro De Custo"] == CENTRO_DE_CUSTO) & (df['Prorrogado']>start) & (df['Prorrogado']<end)] 
                        FILTRO_002 = pm.loc[(pm["Centro De Custo"] == CENTRO_DE_CUSTO) & (pm['Prorrogado']>start) & (pm['Prorrogado']<end)] 
                        FILTRO_001_VALORES = FILTRO_001["Baixas"].sum()
                        aberto = FILTRO_001['Saldo em Aberto'].sum()
                        saldo = (FILTRO_001_VALORES + aberto) - orcado
                        prev = FILTRO_002.loc[FILTRO_002['Tipo Doc.']=='PM']
                        previsto = prev['Valor por Projeto'].sum()
                        
                    
                        DESCRICAO_001 = pd.DataFrame(FILTRO_001.groupby(["Projeto"])["Baixas"].sum()).reset_index()
                        DESCRICAO_002  = pd.DataFrame(FILTRO_001.groupby(["Projeto"])["Saldo em Aberto"].sum()).reset_index()
                        DESCRICAO_003 = pd.merge(DESCRICAO_001, DESCRICAO_002, on=["Projeto"], how='inner')
                        DESCRICAO_003.rename(columns = {'Baixas':'Pago', 'Saldo em Aberto':'Reconhecido'}, inplace = True)
                        #DESCRICAO_003=DESCRICAO_003.assign(Orçado=10000)
                        #DESCRICAO_003['Orçado'] = DESCRICAO_003['Orçado'].astype(float)
                        DESCRICAO_003['Pago'] = DESCRICAO_003['Pago'].astype(float)
                        DESCRICAO_003['Reconhecido'] = DESCRICAO_003['Reconhecido'].astype(float)

                        DESCRICAO_003 = DESCRICAO_003.reindex(columns = ['Projeto','Pago','Reconhecido','Saldo','Percentual_utilizado'])
                        DESCRICAO_003m = DESCRICAO_003.merge(dfo,on='Projeto')
                        DESCRICAO_003m['Saldo']= DESCRICAO_003m['Orçado'] - (DESCRICAO_003m['Pago'] + DESCRICAO_003m['Reconhecido'])


                        percentual = np.round((DESCRICAO_003m['Pago'] + DESCRICAO_003m['Reconhecido']) / DESCRICAO_003m['Orçado'],3)*100

                        DESCRICAO_003m['Percentual_utilizado'] = percentual
                        DESCRICAO_003m = DESCRICAO_003m.reindex(columns = ['Projeto','Orçado','Pago','Reconhecido','Saldo','Percentual_utilizado'])








                    except:
                        st.error(" ## FAVOR SELECIONAR OS FILTROS 🔴​ ")
                        FILTRO_001_VALORES = df 
                        DESCRICAO_003 = 0
                        DESCRICAO_003m = 0
                        

            # ===========================================================================
            # retorno
            # ===========================================================================       
                    
            col1, col2,col3,col4,col5,col6 = st.columns((4,4,4,4,4,4))

            with col1:
                a = st.empty()
            with col2:
                b = st.empty()
            with col3:
                c = st.empty()
            with col4:
                d = st.empty()
            with col5:
                f = st.empty()
            with col6:
                e = st.empty()
            try:
                with b.container():
                    valorgasto= st.metric('Pago:',value=f' R$ {conversor_moeda_brasil(FILTRO_001_VALORES)}')
                    with a.container():
                        st.metric('Orçado:',value=f'R${conversor_moeda_brasil(orcado)}')
                    with c.container():
                        valoresperado = st.metric('Reconhecido:',value=f' R$  {conversor_moeda_brasil(aberto)}')
                    variação_m= orcado - (FILTRO_001_VALORES + aberto)
                    with d.container():
                        st.metric('Saldo:',value=f' R$ {conversor_moeda_brasil(variação_m)}',delta=variação_m)
                    with e.container():
                        st.metric('Percentual Utilizado:',value=f'{np.round((FILTRO_001_VALORES+aberto)/orcado,3)*100}%')
                    with f.container():
                        st.metric('Previsto:',value=f'R${conversor_moeda_brasil(previsto)}') 
            except:
                st.warning(' FAVOR SELECIONAR OS FILTROS 🔴')
                with b.container():
                    valorgasto= st.metric('Pago:',value=f' R$ {conversor_moeda_brasil(0)}')
                    with a.container():
                        st.metric('Orçado:',value=f'R${conversor_moeda_brasil(0)}')
                    with c.container():
                        valoresperado = st.metric('Reconhecido:',value=f' R$  {conversor_moeda_brasil(0)}')
                    variação_m= 0
                    with d.container():
                        st.metric('Saldo:',value=f' R$ {conversor_moeda_brasil(0)}',delta=variação_m)
                    with e.container():
                        st.metric('Percentual Utilizado:',value=0)
                    with f.container():
                        st.metric('Previsto:',value=0) 
            try:
                with st.expander("Por Projeto"): 
                    arrumado = []
                    for i in DESCRICAO_003m['Pago']:
                        arrumado.append(F'R${conversor_moeda_brasil(i)}')
                    DESCRICAO_003m['Pago']=arrumado
                    arrumada = []
                    for i in DESCRICAO_003m['Reconhecido']:
                        arrumada.append(F'R${conversor_moeda_brasil(i)}')
                    DESCRICAO_003m['Reconhecido']=arrumada
                    arrumads = []
                    for i in DESCRICAO_003m['Saldo']:
                        arrumads.append(F'R${conversor_moeda_brasil(i)}')
                    DESCRICAO_003m['Saldo']=arrumads
                    per = []
                    for i in DESCRICAO_003m['Percentual_utilizado']:
                        per.append(f'{np.round(i,3)}%')
                    DESCRICAO_003m['Percentual_utilizado'] = per
                    
                    


                    #DESCRICAO_004 = pd.merge(DESCRICAO_003, dfo, on=["Projeto"], how='inner')
                    gb = GridOptionsBuilder.from_dataframe(DESCRICAO_003)
                    gb.configure_column(field='Orçado',editable=True)
                    #DESCRICAO_003['ProjetosTotais']=list
                    AgGrid(DESCRICAO_003m,editable=False)#.style.format(subset=["Orçado","Pago","Reconhecido","Saldo","percentual_utilizado"], formatter="{:.2f}"),Iterable=True)
            except:
                st.warning(' FAVOR SELECIONAR OS FILTROS 🔴')
                
            with st.expander('GERAL'):   
                try:
                    gb = GridOptionsBuilder.from_dataframe(df)
                    gb.configure_pagination(paginationAutoPageSize=50)
                    gb.configure_side_bar()
                    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=False)
                    gridOptions = gb.build()
                    FILTRO_001.fillna('-',inplace=True)
                    AgGrid(FILTRO_001, gridOptions=gridOptions, enable_enterprise_modules=True,)   
                except:
                    st.warning(' FAVOR SELECIONAR OS FILTROS 🔴')
                #DESCRICAO_008 = pd.merge(DESCRICAO_003, dfo, on=["Projeto"], how='inner')
                
                
