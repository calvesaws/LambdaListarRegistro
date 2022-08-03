import sys
import boto3
sys.path.append('../')
from Dominio import Evento
from Dominio.Dto import Mensagem
 
class MensagemRepository():
    
    def ListarMensagem(evento: Evento):
       try:  
           cliente = boto3.resource('dynamodb')
           tabela = 'Dados'
    
           tabela = cliente.Table(tabela)
               
           resposta = tabela.get_item(
           Key={
               'Id' : evento.id,
           }
        )
       
           return resposta     

       except:
             raise Exception("Erro ao tentar salvar o documento no Dynamodb")

    def AtualizarVisualizacao(mensagem:Mensagem):
        
          cliente = boto3.resource('dynamodb')
          tabela = 'Dados'
    
          tabela = cliente.Table(tabela)
         
          tabela.update_item(
          Key={'Id': mensagem.id },
          UpdateExpression="set visualizacoes = :r",
          ExpressionAttributeValues={
         ':r': mensagem.visualizacoes,                                  
                      },
                  ReturnValues="UPDATED_NEW"
               )
