# JSON to Excel Azure Function

## Introduction
This project provides an Azure Function that converts JSON input into an Excel (.xlsx) file.  
The function receives a HTTP request containing a filename and a list of JSON objects.  
After validating the input, the service converts the data into a Pandas DataFrame and generates an Excel file in memory, returning it as a Base64 string.
This function is part of a project where a Logic App sends the data to the function and receives the file back in Base64 format, which is then used to send an email afterward.

---

## Getting Started

### Prerequisites
- Python 3.9+
- Azure Functions Core Tools
- Dependencies listed in `requirements.txt`:
  - azure-functions
  - pandas
  - xlsxwriter

### How to Run Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start Azure Functions locally:
   ```bash
   func start
   ```
3. Send a POST request to:
   ```
   POST http://localhost:7071/api/JsontoExcel
   ```
4. Example request body:
   ```json
   {
     "fileName": "Hierarquia.xlsx",
     "data": [
       {"nome": "Maria", "idade": 28},
       {"nome": "José", "idade": 34}
     ]
   }
   ```

---

## Build and Test

### Build
The function is automatically built when deployed using Azure Functions pipelines.

### Testing
You can test locally using tools like:
- Postman
- Curl
- Thunder Client (VSCode)

Example test with curl:
```bash
curl -X POST http://localhost:7071/api/JsontoExcel   -H "Content-Type: application/json"   -d '{"fileName":"Hierarquia.xlsx","data":[{"a":1,"b":2},{"a":3,"b":4}]}'
```

The output will contain:
- The original file name  
- MIME type  
- Base64 representation of the generated Excel file  

---

## Contribute

Contributions are welcome!

1. Fork the repository  
2. Create a new branch (`feature/my-feature`)  
3. Commit your changes  
4. Open a pull request  

Please ensure:
- Clear and tested code  
- Documentation updates when necessary  
