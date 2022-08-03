import string

class Mensagem():

  def __init__(self,id:string, mensagem: string, senha: string, tempo: int, visualizacoes_max: int, visualizacoes: int):
    
    self.id = id
    self.mensagem = mensagem
    self.senha = senha
    self.tempo = tempo      
    self.visualizacoes_max = visualizacoes_max
    self.visualizacoes = visualizacoes


    id: string
    mensagem: string
    senha: string
    tempo: int
    visualizacoes_max: int
    visualizacoes: int
    
