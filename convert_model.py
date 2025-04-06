import torch
import tensorflow as tf
import tensorflowjs as tfjs
from torchvision import models

# Load your PyTorch model
def load_pytorch_model(model_path):
    model = models.resnet18(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, 5)  # Adjust 5 to your number of classes
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

# Convert to TensorFlow
def convert_to_tfjs(pytorch_model, output_dir):
    # Create dummy input
    dummy_input = torch.randn(1, 3, 224, 224)
    
    # Export to ONNX
    torch.onnx.export(pytorch_model, dummy_input, "temp.onnx", 
                     input_names=["input"], output_names=["output"])
    
    # Convert ONNX to TensorFlow
    model = tf.keras.models.load_model("temp.onnx")
    
    # Save as TensorFlow.js format
    tfjs.converters.save_keras_model(model, output_dir)

if __name__ == "__main__":
    pytorch_model = load_pytorch_model("best_plant_classifier.pth")
    convert_to_tfjs(pytorch_model, "model")
    print("Model converted successfully to TensorFlow.js format")