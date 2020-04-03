"""A unet model in tensorflow 2.0"""
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import Sequential as Seq
from tensorflow.keras import Model
from tensorflow.keras.applications import MobileNetV2


def encode(filters, pool=False, norm=True):
    """downsample sequential model."""
    net = Seq()
    net.add(
        layers.Conv2D(
            filters, 3, strides=2, padding="same", kernel_initializer="he_normal"
        )
    )
    if pool:
        net.add(layers.MaxPool2D(pool_size=(2, 2)))
    if norm:
        net.add(layers.BatchNormalization())
    net.add(layers.ReLU())
    return net


def decode(filters):
    """upsample sequential model."""
    net = Seq()
    net.add(
        layers.Conv2DTranspose(
            filters, 3, strides=2, padding="same", kernel_initializer="he_normal"
        )
    )
    net.add(layers.ReLU())
    return net


def encoder(pretrained=True):
    """unet encoder
       orig src : https://www.tensorflow.org/tutorials/images/segmentation
    """
    if pretrained:
        mobilenet = MobileNetV2(input_shape=[None, None, 1], include_top=False)
        layers = ["block_{}_expand_relu".format(x) for x in (1, 3, 6, 13)]
        layers.append("block_16_project")
        layers = [mobilenet.get_layer(layer).output for layer in layers]
        enc = Model(inputs=mobilenet.input, outputs=layers)
        enc.tranable = False
    else:
        n_filter = 64
        enc = [
            encode(n_filter * 1, pool=False, norm=False),
            encode(n_filter * 2, pool=False, norm=True),
            encode(n_filter * 4, pool=False, norm=True),
            encode(n_filter * 8, pool=False, norm=True),
            encode(n_filter * 16, pool=True, norm=True),
        ]
    return enc


def decoder():
    """unet decoder"""
    n_filter = 64
    return [
        decode(n_filter * 16),
        decode(n_filter * 8),
        decode(n_filter * 4),
        decode(n_filter * 2),
        decode(n_filter * 1),
    ]


def last_layer(out_channels=1):
    """last layer of u-net.
    """
    return layers.Conv2DTranspose(
        filters=out_channels,
        kernel_size=1,
        strides=2,
        padding="same",
        activation="sigmoid",
        kernel_initializer="he_normal",
    )


def unet_model(out_channels=1, pretrained=False):
    """A unet model with set of upsampling and downsampling layers."""
    input_layer = layers.Input(shape=[160, 160, 1])
    concat_layer = layers.Concatenate()
    skip_layers = []
    output_layer = last_layer(out_channels)

    x = input_layer
    # encode
    if pretrained:
        enc_layers = encoder(pretrained=True)
        skip_layers = enc_layers(x)
        x = skip_layers[-1]
    else:
        enc_layers = encoder(pretrained=False)
        for enc in enc_layers:
            x = enc(x)
            skip_layers.append(x)
    skip_layers = reversed(skip_layers[:-1])

    # decode
    for dec, skip in zip(decoder(), skip_layers):
        x = dec(x)
        concat_layer = layers.Concatenate()
        x = concat_layer([x, skip])
    x = output_layer(x)
    return Model(inputs=input_layer, outputs=x)


if __name__ == "__main__":
    out_channels = 1
    model = unet_model(out_channels, pretrained=False)
