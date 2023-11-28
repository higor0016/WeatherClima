import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

#Função para pegar informações do clima da OpenWeatherMap API

def get_clima(cidade):
    chave_api="8bd3e2c23da06c858dd4b6a6e1de8f0d"
    url=f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={chave_api}"
    res= requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Erro, cidade não encontrada!")
        return None
    
    #Parse da resposta JSON para ter informações do clima
    clima = res.json()
    icone_id = clima['weather'][0]['icon']
    temperatura = clima['main']['temp'] - 273.15
    descricao = clima['weather'][0]['description']
    cidade = clima['name']
    pais = clima['sys']['country']

    #Pegar o icone da URL e retornar todas as informações do clima
    url_icone = f"https://openweathermap.org/img/wn/{icone_id}@2x.png"
    return (url_icone, temperatura, descricao, cidade, pais)
    


#Função para procurar o clima por cidade
def procura():
    cidade = entrada_cidade.get()
    resultado = get_clima(cidade)
    if resultado is None:
        return
    #Se a cidade n existir
    url_icone, temperatura, descricao, cidade, pais = resultado
    lbl_local.configure(text=f"{cidade}, {pais}")


    #Atualiza o icone
    image = Image.open(requests.get(url_icone, stream=True).raw)
    icone = ImageTk.PhotoImage(image)
    lbl_icone.configure(image=icone)
    lbl_icone.image = icone

    #Atualiza a temperatura e descrção
    lbl_temperatura.configure(text=f"Temperatura: {temperatura:.2f}°C")
    lbl_descricao_clima.configure(text=f"Descrição: {descricao}")

root = ttkbootstrap.Window(themename="morph")
root.title("App Clima")
root.geometry("400x400")

#Entry Widget -> para dar input com a cidade
entrada_cidade = ttkbootstrap.Entry(root,font="Helvetica, 18")
entrada_cidade.pack(pady=10)

#Button Widget -> para procurar informações meteorológicas
botao_procura = ttkbootstrap.Button(root, text="Search", command=procura, bootstyle="Cuidado")
botao_procura.pack(pady=10)

#label widget -> para mostrar a cidade
lbl_local = tk.Label(root, font="Helvetica, 25")
lbl_local.pack(pady=20)

#Para mostrar ícone do tempo
lbl_icone = tk.Label(root)
lbl_icone.pack()

#Label para mostrar temperatura
lbl_temperatura = tk.Label(root, font="Helvetica, 20")
lbl_temperatura.pack()

#Label para mostrar a descrição do clima
lbl_descricao_clima = tk.Label(root, font="Helvetica, 20")
lbl_descricao_clima.pack()

root.mainloop()