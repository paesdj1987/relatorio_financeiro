# request.py

import os
from dotenv import load_dotenv
import pandas as pd
import oracledb
from sqlalchemy import create_engine
from typing import List

# Carrega variáveis de ambiente do .env
load_dotenv()

def connect():
    """
    Thick mode + TNS: carrega as DLLs do Instant Client e usa alias TNS.
    """
    instant_client = os.getenv("ORACLE_INSTANT_CLIENT_PATH")
    if not instant_client:
        raise RuntimeError("ORACLE_INSTANT_CLIENT_PATH não definido no .env")
    os.add_dll_directory(instant_client)

    tns_admin = os.getenv("TNS_ADMIN")
    if tns_admin:
        oracledb.init_oracle_client(lib_dir=instant_client, config_dir=tns_admin)
    else:
        oracledb.init_oracle_client(lib_dir=instant_client)

    user      = os.getenv("ORACLE_USER")
    password  = os.getenv("ORACLE_PASSWORD")
    tns_alias = os.getenv("ORACLE_TNS_ALIAS")

    if tns_alias:
        dsn = tns_alias
    else:
        host    = os.getenv("ORACLE_HOST")
        port    = os.getenv("ORACLE_PORT")
        service = os.getenv("ORACLE_SERVICE")
        dsn     = f"{host}:{port}/{service}"

    conn_str = f"oracle+oracledb://{user}:{password}@{dsn}"
    return create_engine(conn_str, pool_pre_ping=True)

# Cria engine global para reuse de pool
engine = connect()


