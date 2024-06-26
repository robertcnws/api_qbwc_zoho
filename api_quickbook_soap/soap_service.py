from api_zoho.models import AppConfig
import logging
import uuid
import re

# Configura el logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def handle_authenticate(body):
    logger.debug("Handling authenticate request")
    app_config = AppConfig.objects.first()
    username = body['authenticate']['strUserName']
    password = body['authenticate']['strPassword']
    if username == app_config.qb_username and password == app_config.qb_password:
        ticket = str(uuid.uuid4())
        response_xml = f'''
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:qb="http://developer.intuit.com/">
            <soap:Header/>
            <soap:Body>
                <qb:authenticateResponse>
                    <qb:authenticateResult>
                        <qb:string>{ticket}</qb:string>
                        <qb:string></qb:string>
                    </qb:authenticateResult>
                </qb:authenticateResponse>
            </soap:Body>
        </soap:Envelope>
        '''
        return response_xml
    else:
        response_xml = '''
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:qb="http://developer.intuit.com/">
            <soap:Header/>
            <soap:Body>
                <qb:authenticateResponse>
                    <qb:authenticateResult>
                        <qb:string></qb:string>
                        <qb:string>nvu</qb:string>
                    </qb:authenticateResult>
                </qb:authenticateResponse>
            </soap:Body>
        </soap:Envelope>
        '''
        return response_xml

def generate_customer_query_response():
    data_xml = '''<CustomerQueryRq requestID="1">
                    <IncludeRetElement>ListID</IncludeRetElement>
                    <IncludeRetElement>FullName</IncludeRetElement>
                    <IncludeRetElement>FirstName</IncludeRetElement>
                    <IncludeRetElement>LastName</IncludeRetElement>
                    <IncludeRetElement>CompanyName</IncludeRetElement>
                    <IncludeRetElement>Phone</IncludeRetElement>
                    <IncludeRetElement>Email</IncludeRetElement>
                  </CustomerQueryRq>'''
    
    request_xml = f'''<?qbxml version="8.0"?>
                    <QBXML>
                        <QBXMLMsgsRq onError="stopOnError">
                            {data_xml}
                        </QBXMLMsgsRq>
                    </QBXML>'''
    
    response = f'''<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:qb="http://developer.intuit.com/">
                        <soap:Header/>
                        <soap:Body>
                            <qb:sendRequestXMLResponse>
                                <qb:sendRequestXMLResult><![CDATA[{request_xml}]]></qb:sendRequestXMLResult>
                            </qb:sendRequestXMLResponse>
                        </soap:Body>
                    </soap:Envelope>'''
    
    return response

def generate_item_query_response():
    data_xml = '''<ItemInventoryQueryRq requestID="2">
                    <IncludeRetElement>ListID</IncludeRetElement>
                    <IncludeRetElement>Name</IncludeRetElement>
                  </ItemInventoryQueryRq>'''
    
    request_xml = f'''<?qbxml version="8.0"?>
                    <QBXML>
                        <QBXMLMsgsRq onError="stopOnError">
                            {data_xml}
                        </QBXMLMsgsRq>
                    </QBXML>'''
    
    response = f'''<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:qb="http://developer.intuit.com/">
                        <soap:Header/>
                        <soap:Body>
                            <qb:sendRequestXMLResponse>
                                <qb:sendRequestXMLResult><![CDATA[{request_xml}]]></qb:sendRequestXMLResult>
                            </qb:sendRequestXMLResponse>
                        </soap:Body>
                    </soap:Envelope>'''
    
    return response



def generate_close_connection_response():
    logger.debug("Generating close connection response")
    response_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:qb="http://developer.intuit.com/">
        <soap:Header/>
        <soap:Body>
            <qb:closeConnectionResponse>
                <qb:closeConnectionResult>Connection closed successfully</qb:closeConnectionResult>
            </qb:closeConnectionResponse>
        </soap:Body>
    </soap:Envelope>'''
    return response_xml

def generate_unsupported_request_response():
    response_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                   xmlns:qb="http://developer.intuit.com/">
        <soap:Header/>
        <soap:Body>
            <qb:QBXML>
                <qb:QBXMLMsgsRs>
                    <qb:StatusMessage>Unsupported request</qb:StatusMessage>
                </qb:QBXMLMsgsRs>
            </qb:QBXML>
        </soap:Body>
    </soap:Envelope>'''
    return response_xml

def generate_error_response(error_message):
    response_xml = f'''<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                   xmlns:qb="http://developer.intuit.com/">
        <soap:Header/>
        <soap:Body>
            <qb:QBXML>
                <qb:QBXMLMsgsRs>
                    <qb:StatusMessage>Error processing request: {error_message}</qb:StatusMessage>
                </qb:QBXMLMsgsRs>
            </qb:QBXML>
        </soap:Body>
    </soap:Envelope>'''
    return response_xml

