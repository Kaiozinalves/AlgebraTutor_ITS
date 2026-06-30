from sqlalchemy.orm import Session
from models import AlunoProgresso, Conceito, PreRequisito

def get_conceitos_desbloqueados(db: Session, aluno_id: int):
    # Pega todos os progressos do aluno
    progressos = db.query(AlunoProgresso).filter(AlunoProgresso.aluno_id == aluno_id).all()
    dominio_map = {p.conceito_id: p.dominio for p in progressos}
    
    # Pega todos os conceitos e seus pre-requisitos
    conceitos = db.query(Conceito).all()
    
    desbloqueados = []
    
    for c in conceitos:
        # Se domínio já for 1.0 (ou muito próximo, ex: >= 0.99), talvez não precisemos retornar como "ativo", 
        # mas por hora retornamos o estado de desbloqueio.
        
        pre_reqs = db.query(PreRequisito).filter(PreRequisito.conceito_id == c.id).all()
        
        pode_desbloquear = True
        for pr in pre_reqs:
            dom = dominio_map.get(pr.pre_requisito_id, 0.0)
            if dom < 0.70:
                pode_desbloquear = False
                break
                
        if pode_desbloquear:
            desbloqueados.append({
                "id": c.id,
                "nome": c.nome,
                "dominio": dominio_map.get(c.id, 0.0)
            })
            
    return desbloqueados

def aplicar_cascata_bloqueio(db: Session, aluno_id: int):
    # Roda em loop até estabilizar, garantindo que a queda do conceito 1 derrube o 2, que por sua vez derruba o 3.
    changed = True
    while changed:
        changed = False
        progressos = db.query(AlunoProgresso).filter(AlunoProgresso.aluno_id == aluno_id).all()
        dominio_map = {p.conceito_id: p for p in progressos}
        
        conceitos = db.query(Conceito).all()
        
        for c in conceitos:
            pre_reqs = db.query(PreRequisito).filter(PreRequisito.conceito_id == c.id).all()
            
            pode_desbloquear = True
            for pr in pre_reqs:
                if pr.pre_requisito_id in dominio_map:
                    if dominio_map[pr.pre_requisito_id].dominio < 0.70:
                        pode_desbloquear = False
                        break
                else:
                    pode_desbloquear = False
                    break
                    
            if not pode_desbloquear:
                # Se deveria estar bloqueado mas ainda tem pontos, reseta para 0
                if c.id in dominio_map and dominio_map[c.id].dominio > 0.0:
                    dominio_map[c.id].dominio = 0.0
                    changed = True
                    
    db.commit()

def atualizar_dominio(db: Session, aluno_id: int, conceito_id: int, acertou: bool, usou_dica: bool = False):
    progresso = db.query(AlunoProgresso).filter(
        AlunoProgresso.aluno_id == aluno_id,
        AlunoProgresso.conceito_id == conceito_id
    ).first()
    
    if not progresso:
        progresso = AlunoProgresso(aluno_id=aluno_id, conceito_id=conceito_id, dominio=0.0)
        db.add(progresso)
    
    if acertou:
        ganho = 0.10 if usou_dica else 0.20
        progresso.dominio = min(1.0, progresso.dominio + ganho)
        db.commit()
    else:
        progresso.dominio = max(0.0, progresso.dominio - 0.10)
        db.commit()
        aplicar_cascata_bloqueio(db, aluno_id)
        
    db.refresh(progresso)
    return progresso.dominio
