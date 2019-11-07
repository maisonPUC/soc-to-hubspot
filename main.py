import csv
import requests
import json
import os
from random import uniform, choice

BASE_URL = "https://api.hubapi.com"
HEARDERS = {
    "Authorization": f"Bearer {os.environ['TOKEN']}",
    "Content-Type": "application/json",
}


def create_company(client):
    endpoint = f"{BASE_URL}/companies/v2/companies/"
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
    endpoint = f"{BASE_URL}/deals/v1/deal/"
    data = json.dumps(
        {
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
    )

    r = requests.post(url=endpoint, data=data, headers=HEARDERS)

    print(r.text)
    return json.loads(r.text)


def create_contact(client):
    endpoint = f"{BASE_URL}/contacts/v1/contact/"
    data = json.dumps(
        {
            "properties": [
                {
                    "property": "email",
                    "value": f"{client['CODIGO']}{client['email']}",
                },
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


# def associate_contact_company(contact, company):
#     print("Success")
#
#
# def associate_company_deal(company, deal):
#     print("Success")


def main():
    with open("clientes.csv", encoding="latin-1") as csvfile:
        clients = csv.DictReader(csvfile, delimiter=";")
        for client in clients:
            contact = create_contact(client)
            company = create_company(client)
            deal = create_deal(client, company, contact)
            # associate_contact_company(contact, company)
            # associate_company_deal(company, deal)


if __name__ == "__main__":
    main()

