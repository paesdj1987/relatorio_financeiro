#ldap_auth.py

from ldap3 import Server, Connection, ALL
import os

LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_BIND_DN = os.getenv("LDAP_BIND_DN")
LDAP_BIND_PASSWORD = os.getenv("LDAP_BIND_PASSWORD")
LDAP_BASE_DN = os.getenv("LDAP_BASE_DN")
LDAP_USER_SEARCH_FILTER = os.getenv("LDAP_USER_SEARCH_FILTER", "(sAMAccountName={username})")

def authenticate_and_authorize(username, password):
    # 0) Verifica variáveis
    if not all([LDAP_SERVER, LDAP_BIND_DN, LDAP_BIND_PASSWORD, LDAP_BASE_DN]):
        raise RuntimeError("Variáveis LDAP_* não configuradas corretamente.")

    server = Server(LDAP_SERVER, get_info=ALL)

    # 1) Bind com conta de serviço
    try:
        svc_conn = Connection(server, LDAP_BIND_DN, LDAP_BIND_PASSWORD, auto_bind=True)
    except Exception as e:
        print(f"Erro bind serviço: {e}")
        return False

    # 2) Procura o DN do usuário
    filter = LDAP_USER_SEARCH_FILTER.format(username=username)
    svc_conn.search(LDAP_BASE_DN, filter, attributes=["distinguishedName"])
    if not svc_conn.entries:
        svc_conn.unbind()
        return False  

    user_dn = svc_conn.entries[0].distinguishedName.value

    # 3) Tenta autenticar com a senha
    try:
        user_conn = Connection(server, user_dn, password, auto_bind=True)
        user_conn.unbind()
    except Exception as e:
        print(f"Erro bind usuário: {e}")
        svc_conn.unbind()
        return False

    svc_conn.unbind()
    return True