def control_map_query(
    uo_list: List[str] | None = None,   
    dt_ini: str | None = None,          
    dt_fim: str | None = None
) -> pd.DataFrame:
    """
    Executa o SELECT de Mapa de Controle já filtrando por:
      • Cod Obra
      • intervalo de Data_da_SC (inclusive)
    """
    # SQL base
    base_sql = """
    SELECT
    /* ---------- SC / OBRA ---------- */
    "sc"."codigo"                               AS "Num_da_SC",
    "emp"."codigo"                              AS "Cod_Obra",
    TRUNC("sc"."data_registro")  AS "Data_da_SC",
    "sc"."data_necessidade"                     AS "Data_da_SC_Chegada_a_Obra",
	  "psc"."descricao"							              AS "Descricao_SC",
    /* --------- INSUMO / COTAÇÃO ---- */
    "coi"."codigo"                              AS "Cod_Insumo",
    "coi"."descricao"                           AS "Descricao_do_Insumo",
    /* ---------- NT ----------------- */
    "nt"."codigo"                               AS "Num_NT",
    "nt"."data_ap_final"                        AS "Data_Aprovacao_da_NT",
    /* ---------- PEDIDO ------------- */
    "pc"."codigo"                               AS "Num_do_PC",
    "pc"."data_aceite"                          AS "Data_Emissao_do_PC",
    "pcnf"."data_previsao_entrega"              AS "Previsao_de_Entrega",
    /* ---------- NOTA FISCAL -------- */
    "nf"."data_saida_entrada"                   AS "Data_da_NF",
    "nf"."numero"                               AS "Num_da_NF",
    "nf"."data_recebimento"                     AS "Data_Entrada_na_Obra",
    "nf"."data_pagamento"                       AS "Data_Vencimento",
    "nf_sts"."descricao"                        AS "Status_da_NF",
    /* ---------- FORNECEDOR SC --------- */
    "psf"."cnpj_cpf"                            AS "Fornecedor_CNPJ",
    "psf"."descricao"                           AS "Fornecedor",
    /* ---------- UA / CC ------------ */
    "ua"."codigo"                               AS "UA_Codigo",
    "ua"."descricao"                            AS "UA_Descricao",
    /* ---------- VALORES ------------ */
    "fc"."valor_unitario"                       AS "Valor_Unitario",
    "fc"."quantidade_solicitada"                AS "Qtd_Solicitada",
    "fc"."valor_total"                          AS "Valor_Total",
    /* Total entregue agregado — */
    "nfi_conc_agg"."total_entregue"             AS "Qtd_Entregue",
    /* Saldo sobre total entregue */
    ("fc"."quantidade_solicitada"
     - "nfi_conc_agg"."total_entregue")         AS "Saldo",
    "fc"."quantidade_anterior"                  AS "Qtd_Solicitada_Anterior",
    "fc"."valor_unitario_anterior"              AS "Valor_Unitario_Anterior",
    "fc"."valor_total_anterior"                 AS "Valor_Total_Anterior"
FROM OR_PCO."pco_sc"                           "sc"

    /* obra / empresa solicitante */
    LEFT JOIN OR_PGI."sca_organizacao_secao"     "emp" ON "sc"."idt_empresa_solicitante" = "emp"."idt"
      
    /* fornecedor da SC */
    LEFT JOIN OR_PCO."pco_sc_fornecedor"         "psf" ON "psf"."idt_sc" = "sc"."idt"
           
    /* Status da SC */
	  LEFT JOIN OR_PCO."pco_status_sc" 			       "psc" ON "sc"."idt_status_sc" = "psc"."idt"
	  		
    /* SC → insumo → empresa_insumo */
    INNER JOIN OR_PCO."pco_sc_insumo"            "sci" ON "sci"."idt_sc" = "sc"."idt"      
    INNER JOIN OR_PCO."pco_sc_insumo_empresa"    "scie" ON "scie"."idt_sci" = "sci"."idt"
      
    /* cotação do insumo */
    INNER JOIN OR_PFO."pfo_cotacao_insumo"       "coi" ON "coi"."idt_sc_insumo_empresa" = "scie"."idt"
      
    /* nota técnica */
    LEFT JOIN OR_PCO."pco_nt"                    "nt" ON "nt"."idt_sc" = "sc"."idt"
      
    /* pedido de compra */
    LEFT JOIN OR_PFO."pfo_pedido_compra"         "pc" ON "pc"."idt_sc" = "sc"."idt"
      
    /* nota fiscal */
    LEFT JOIN OR_PCO."pco_nf"                    "nf" ON "nf"."idt_sc_del" = "sc"."idt"

    /* item de NF */
    LEFT JOIN OR_PCO."pco_nf_insumo"             "nfi" ON "nfi"."idt_nf" = "nf"."idt"
      
    
    /*  1- junta conciliações + filtro por cotação em um único sub‐agregado */
    LEFT JOIN (
      SELECT
        "idt_nf_insumo",
        "idt_cotacao_insumo",
        SUM("qtd_recebida") AS "total_entregue"
      FROM OR_PCO."pco_nf_conc_insumo"
      GROUP BY
        "idt_nf_insumo",
        "idt_cotacao_insumo"
    )                                           "nfi_conc_agg"
      ON "nfi_conc_agg"."idt_nf_insumo"      = "nfi"."idt"
     AND "nfi_conc_agg"."idt_cotacao_insumo"  = "coi"."idt"

    /* status da NF */
    LEFT JOIN OR_PCO."pco_status_nf"             "nf_sts" ON "nf_sts"."idt" = "nf"."idt_status_nf"
      
    /* previsão de entrega (PC × NF) */
    LEFT JOIN OR_PFO."pfo_pedido_compra_nf"      "pcnf" ON "pcnf"."idt_pc" = "pc"."idt" AND "pcnf"."nf_numero" = "nf"."numero" AND "pcnf"."nf_serie" = "nf"."serie"
    
    /* fiscal/contábil da NT */
    LEFT JOIN OR_PCO."pco_nt_fiscal_contabil"    "fc" ON "fc"."idt_sc_insumo_empresa" = "scie"."idt" AND "fc"."idt_nt" = "nt"."idt"
  
    /* UA / centro de custo */
    LEFT JOIN OR_PGI."cge_centro_resultado"      "ua" ON "ua"."idt" = "fc"."idt_centro_custo"
WHERE
    "psc"."idt" IN ('4', '9', '10' ,'12', '13', '14', '17')
    AND (:dt_ini IS NULL OR TRUNC("sc"."data_registro") >= TO_DATE(:dt_ini,'YYYY-MM-DD'))
    AND (:dt_fim IS NULL OR TRUNC("sc"."data_registro") <= TO_DATE(:dt_fim,'YYYY-MM-DD'))
    AND "nf_sts"."descricao" IN ('Aprovado', 'Registra Parcelas')

    """
    # ---------- parâmetros ----------
    params: dict[str, str] = {
        "dt_ini": dt_ini,
        "dt_fim": dt_fim,
    }

    if uo_list:
        if len(uo_list) == 1:
            base_sql += '\n  AND "emp"."codigo" = :uo0'
            params["uo0"] = uo_list[0]
        else:
            placeholders = ", ".join(f":uo{i}" for i in range(len(uo_list)))
            base_sql += f'\n  AND "emp"."codigo" IN ({placeholders})'
            for i, val in enumerate(uo_list):
                params[f"uo{i}"] = val

    # Executa a query e retorna DataFrame filtrado
    return pd.read_sql(base_sql, con=engine, params=params)


