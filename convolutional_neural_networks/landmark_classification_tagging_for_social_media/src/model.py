import torch
import torch.nn as nn


# define the CNN architecture
class MyModel(nn.Module):
    def __init__(self, num_classes: int = 1000, dropout: float = 0.7) -> None:
        super().__init__()

        # YOUR CODE HERE
        # Define a CNN architecture. Remember to use the variable num_classes
        # to size appropriately the output of your classifier, and if you use
        # the Dropout layer, use the variable "dropout" to indicate how much
        # to use (like nn.Dropout(p=dropout))

        self.model = nn.Sequential(
            # first conv+maxpool+relu
            nn.Conv2d(3, 32, 3, padding=1),
            nn.LeakyReLU(),
            nn.MaxPool2d(2, 2),
            
            # second conv+maxpool+relu
            nn.Conv2d(32, 64, 3, padding=1),
            nn.LeakyReLU(),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(64),
            
            # third conv+maxpool+relu
            nn.Conv2d(64, 128, 3, padding=1),
            nn.LeakyReLU(),
            nn.MaxPool2d(2, 2),
            
            # fourth conv+maxpool+relu
            nn.Conv2d(128, 256, 3, padding=1),
            nn.LeakyReLU(),
            nn.MaxPool2d(2, 2),  
            nn.BatchNorm2d(256),
            
            # fifth conv+maxpool+relu
            nn.Conv2d(256, 512, 3, padding=1),
            nn.LeakyReLU(),
            nn.MaxPool2d(2, 2),  
            nn.BatchNorm2d(512),    
            
            # flatten feature maps
            nn.Flatten(),
            
            nn.Dropout(dropout),
            
            # fully connected layers
            nn.Linear(7 * 7 * 512, 2048),
            nn.Linear(2048, 1024),
            nn.BatchNorm1d(1024),
            nn.Dropout(dropout),
            nn.Linear(1024, num_classes),
            nn.LeakyReLU(negative_slope=0.2),

        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # YOUR CODE HERE: process the input tensor through the
        # feature extractor, the pooling and the final linear
        # layers (if appropriate for the architecture chosen)
        return self.model(x)


######################################################################################
#                                     TESTS
######################################################################################
import pytest


@pytest.fixture(scope="session")
def data_loaders():
    from .data import get_data_loaders

    return get_data_loaders(batch_size=2)


def test_model_construction(data_loaders):

    model = MyModel(num_classes=23, dropout=0.3)

    dataiter = iter(data_loaders["train"])
    images, labels = dataiter.next()

    out = model(images)

    assert isinstance(
        out, torch.Tensor
    ), "The output of the .forward method should be a Tensor of size ([batch_size], [n_classes])"

    assert out.shape == torch.Size(
        [2, 23]
    ), f"Expected an output tensor of size (2, 23), got {out.shape}"
