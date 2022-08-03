import sys
import datetime
from Dominio.Dto import Mensagem 
from Dominio import Evento
from Infraestructure.Repositories import MensagemRepository
sys.path.append('Services/modules')
import rsa 
import uuid
import json

class MensagemService():

      def descriptografar(self,mensagem):             
          
             with open('Services/Chave/private_key.pem', mode='rb') as private_file:
                chave = private_file.read()
                private_key = rsa.PrivateKey.load_pkcs1(chave,'PEM');
      
             mensagem_descript = rsa.decrypt(mensagem, private_key).decode() 
             
    
             return mensagem_descript
             
             
      def converte_json(self, body):
           return {
                   'statusCode': 200,
                     "headers": {
                      "Access-Control-Allow-Origin": "*",
                       "Access-Control-Allow-Header": "Content-Type",
                         "Access-Control-Allow-Methods": "OPTIONS,GET"
                         },
                        'body': json.dumps(body)
                    }
          

      def ListarMensagem(self, evento: Evento):

         mensagem_repository = MensagemRepository.MensagemRepository.ListarMensagem(evento)

          
         try:
             print(mensagem_repository['Item']['mensagem'].value)
         except:
           mensagem_erro = {
                "mensagem": "Mensagem não existe"
               }
           return self.converte_json(mensagem_erro)

         mensagem_cript = (mensagem_repository['Item']['mensagem'].value);
         senha_cript= (mensagem_repository['Item']['senha'].value);
         epoch_tempo = int(mensagem_repository['Item']['tempo']);
         
         tempo_atual = datetime.datetime.now()   ;  
         date_time = datetime.datetime.fromtimestamp( epoch_tempo )    ;  

         mensagem = Mensagem.Mensagem(evento.id, self.descriptografar(mensagem_cript), 
         self.descriptografar(senha_cript), str(date_time.strftime("%d-%m-%Y %H:%M:%S")),
         str(mensagem_repository['Item']['visualizacoes_max']), str(mensagem_repository['Item']['visualizacoes']));                    

         if tempo_atual > date_time:
           mensagem_expirada = {
                   "mensagem": "Mensagem foi expirada"
                      }
           return self.converte_json(mensagem_expirada)
    
         else:
          if mensagem.senha == evento.senha:
            mensagem.visualizacoes = int(mensagem.visualizacoes) + 1
            if mensagem.visualizacoes <= int(mensagem.visualizacoes_max):
            
              retorno_valido = {
                "mensagem" : mensagem.mensagem,
                "senha": mensagem.senha,
                "visualizacoes": mensagem.visualizacoes,
                "visualizacoes_max": mensagem.visualizacoes_max,
                "minutos" : mensagem.tempo
                 }
            
              MensagemRepository.MensagemRepository.AtualizarVisualizacao(mensagem)
             
              return self.converte_json(retorno_valido)
             
            else:
               
                  mensagem_limitada = {
                      "mensagem": "A mensagem passou do limite de visualizacao"
                       }
                  return self.converte_json(mensagem_limitada)
                  

          else:
           
            senha_erro = {
              "mensagem" : "Senha Incorreta",
          
              }
            return self.converte_json(senha_erro)

   