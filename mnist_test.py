import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from dataloader_test import mnist_dataloader
from torch.utils.tensorboard import SummaryWriter


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5, 1)
        self.conv2 = nn.Conv2d(20, 50, 5, 1)
        self.fc1 = nn.Linear(4 * 4 * 50, 500)
        self.fc2 = nn.Linear(500, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4 * 4 * 50)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)

    def forward_embedding(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4 * 4 * 50)
        x = F.relu(self.fc1(x))
        return x


def train(model, device, train_loader, optimizer, epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % 10 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                       100. * batch_idx / len(train_loader), loss.item()))


def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


def embedding(model, device, writer, epoch):
    model.eval()
    _, loader = mnist_dataloader(batch_size=1024)
    data, target = next(iter(loader))
    data, target = data.to(device), target.to(device)
    with torch.no_grad():
        em = model.forward_embedding(data)
        writer.add_embedding(em, target, data, epoch)


def main():
    # Setting
    use_save = False
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')

    # Hyper-parameter
    lr = 0.01
    momentum = 0.5
    epochs = 5

    model = Net().to(device)
    optimizer = optim.SGD(model.parameters(), lr, momentum)
    train_loader, test_loader = mnist_dataloader()
    writer = SummaryWriter('embedding')

    if use_save:
        model.load_state_dict(torch.load('mnist_cnn.pt'))
    else:
        for epoch in range(1, epochs + 1):
            train(model, device, train_loader, optimizer, epoch)
            test(model, device, test_loader)
            embedding(model, device, writer, epoch)
        torch.save(model.state_dict(), 'mnist_cnn.pt')
    writer.close()


if __name__ == '__main__':
    main()
