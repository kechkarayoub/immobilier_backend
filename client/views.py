# -*- coding: utf-8 -*-
from .models import Client
from admin_data.models import AdminData
from backend.utils import get_list_social_links_images, send_email
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from settings_db.models import SettingsDb
from newsletter.models import Newsletter
from backend.utils import is_email_valid
import datetime
from django.views.decorators.csrf import csrf_exempt
import xlrd


@api_view(['POST'])
# #@csrf_exempt
def import_clients(request):
    """
    Import client list from excel file.
    """
    response = {
        "message": "Erreur serveur"
    }
    row_header = 0
    col_first_name = 2
    col_last_name = 3
    col_email = 5
    col_address = 7
    col_apartment = 8
    col_type = 9
    if request.method == 'POST':
        response.update({"success": True})
        if request.FILES.get("file"):
            file = request.FILES.get("file")
            document = xlrd.open_workbook(file_contents=file.read())
            issues = {}
            clients_created = 0
            clients_updated = 0
            issues_exist = False
            message = ""
            for sheet_name in document.sheet_names():
                sheet_issues = []
                worksheet = document.sheet_by_name(sheet_name)
                if worksheet.nrows > 0:
                    structured_file = True
                    if not str(worksheet.row(row_header)[col_first_name].value).strip().lower() in ["prenom", "prénom", "nom 1"]:
                        structured_file = False
                    if not str(worksheet.row(row_header)[col_last_name].value).strip().lower() in ["nom", "nom 2"]:
                        structured_file = False
                    if not str(worksheet.row(row_header)[col_email].value).strip().lower() in ["email"]:
                        structured_file = False
                    if not str(worksheet.row(row_header)[col_address].value).strip().lower() in ["adresse"]:
                        structured_file = False
                    if not str(worksheet.row(row_header)[col_apartment].value).strip().lower() in ["apt", "appartement"]:
                        structured_file = False
                    if not structured_file:
                        message = "Importation n'est pas terminée."
                        sheet_issues.append(
                            "Le fichier n'est pas valide ou n'est pas bien structuré dans la feille: {}.".format(sheet_name)
                        )
                        issues_exist = True
                    else:
                        message = "Importation terminée."
                        idx = row_header + 1
                        while idx < worksheet.nrows:
                            client_row = worksheet.row(idx)
                            email = client_row[col_email].value.strip()
                            first_name = client_row[col_first_name].value.strip()
                            last_name = client_row[col_last_name].value.strip()
                            if email and first_name and last_name:
                                if is_email_valid(email):
                                    address = client_row[col_address].value.strip() or ""
                                    apartment = str(int(client_row[col_apartment].value)).strip() if\
                                        client_row[col_apartment].value else ""
                                    try:
                                        type = client_row[col_type].value.lower().strip() or ""
                                    except:
                                        type = ""
                                    type = type if type in ["locataire", "vendeur", "achteur"] else ""
                                    if not Client.objects.filter(email=email).exists():
                                        Client.objects.create(
                                            email=email, first_name=first_name, last_name=last_name,
                                            address=address, apartment=apartment, type=type
                                        )
                                        clients_created += 1
                                    else:
                                        Client.objects.filter(email=email).update(
                                            is_active=True, first_name=first_name, last_name=last_name,
                                            address=address, apartment=apartment, type=type
                                        )
                                        clients_updated += 1

                                    if type != "locataire":
                                        if not Newsletter.objects.filter(email=email).exists():
                                            Newsletter.objects.create(
                                                email=email,
                                                first_name=first_name,
                                                last_name=last_name,
                                                type=type
                                            )
                                    else:
                                        Newsletter.objects.filter(email=email).update(is_active=False)
                                else:
                                    sheet_issues.append(
                                        "Dans la ligne {}; Nom, Prénom et Email sont obligatoires".format(idx)
                                    )
                                issues_exist = True
                            elif email or first_name or last_name:
                                sheet_issues.append("Dans la ligne {}; l'adresse email est invalide!".format(idx))
                                issues_exist = True
                            idx += 1
                    issues[sheet_name] = sheet_issues
            response.update({
                "message": message,
                "clients_created": clients_created,
                "clients_updated": clients_updated,
                "issues": issues if issues_exist else None,
            })
        return JsonResponse(response, status=status.HTTP_200_OK)
    return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)


