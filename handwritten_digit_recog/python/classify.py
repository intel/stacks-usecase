import torch
import numpy as np
import matplotlib.pyplot as plt
from torchvision import datasets, transforms

from train import Net

# Load pre-trained model
model_path = "/workdir/models/mnist_cnn.pt"
device = torch.device("cpu")
model = Net().to(device)
model.load_state_dict(torch.load(model_path))

# Use a transform to normalize data (same as in training)
transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
)

# Load training data
kwargs = {"num_workers": 1, "pin_memory": True}
test_loader = datasets.MNIST("data", download=True, train=False, transform=transform)
data_loader = torch.utils.data.DataLoader(test_loader, batch_size=64, shuffle=True)


def img_show(img, ps, probab):
    ps = ps.data.numpy().squeeze()
    fig, (ax1, ax2) = plt.subplots(figsize=(5, 3), ncols=2)
    ax1.imshow(img.resize_(1, 28, 28).numpy().squeeze(), cmap="gray_r")
    ax1.axis("off")
    ax1.set_title("Random Test Image")
    ax1.text(
        5,
        30,
        "Predicted value: %s" % probab.index(max(probab)),
        fontsize=10,
        bbox={"facecolor": "cornsilk", "boxstyle": "round", "alpha": 0.5},
    )
    ax2.barh(np.arange(10), ps, color="gold")
    ax2.set_aspect(0.1)
    ax2.set_yticks(np.arange(10))
    ax2.set_yticklabels(np.arange(10))
    ax2.set_title("Probability Chart")
    ax2.set_xlim(0, 1.1)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Function for classifying random handwritten numbers from the MNIST dataset
def classify(imgshow=False):
    images, labels = next(iter(data_loader))
    img = images[0].view(1, 1, 28, 28)
    with torch.no_grad():
        logps = model(img)
    ps = torch.exp(logps)
    probab = list(ps.numpy()[0])
    if imgshow:
        img_show(img, ps, probab)
    return img, probab


if __name__ == "__main__":
    classify(imgshow=True)
