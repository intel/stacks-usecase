"""Classic U-Net architecture."""

from tensorflow.keras import layers
from tensorflow.keras import Input, Model

# layers
Conv2D = layers.Conv2D
MaxPooling2D = layers.MaxPooling2D
Dropout = layers.Dropout
concatenate = layers.concatenate
Conv2DTranspose = layers.Conv2DTranspose


def downsample(N, input_layer, base_filters=64):
    """conv2d defaults."""
    return Conv2D(
        filters=base_filters * N,
        kernel_size=3,
        activation="relu",
        padding="same",
        kernel_initializer="he_normal",
    )(input_layer)


def upsample(N, input_layer, base_filters=64):
    """deconv defaults."""
    return Conv2DTranspose(
        filters=base_filters * N,
        kernel_size=3,
        strides=(2, 2),
        padding="same",
        kernel_initializer="he_normal",
    )(input_layer)


def unet_model(input_layer, base_filters, reg=False, test=True):
    """classic unet model."""
    # encoder block
    conv1 = downsample(1, input_layer)
    if not test:
        conv1 = downsample(1, conv1)
    pool1 = MaxPooling2D(2)(conv1)
    conv2 = downsample(2, pool1)
    if not test:
        conv2 = downsample(2, conv2)
    pool2 = MaxPooling2D(2)(conv2)
    conv3 = downsample(4, pool2)
    if not test:
        conv3 = downsample(4, conv3)
    pool3 = MaxPooling2D(2)(conv3)
    conv4 = downsample(8, pool3)
    if not test:
        conv4 = downsample(8, conv4)
    pool4 = MaxPooling2D(2)(conv4)

    # bottleneck
    convm = downsample(16, pool4)
    if not test:
        convm = downsample(16, convm)

    # decoder block
    deconv4 = upsample(8, convm)
    uconv4 = concatenate([deconv4, conv4])
    if reg:
        uconv4 = Dropout(0.5)(uconv4)
    uconv4 = downsample(8, uconv4)
    if not test:
        uconv4 = downsample(8, uconv4)
    deconv3 = upsample(4, uconv4)
    uconv3 = concatenate([deconv3, conv3])
    if reg:
        uconv3 = Dropout(0.5)(uconv3)
    uconv3 = downsample(4, uconv3)
    if not test:
        uconv3 = downsample(4, uconv3)
    deconv2 = upsample(2, uconv3)
    uconv2 = concatenate([deconv2, conv2])
    if reg:
        uconv2 = Dropout(0.5)(uconv2)
    uconv2 = downsample(2, uconv2)
    if not test:
        uconv2 = downsample(2, uconv2)
    deconv1 = upsample(1, uconv2)
    uconv1 = concatenate([deconv1, conv1])
    if reg:
        uconv1 = Dropout(0.5)(uconv1)
    uconv1 = downsample(1, uconv1)
    if not test:
        uconv1 = downsample(1, uconv1)

    output_layer = Conv2D(1, 1, padding="same", activation="sigmoid")(uconv1)

    return output_layer


def model():
    """generate Unet model and return instance of Model."""
    input_layer = Input((None, None, 1))
    output_layer = unet_model(input_layer, 64, test=False)
    return Model(inputs=[input_layer], outputs=[output_layer])


if __name__ == "__main__":
    m = model()
    for layers in m.layers:
        print(layers.output_shape)
