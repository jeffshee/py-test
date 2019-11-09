from torch.utils.data import DataLoader
from torchvision import datasets, transforms


def img_folder_dataloader(path, image_size=64, batch_size=128, normalize=True):
    trans = transforms.Compose([transforms.Resize(image_size),
                                transforms.CenterCrop(image_size),
                                transforms.ToTensor()])
    if normalize:
        trans = transforms.Compose([trans, transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    return DataLoader(datasets.ImageFolder(root=path, transform=trans), batch_size=batch_size, shuffle=True)


def mnist_dataloader(path='../data/', image_size=28, batch_size=64):
    trans = transforms.Compose([transforms.Resize(image_size),
                                transforms.ToTensor(),
                                transforms.Normalize((0.1307,), (0.3081,))])
    train_dataloader = DataLoader(datasets.MNIST(path, train=True, transform=trans), batch_size=batch_size,
                                  shuffle=True)
    val_dataloader = DataLoader(datasets.MNIST(path, train=False, transform=trans), batch_size=batch_size, shuffle=True)
    return train_dataloader, val_dataloader


loader = img_folder_dataloader('../data/tiny-imagenet-200/train', 64, 64, False)


# to quickly get 1 batch from dataloader
def get_sample(dataloader=loader):
    return next(iter(dataloader))
