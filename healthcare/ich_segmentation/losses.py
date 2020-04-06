"""custom losses for unet"""
import tensorflow as tf


def dice_coef(label, pred):
    smooth = 1
    sum = tf.keras.backend.sum
    label = tf.keras.backend.flatten(label)
    predi = tf.keras.backend.flatten(pred)
    intersect = sum(label * pred)
    return (2.0 * intersect + 1) / (sum(label) + sum(pred) + 1)


def dice_loss(label, pred):
    """dice loss."""
    return 1 - dice_coef(label, pred)


def bce_loss(label, pred):
    """wrapper for crossentropy loss."""
    return tf.keras.losses.binary_crossentropy(label, pred)


def dice_bce_loss(label, pred):
    """combined binary and dice loss."""
    return dice_loss(label, pred) + bce_loss(label, pred)
