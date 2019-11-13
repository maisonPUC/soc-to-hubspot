import csv
import requests
import json
import os
import re
from random import uniform, choice

HUBAPI_URL = "https://api.hubapi.com"
SOC_URL = "https://ws1.soc.com.br/WebSoc"
HEARDERS = {
    "Authorization": f"Bearer {os.environ['TOKEN']}",
    "Content-Type": "application/json",
}


def create_company(client):
    endpoint = f"{HUBAPI_URL}/companies/v2/companies/"
    data = json.dumps(
        {
            "properties": [
                {"name": "name", "value": client["NOME"]},
                {"name": "description", "value": client["RAZAOSOCIAL"]},
                {
                    "name": "address",
                    "value": f"{client['ENDERECO']} {client['NUMEROENDERECO']}",
                },
                {"name": "city", "value": client["CIDADE"]},
                {"name": "state", "value": client["UF"]},
                {"name": "zip", "value": client["CEP"]},
                {"name": "cnpj", "value": client["CNPJ"]},
                {"name": "inscricao", "value": client["INSCRICAO"]},
            ]
        }
    )

    r = requests.post(url=endpoint, data=data, headers=HEARDERS)

    print(r.text)
    return json.loads(r.text)


def create_deal(client, company, contact):
    endpoint = f"{HUBAPI_URL}/deals/v1/deal/"
    data = {
        "associations": {
            "associatedCompanyIds": [company["companyId"]],
            "associatedVids": [contact["vid"]],
        },
        "properties": [
            {"value": client["NOME"], "name": "dealname"},
            {
                "value": choice(
                    [
                        "1089243",
                        "appointmentscheduled",
                        "presentationscheduled",
                        "qualifiedtobuy",
                        "decisionmakerboughtin",
                    ]
                ),
                "name": "dealstage",
            },
            {"value": "default", "name": "pipeline"},
            {"value": 1409443200000, "name": "closedate"},
            {"value": uniform(5000.0, 100000.0), "name": "amount"},
            {"value": "newbusiness", "name": "dealtype"},
        ],
    }

    if "companyId" in company:
        data["associations"]["associatedCompanyIds"] = company["companyId"]
    if "vid" in contact:
        data["associations"]["associatedVids"] = contact["vid"]

    r = requests.post(url=endpoint, data=json.dumps(data), headers=HEARDERS)

    print(r.text)
    return json.loads(r.text)


def create_email(client):
    domains = [
        "hotmail.com",
        "gmail.com",
        "aol.com",
        "mail.com",
        "mail.kz",
        "yahoo.com",
    ]

    cleared = re.sub(r"[^a-zA-Z0-9]+", "", client["RAZAOSOCIAL"])
    first = cleared[:10].lower().replace(" ", "_")

    return f"{first}.{client['CODIGO']}@{choice(domains)}"


def create_contact(client):
    endpoint = f"{HUBAPI_URL}/contacts/v1/contact/"
    data = json.dumps(
        {
            "properties": [
                {"property": "email", "value": f"{create_email(client)}"},
                {"property": "firstname", "value": client["NOME"]},
                {"property": "lastname", "value": client["RAZAOSOCIAL"]},
                {
                    "property": "address",
                    "value": f"{client['ENDERECO']} {client['NUMEROENDERECO']}",
                },
                {"property": "city", "value": client["CIDADE"]},
                {"property": "state", "value": client["UF"]},
                {"property": "zip", "value": client["CEP"]},
            ]
        }
    )

    r = requests.post(url=endpoint, data=data, headers=HEARDERS)

    print(r.text)
    return json.loads(r.text)


def get_clients():
    parametro = {
        "empresa": "38380",
        "codigo": "703",
        "chave": os.environ["KEY"],
        "tipoSaida": "csv",
    }

    params = {"parametro": json.dumps(parametro)}
    endpoint = f"{SOC_URL}/exportadados"
    r = requests.get(url=endpoint, params=params)
    print(r.text)
    with open("clientes.csv", "w") as text_file:
        text_file.write(r.text)


def main():
    get_clients()
    with open("clientes.csv", encoding="latin-1") as csvfile:
        clients = csv.DictReader(csvfile, delimiter=";")
        for client in clients:
            contact = create_contact(client)
            company = create_company(client)
            create_deal(client, company, contact)


if __name__ == "__main__":
    main()