def generate_customer_add_response(zoho_final_customers):
    data_xml = ''
    for i in range(len(zoho_final_customers) - 20, len(zoho_final_customers)):
        data_xml += f'''<CustomerAddRq requestID="{i + 2}">
                            <CustomerAdd>
                                <Name>{zoho_final_customers[i].customer_name if zoho_final_customers[i].customer_name else "NO NAME"}</Name>
                                <CompanyName>{zoho_final_customers[i].company_name if zoho_final_customers[i].company_name else "NO COMPANY NAME"}</CompanyName>
                                <FirstName>{zoho_final_customers[i].first_name if zoho_final_customers[i].first_name else "NO FIRST NAME"}</FirstName>
                                <LastName>{zoho_final_customers[i].last_name if zoho_final_customers[i].last_name else "NO LAST NAME"}</LastName>
                                <Phone>{zoho_final_customers[i].phone if zoho_final_customers[i].phone else "NO PHONE"}</Phone>
                                <Email>{zoho_final_customers[i].email if zoho_final_customers[i].email else "not@email.com"}</Email>
                            </CustomerAdd>
                        </CustomerAddRq>'''
    
    request_xml = f'''<?qbxml version="8.0"?>
                      <QBXML>
                        <QBXMLMsgsRq onError="stopOnError">
                            {data_xml}
                        </QBXMLMsgsRq>
                      </QBXML>'''
    
    response = f'''<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:qb="http://developer.intuit.com/">
                        <soap:Header/>
                        <soap:Body>
                            <qb:sendRequestXMLResponse>
                                <qb:sendRequestXMLResult><![CDATA[{request_xml}]]></qb:sendRequestXMLResult>
                            </qb:sendRequestXMLResponse>
                        </soap:Body>
                    </soap:Envelope>'''
    return response

def generate_customer_add_response_new_version(zoho_final_customers):
    data_xml = '''<InvoiceAddRq requestID="2">
      <InvoiceAdd>
        <CustomerRef>
          <ListID>80000043-1718995153</ListID> <!-- Nombre completo del cliente -->
        </CustomerRef>
        <TxnDate>2024-06-21</TxnDate>
        <RefNumber>1234</RefNumber>
        <BillAddress>
          <Addr1>John Doe</Addr1>
          <Addr2>123 Main St.</Addr2>
          <City>Mountain View</City>
          <State>CA</State>
          <PostalCode>94043</PostalCode>
        </BillAddress>
        <PONumber>5678</PONumber>
        <TermsRef>
          <FullName>Net 30</FullName>
        </TermsRef>
        <InvoiceLineAdd>
          <ItemRef>
            <FullName>...Fourth John Doe Item</FullName>
          </ItemRef>
          <Desc>Product 1 Description</Desc>
          <Quantity>1</Quantity>
          <Rate>100.00</Rate>
        </InvoiceLineAdd>
        <InvoiceLineAdd>
          <ItemRef>
            <FullName>...Fourth John Doe Item</FullName>
          </ItemRef>
          <Desc>Product 2 Description</Desc>
          <Quantity>2</Quantity>
          <Rate>50.00</Rate>
        </InvoiceLineAdd>
      </InvoiceAdd>
    </InvoiceAddRq>'''
    
    request_xml = f'''<?qbxml version="8.0"?>
                    <QBXML>
                        <QBXMLMsgsRq onError="stopOnError">
                            {data_xml}
                        </QBXMLMsgsRq>
                    </QBXML>'''
    
    response = f'''<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:qb="http://developer.intuit.com/">
                        <soap:Header/>
                        <soap:Body>
                            <qb:sendRequestXMLResponse>
                                <qb:sendRequestXMLResult><![CDATA[{request_xml}]]></qb:sendRequestXMLResult>
                            </qb:sendRequestXMLResponse>
                        </soap:Body>
                    </soap:Envelope>'''
    return response


def generate_item_add_response(zoho_final_items):
    # data_xml = '''<ItemNonInventoryAddRq>
    #                 <ItemNonInventoryAdd>
    #                     <Name>***Sample Item</Name>
    #                     <SalesOrPurchase>
    #                         <Desc>Sample item description</Desc>
    #                         <Price>100.00</Price>
    #                         <AccountRef>
    #                             <FullName>Construction Income</FullName>
    #                         </AccountRef>
    #                     </SalesOrPurchase>
    #                 </ItemNonInventoryAdd>
    #             </ItemNonInventoryAddRq>'''
    data_xml = ''
    for i in range(len(zoho_final_items) - 3, len(zoho_final_items) - 2):
        replace_name = re.sub(r'[/()]', ' ', zoho_final_items[i].name).strip()
        replace_name = re.sub(r'\s+', ' ', replace_name)    
        data_xml += f'''<ItemNonInventoryAddRq requestID="{i + 2}">
                            <ItemNonInventoryAdd>
                                <Name>{replace_name if zoho_final_items[i].name else "NO NAME"}</Name>
                                <SalesOrPurchase>
                                    <Desc>SKU: {zoho_final_items[i].sku if zoho_final_items[i].sku else "NO DESCRIPTION"}</Desc>
                                    <Price>{zoho_final_items[i].rate if zoho_final_items[i].rate else "0.00"}</Price>
                                    <AccountRef>
                                        <FullName>Construction Income</FullName>
                                    </AccountRef>
                                </SalesOrPurchase>
                            </ItemNonInventoryAdd>
                        </ItemNonInventoryAddRq>
                    '''
    
    request_xml = f'''<?qbxml version="8.0"?>
                      <QBXML>
                        <QBXMLMsgsRq onError="stopOnError">
                            {data_xml}
                        </QBXMLMsgsRq>
                      </QBXML>'''
    
    response = f'''<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:qb="http://developer.intuit.com/">
                        <soap:Header/>
                        <soap:Body>
                            <qb:sendRequestXMLResponse>
                                <qb:sendRequestXMLResult><![CDATA[{request_xml}]]></qb:sendRequestXMLResult>
                            </qb:sendRequestXMLResponse>
                        </soap:Body>
                    </soap:Envelope>'''
    return response