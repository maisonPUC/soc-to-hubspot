import csv
import requests
import json
import os

BASE_URL = "https://api.hubapi.com"
HEARDERS = {
    "Authorization": f"Bearer {os.environ['TOKEN']}",
    "Content-Type": "application/json",
}


def create_company(cliente):
    endpoint = f"{BASE_URL}/companies/v2/companies"
    data = json.dumps(
        {
            "properties": [
                {"property": "name", "value": cliente["NOME"]},
                {"property": "description", "value": cliente["RAZAOSOCIAL"]},
                {
                    "property": "address",
                    "value": f"{cliente['ENDERECO']} {cliente['NUMEROENDERECO']}",
                },
                {"property": "city", "value": cliente["CIDADE"]},
                {"property": "state", "value": cliente["UF"]},
                {"property": "zip", "value": cliente["CEP"]},
            ]
        }
    )

    r = requests.post(url=endpoint, data=data, headers=HEARDERS)

    print(r.text)
    return json.loads(r.text)


def create_deal(cliente):
    return {}


def create_contact(cliente):
    endpoint = f"{BASE_URL}/contacts/v1/contact/"
    data = json.dumps(
        {
            "properties": [
                {
                    "property": "email",
                    "value": f"{cliente['CODIGO']}{cliente['email']}",
                },
                {"property": "firstname", "value": cliente["NOME"]},
                {"property": "lastname", "value": cliente["RAZAOSOCIAL"]},
                {
                    "property": "address",
                    "value": f"{cliente['ENDERECO']} {cliente['NUMEROENDERECO']}",
                },
                {"property": "city", "value": cliente["CIDADE"]},
                {"property": "state", "value": cliente["UF"]},
                {"property": "zip", "value": cliente["CEP"]},
            ]
        }
    )

    r = requests.post(url=endpoint, data=data, headers=HEARDERS)

    print(r.text)
    return json.loads(r.text)


def associate_contact_company(contact, company):
    print("Success")


def associate_company_deal(company, deal):
    print("Success")


def main():
    with open("clientes.csv", encoding="latin-1") as csvfile:
        clientes = csv.DictReader(csvfile, delimiter=";")
        for cliente in clientes:
            contact = create_contact(cliente)
            company = create_company(cliente)
            deal = create_deal(cliente)
            associate_contact_company(contact, company)
            associate_company_deal(company, deal)


if __name__ == "__main__":
    main()
