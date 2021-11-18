"""
Realiza o treinamento das marcas da mao
"""

import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


try:
    dados = pd.read_csv('marcas.csv', sep=';')
except FileNotFoundError:
    raise Exception(
        'Arquivo de marcas nao encontrado! Para criar o arquivo de marcas eh necessario rodar "coleta_dados.py"'
    )

# Colunas utilizadas como input para o treinamento
x_columns = ['0x', '0y', '0z', '1x', '1y', '1z', '2x', '2y', '2z', '3x', '3y', '3z',
             '4x', '4y', '4z', '5x', '5y', '5z', '6x', '6y', '6z', '7x', '7y', '7z',
             '8x', '8y', '8z', '9x', '9y', '9z', '10x', '10y', '10z', '11x', '11y',
             '11z', '12x', '12y', '12z', '13x', '13y', '13z', '14x', '14y', '14z',
             '15x', '15y', '15z', '16x', '16y', '16z', '17x', '17y', '17z', '18x',
             '18y', '18z', '19x', '19y', '19z', '20x', '20y', '20z']


# Conteudo com 666 foi considerado nao relevante ou com problema
com_conteudo = dados['target'] != 666
dados = dados[com_conteudo]
# Conteudo com -1 nao foi classificado
com_conteudo = dados['target'] != -1
dados = dados[com_conteudo]

dataset_train, dataset_test = train_test_split(dados, test_size=0.25, random_state=True)

x_train = dataset_train[x_columns]
y_train = dataset_train['target']

x_test = dataset_test[x_columns]
y_test = dataset_test['target']

y_train_dummies = pd.get_dummies(y_train).reindex(columns=range(5), fill_value=0)

tensor_x_train = torch.tensor(x_train.values, dtype=torch.float)
tensor_y_train = torch.tensor(y_train_dummies.values, dtype=torch.float)

tensor_x_test = torch.tensor(x_test.values, dtype=torch.float)

dataset = torch.utils.data.TensorDataset(tensor_x_train, tensor_y_train)
train_loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

model = torch.nn.Sequential(
        torch.nn.Linear(in_features=63, out_features=64),
        torch.nn.ReLU(),
        torch.nn.Linear(64, 5),
        torch.nn.Softmax(dim=1)
        )     
criterion = torch.nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters())

for epoch in range(300):
    running_loss = 0.       # Para armazenar o loss de cada epoca
    model.train()
    for data in train_loader:
        inputs, labels = data
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    
    model.eval()
    previsoes = model(tensor_x_test)
    top_p, top_class = previsoes.topk(k=1, dim=1)
    acc_test = accuracy_score(y_test, top_class)
    print('Epoca {}; Loss {}; Acc Test {}'.format(epoch, running_loss/len(train_loader), acc_test))
    
torch.save(model.state_dict(), '../model.pth')
