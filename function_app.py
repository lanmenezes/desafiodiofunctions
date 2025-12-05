import base64
import io
import json
import logging

import azure.functions as func
import pandas as pd

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="JsontoExcel")
def Files_JsontoExcel(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

   
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Body inválido, envie um JSON."}),
            status_code=400,
            mimetype="application/json"
        )

    
    # 1. Validação da entrada
    
    file_name = body.get("fileName")
    data = body.get("data")

    if not file_name:
        return func.HttpResponse(
            json.dumps({"error": "O campo 'fileName' é obrigatório."}),
            status_code=400,
            mimetype="application/json"
        )

    if not data:
        return func.HttpResponse(
            json.dumps({"error": "O campo 'data' é obrigatório e deve conter uma lista JSON."}),
            status_code=400,
            mimetype="application/json"
        )

    accepted_files = ["Hierarquia.xlsx", "Qqcoisa.xlsx", "Desafio.xlsx"]
    
    if file_name not in accepted_files:
        return func.HttpResponse(
            json.dumps({"error": f"O nome do arquivo '{file_name}' não é aceito."}),
            status_code=400,
            mimetype="application/json"
        )
       
    # 2. Cria DataFrame a partir do JSON
   
    try:
        df = pd.DataFrame(data)
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": f"Não foi possível converter JSON para tabela: {str(e)}"}),
            status_code=400,
            mimetype="application/json"
        )

    
    # 3. Gera o Excel em memória
   
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Dados")

    excel_bytes = output.getvalue()
    excel_b64 = base64.b64encode(excel_bytes).decode("utf-8")

    
    # 4. Resposta com o arquivo
    
    response_body = {
        "fileName": file_name,  # usa o nome enviado
        "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "fileBase64": excel_b64
    }

    return func.HttpResponse(
        json.dumps(response_body),
        status_code=200,
        mimetype="application/json"
    )
