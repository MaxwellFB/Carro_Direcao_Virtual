<p align="center">
  <img src="./img/Dirigindo.gif" />
</p>

# Carro com Direção Virtual
Este projeto possui o objetivo de simular a direção de um carro com apenas o movimento da mão. Para isso foi utilizado Mediapipe e aprendizado profundo (usado Pytorch) para capturar e processar os movimentos da mão e para o ambiente virtual do carro foi utilizado Microsoft Airsim e Unreal.

**Atenção:** Código configurado para utilizar webcam

## Instalações e preparações

### Pré-requisitos
Não irei descrever a instalação e configuração do ambiente da Microsoft Airsim e da Unreal. Este tutorial pode ser encontrado na página do Github da [Microsoft Airsim](https://github.com/microsoft/AirSim) e em sua [documentação](https://microsoft.github.io/AirSim/). A versão do Airsim utilizada foi a v1.6.0 — Windows.

Caso deseje utilizar Anaconda, disponibilizei meu environment, chamado “driveCar” e pode ser instalar usando o comando:

    conda env create -f environmentDriveCar.yml

#### Python e bibliotecas:
* Python v3.9.6
* Airsim v1.6.0
* Gym v0.21.0
* MediaPipe v0.8.7
* Numpy v1.21.4
* OpenCV v4.5.4
* Pandas v1.3.4
* Pynput v1.7.4
* Sklearn v1.0.1
* Torch v1.10.0

## Como rodar
Para um melhor funcionamento é conselhável realizar a própria coleta dos dados e treinamento da rede, descrito em "Coleta de dados e treinamento". Mas caso deseje utilizar a rede que disponibilizei, pode continuar a leitura em "Iniciando jogo".

### Coleta de dados e treinamento
A coleta de dados e a realização do treinamento de uma rede é aconselhável devido à baixa quantidade de dados e variedades utilizadas durante o treinamento da rede disponibilizada.

Todos os arquivos necessários para as próximas etapas estão dentro da **pasta "treinamento"**.

#### Coleta de dados
Para iniciar a coleta de dados, basta executar o arquivo "coleta_dados.py". Ao executar a webcam deve ser inicializada e acada 10 frames (pode ser alterado no código) a imagem será coletada e armazenada na pasta "frames", além das marcas da mão e algumas informações necessárias no arquivo "marcas.csv". Ou seja, realize os movimentos que desejar para controlar a direção do veículo (lembrando que quanto mais dados de cada comando melhor será o resultado). Não se preocupe com movimentos errados, será possível excluí-los na etapa seguinte.

#### Classificação dos dados
Com os frames coletados é possível executar o arquivo "classifica_dados.py". Irá mostrar o primeiro frame disponível na pasta "frames". Observando o frame, deve ser utilizado o teclado (parte numérica superior) para informar qual comando a imagem atual está realizando, logo após a classificação o próximo frame será carregado, até percorrer todos os frames. Os comandos disponíveis são:

Tecla   | Função
------- | ------- 
0       | Neutro
1       | Pouco direita
2       | Muito direita
3       | Pouco esquerda
4       | Muito esquerda
d       | Não utilizar arquivo para treinamento (Código: "666")
ESC     | Encerrar prematuramente

Todos os comandos serão atualizados na coluna "target" no arquivo "marcas.csv" criado anteriormente.

#### Treinamento
Com os dados devidamente coletados e classificados, basta realizar o treinamento. O treinamento está configurado para receber todas as 63 marcas da mão coletadas pelo Mediapipe e para ser uma rede pequena (e leve). Caso se sentir a vontade, fique livre para alterar.

Para realizar o treinamento basta executar o arquivo "treina_model.py". Ao finalizar o treinamento o arquivo "model.pth" será criado no diretório principal.

**OBS:** O arquivo "treina_model.ipynb" foi utilizado para testes durante o treinamento da rede e optei por deixar no repositório por achar o Jupyter Notebook mais fácil de realizar testes (outro detalhe, a versão do Airsim utilizada neste projeto utiliza algumas bibliotecas antigas que não são compatíveis com Jupyter Notebook). Todo código essencial para o treinamento foi colocado no arquivo "treina_model.py".

### Iniciando jogo
Primeiro o ambiente Unreal (ou Unity) e o plugin Airsim devem estar devidamente instalados e funcionando. E por fim, o ambiente (podendo ser dentro da engine ou compilado) deve estar em execução e o arquivo "model.pth" no diretório principal (no mesmo que o arquivo "main.py")

Com ambiente executando, basta executar o arquivo "main.py". Será feito a conexão com Airsim em execução, inicialização da webcam e das previsões do movimento da mão.

## Funcionalidades
Para controlar o volante do veículo é usado os movimentos com a mão esquerda simulando um volante.

Para os demais movimentos do veículo é utilizado o mouse:

Tecla                   | Função
----------------------- | ------- 
Botão esquerdo          | Acelerar
Botão direito           | Frear/ré
Botão do meio (scroll)  | Reiniciar ambiente

**Atenção:** Recomendo manter a mão levemente afastada da webcam, caso contrário o Mediapipe se perde. E cuidado onde o ponteiro do mouse irá estar quando estiver clicando para acelerar/frear (aconselho deixar dentro do ambiente ou na imagem da webcam).

## Autor
* **Maxwell F. Barbosa** - [MaxwellFB](https://github.com/MaxwellFB)
