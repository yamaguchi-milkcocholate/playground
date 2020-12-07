import torch
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from network import Net


def train():
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.5, ), (0.5, ))]
    )
    trainset = torchvision.datasets.MNIST(
        root='./data',
        train=True,
        download=True,
        transform=transform
        )
    trainloader = torch.utils.data.DataLoader(
        trainset,
        batch_size=100,
        shuffle=True,
        num_workers=2
        )
    testset = torchvision.datasets.MNIST(
        root='./data',
        train=False,
        download=True,
        transform=transform
        )
    testloader = torch.utils.data.DataLoader(
        testset,
        batch_size=100,
        shuffle=False,
        num_workers=2
        )
    classes = tuple(np.linspace(0, 9, 10, dtype=np.uint8))

    net = Net()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(
        net.parameters(),
        lr=0.0005,
        momentum=0.99,
        nesterov=True
        )

    EPOCHS = 10
    for epoch in range(EPOCHS):
        running_loss = 0.0
        for i, (inputs, labels) in enumerate(trainloader, 0):
            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 100 == 99:
                print('[{:d}, {:5d}] loss: {:.3f}'.format(epoch + 1, i + 1, running_loss / 100))
                running_loss = 0.0
    print('Finished Training')
    correct = 0
    total = 0
    with torch.no_grad():
        for (images, labels) in testloader:
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    print('Accuracy: {:.2f} %%'.format(100 * float(correct/total)))

    torch.save(net.state_dict(), 'model.pth')


if __name__ == "__main__":
    train()
