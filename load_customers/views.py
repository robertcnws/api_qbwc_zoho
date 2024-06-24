from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import UploadFileForm
from .models import Customer
import pandas as pd
import chardet

def detect_encoding(file):
    # Detect encoding
    rawdata = file.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']
    file.seek(0)  # Reset file pointer
    return encoding

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        if not (file.name.endswith('.csv') or file.name.endswith('.CSV')):
            return HttpResponse('Error: El archivo no es un archivo CSV válido.')
        try:
            chunk_size = 1000

            chunks = pd.read_csv(file, chunksize=chunk_size, encoding=detect_encoding(file))

            for chunk in chunks:
                # Procesa cada chunk por separado
                print(chunk.head())
            # file = file.read().decode('latin-1').splitlines()
            # reader = csv.reader(file)
            # next(reader)
            # for row in reader:
            #     nuevo_cliente = Customer(
            #         active_status=row[1],
            #         customer=row[2],
            #         balance=row[3],
            #         balance_total=row[4],
            #         company=row[5],
            #         mr=row[6],
            #         first_name=row[7],
            #         mi=row[8],
            #         last_name=row[9],
            #         primary_contact=row[10],
            #         main_phone=row[11],
            #         fax=row[12],
            #         alt_phone=row[13],
            #         secondary_contact=row[14],
            #         job_title=row[15],
            #         main_email=row[16],
            #         bill_to_1=row[17],
            #         bill_to_2=row[18],
            #         bill_to_3=row[18],
            #         bill_to_4=row[20],
            #         bill_to_5=row[21],
            #         ship_to_1=row[22],
            #         ship_to_2=row[23],
            #         ship_to_3=row[24],
            #         ship_to_4=row[25],
            #         ship_to_5=row[26],
            #         customer_type=row[27],
            #         terms=row[28],
            #         rep=row[29],
            #         sales_tax_code=row[30],
            #         tax_item=row[31],
            #         resale_num=row[32],
            #         account_nro=row[33],
            #         credit_limit=row[34],
            #         job_status=row[35],
            #         job_type=row[36],
            #         job_description=row[37],
            #         start_date=row[38],
            #         projected=row[39],
            #         end_date=row[40],
            #     )
            #     nuevo_cliente.save()
            return HttpResponse('Archivo CSV cargado y procesado correctamente.')
        except Exception as e:
            return HttpResponse(f'Error al procesar el archivo CSV: {str(e)}')
    else:
        form = UploadFileForm()
    return render(request, 'load_customers/upload.html', {'form': form})


def list_customers(request):
    customers = Customer.objects.all()
    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'load_customers/list_customers.html', {'page_obj': page_obj})

def home(request):
    return render(request, 'load_customers/home.html')