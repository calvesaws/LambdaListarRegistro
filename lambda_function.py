import sys
from Services import MensagemService
from Dominio import Evento

def lambda_handler(event, context):
  evento = Evento.Evento( event['pathParameters']['id'] , event['queryStringParameters']['senha'] );
 
  mensagem_obj = MensagemService.MensagemService().ListarMensagem(evento);


  return mensagem_obj



