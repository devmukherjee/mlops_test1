import tensorflow as tf

def resize_image(image, label):
  """Resizes the input image to the desired size.

  Args:
    image: A tensor representing the image.
    label: The corresponding label for the image.

  Returns:
    A tuple containing the resized image and the original label.
  """
  resized_image = tf.image.resize(image, [224, 224]) # Replace [224, 224] with your desired size
  return resized_image, label

# Assuming 'image_dataset' is your tf.keras.data.Dataset
#resized_dataset = image_dataset.map(resize_image)