import uuid
from django.db import models
from apps.orders.models import Order
from apps.payments.models import Payments
from apps.shipments.models import Shipments, ShipmentTransactionLog
from novaposhta import NovaPoshtaApi
import response


def send_to_nova_poshta(arg_shipment_id):
    
    #instantiate objects    
    shipment=Shipment.objects.filter(id=arg_shipment_id).first()
    order=Order.objects.filter(id=shipment.order).first()
    user_name=UserProfile.object.filter(id=order.user).first()
    client=NovaPoshtaApi(api_key='')    
    
    #set-up sender variables
    sender=client.counterparty.get_counterparties(find_by_string="Тест")
    contact_sender=client.counterparty.get_counterparty_contact_person(sender)
    sender_city=client.address.search_settlements(city_name='Київ')
    sender_adress=client.adress.search_settlement_streets(street_name='Спортивна площа 1а', sender_city)

    #set-up recipient variables
    recipient_city=client.address.search_settlements(city_name=shipment.destination_city)
    recipient_adress=sender_adress=client.adress.search_settlement_streets(street_name='{} {}'.format(shipment.destination_adress_street, shipment.destination_adress_building), recipient_city)
    recipient=client.counterparty.get_counterparties(find_by_string='{} {}'.format(user_name.first_name, surname)
    
    request_payload={
        "apiKey": "",
        "modelName": "InternetDocument",
        "calledMethod": "save",
        "methodProperties":{
            "PayerType": "Sender",
            "PaymenentMethod": "Cash",
            "DateTime": shipment.shipment_date,
            "CargoType": "Cargo",
            "VolumeGeneral": "0.1",
            "Weight": "10",
            "ServiceType": "WarehouseDoor",
            "SeatsAmount": "1",
            "Description": "одяг",
            "Cost": "300",
            "CitySender": sender_city
            "Sender": sender
            "SenderAdress": sender_adress
            "ContactSender": contact_sender
            "SendersPhone": "380951244429"
            "CityRecipient": recipient_city
            "RecipientAdress": recipient_adress
            "ContactRecipient": recipient
            #"RecipientPhone": "" 
                    }
    
    }
    
    
    response_payload=client.send('IneternetDocument', 'save', request_payload)
    logline=ShipmentTransactionLog
    logline.shipment=Shipment.objects.filter(id=arg_shipment_id)
    logline.request_payload=request_payload
    logline.response_payload=response_payload
    
#TODO 1. parse response 2. ammend shipment status 3. save shipment tracking number to Shipment


