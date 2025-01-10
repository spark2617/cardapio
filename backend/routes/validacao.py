def validar_campos(dados, campos_obrigatorios):
    erros = []

    for campo, tipo in campos_obrigatorios.items():
        valor = dados.get(campo)

        # Verifica se o campo está ausente ou vazio
        if valor is None or (isinstance(valor, str) and valor.strip() == ""):
            erros.append(f"O campo '{campo}' é obrigatório e não pode estar vazio.")
        # Verifica se o tipo está correto
        elif not isinstance(valor, tipo):
            erros.append(f"O campo '{campo}' deve ser do tipo {tipo.__name__}.")

    return erros