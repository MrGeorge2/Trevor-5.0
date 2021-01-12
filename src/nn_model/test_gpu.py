import tensorflow as tf


def test_tf_gpu():
    print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))