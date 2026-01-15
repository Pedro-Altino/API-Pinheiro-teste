from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from db import get_db_connection, get_db_cursor

security = HTTPBasic(auto_error=True)

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    # Valida se credenciais foram fornecidas
    if not credentials or not credentials.username or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais ausentes",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    conn = get_db_connection()
    cursor = get_db_cursor(conn)
    
    try:
        cursor.execute(
            "SELECT id_usuario, nome, email, tipo_usuario FROM usuario WHERE email = %s AND senha = %s",
            (credentials.username, credentials.password)
        )
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Basic"},
            )
        
        return dict(user)
    finally:
        cursor.close()
        conn.close()

def require_auth(user: dict = Depends(verify_credentials)):
    return user

def require_admin(user: dict = Depends(verify_credentials)):
    if user.get("tipo_usuario") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas administradores podem acessar este recurso."
        )
    return user

def require_admin_for_user_ops(user: dict = Depends(verify_credentials)):
    """Operações de usuário são exclusivas para administradores"""
    if user.get("tipo_usuario") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas administradores podem gerenciar usuários."
        )
    return user

def check_ownership(user: dict, id_usuario_cadastrou: int):
    if user.get("tipo_usuario") != "admin" and user.get("id_usuario") != id_usuario_cadastrou:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Você só pode editar/deletar seus próprios registros."
        )
    return True
