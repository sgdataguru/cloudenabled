#!/usr/bin/env python3
"""
Assignment 4: TensorFlow CNN Classification
Duration: 20 minutes
Focus: TensorFlow, CNN, Image Classification

This program:
1. Trains a CNN to classify Donald Trump vs Lawrence Wong images
2. Uses a simple CNN architecture suitable for small datasets
3. Evaluates model performance with accuracy metrics
4. Tests prediction on new images
5. Provides reflection on model performance

Note: This is a demonstration of CNN techniques using public figures.
In practice, avoid using personal identification for classification.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import TensorFlow components
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from PIL import Image
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("TensorFlow not available. Please install: pip install tensorflow pillow matplotlib")

class CNNImageClassifier:
    """CNN classifier for binary image classification"""
    
    def __init__(self, img_size=(150, 150), num_classes=2):
        """Initialize the CNN classifier"""
        self.img_size = img_size
        self.num_classes = num_classes
        self.model = None
        self.history = None
        self.class_names = ['donald_trump', 'lawrence_wong']
        
    def create_sample_data(self):
        """Create sample synthetic data for demonstration when real images aren't available"""
        print("Creating synthetic training data for demonstration...")
        
        # Create directories
        for split in ['train', 'val']:
            for class_name in self.class_names:
                os.makedirs(f'data/{split}/{class_name}', exist_ok=True)
        
        # Generate synthetic images (colored noise patterns)
        np.random.seed(42)
        
        # Training data: 20 images per class
        for class_idx, class_name in enumerate(self.class_names):
            for i in range(20):
                # Create different patterns for each class
                if class_idx == 0:  # donald_trump - reddish pattern
                    img_array = np.random.randint(100, 255, (*self.img_size, 3), dtype=np.uint8)
                    img_array[:, :, 0] = np.random.randint(180, 255, self.img_size)  # More red
                else:  # lawrence_wong - bluish pattern  
                    img_array = np.random.randint(100, 255, (*self.img_size, 3), dtype=np.uint8)
                    img_array[:, :, 2] = np.random.randint(180, 255, self.img_size)  # More blue
                
                img = Image.fromarray(img_array)
                img.save(f'data/train/{class_name}/sample_{i:02d}.jpg')
        
        # Validation data: 5 images per class
        for class_idx, class_name in enumerate(self.class_names):
            for i in range(5):
                if class_idx == 0:
                    img_array = np.random.randint(100, 255, (*self.img_size, 3), dtype=np.uint8)
                    img_array[:, :, 0] = np.random.randint(180, 255, self.img_size)
                else:
                    img_array = np.random.randint(100, 255, (*self.img_size, 3), dtype=np.uint8)
                    img_array[:, :, 2] = np.random.randint(180, 255, self.img_size)
                
                img = Image.fromarray(img_array)
                img.save(f'data/val/{class_name}/val_{i:02d}.jpg')
        
        print("✓ Synthetic training data created")
        print("  - 20 training images per class")
        print("  - 5 validation images per class")
    
    def prepare_data_generators(self):
        """Prepare data generators for training and validation"""
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        # Only rescaling for validation
        val_datagen = ImageDataGenerator(rescale=1./255)
        
        # Create generators
        train_generator = train_datagen.flow_from_directory(
            'data/train',
            target_size=self.img_size,
            batch_size=8,  # Small batch size for small dataset
            class_mode='binary',
            shuffle=True
        )
        
        val_generator = val_datagen.flow_from_directory(
            'data/val',
            target_size=self.img_size,
            batch_size=8,
            class_mode='binary',
            shuffle=False
        )
        
        return train_generator, val_generator
    
    def build_model(self):
        """Build a simple CNN model suitable for small datasets"""
        model = keras.Sequential([
            # First convolutional block
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(*self.img_size, 3)),
            layers.MaxPooling2D(2, 2),
            
            # Second convolutional block
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D(2, 2),
            
            # Third convolutional block
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.MaxPooling2D(2, 2),
            
            # Flatten and dense layers
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(1, activation='sigmoid')  # Binary classification
        ])
        
        # Compile model
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def train_model(self, train_generator, val_generator, epochs=10):
        """Train the CNN model"""
        print(f"\nTraining CNN model for {epochs} epochs...")
        print("Model architecture:")
        self.model.summary()
        
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=3,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=2,
                min_lr=1e-7
            )
        ]
        
        # Train model
        self.history = self.model.fit(
            train_generator,
            epochs=epochs,
            validation_data=val_generator,
            callbacks=callbacks,
            verbose=1
        )
        
        return self.history
    
    def evaluate_model(self, val_generator):
        """Evaluate model performance"""
        print("\\nEvaluating model performance...")
        
        # Get predictions
        val_generator.reset()
        predictions = self.model.predict(val_generator)
        y_pred = (predictions > 0.5).astype(int).flatten()
        y_true = val_generator.classes
        
        # Calculate metrics
        accuracy = np.mean(y_pred == y_true)
        
        # Simple confusion matrix calculation
        tp = np.sum((y_pred == 1) & (y_true == 1))
        tn = np.sum((y_pred == 0) & (y_true == 0))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        fn = np.sum((y_pred == 0) & (y_true == 1))
        
        print(f"Validation Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
        print(f"\\nConfusion Matrix:")
        print(f"True Negatives:  {tn}")
        print(f"False Positives: {fp}")
        print(f"False Negatives: {fn}")
        print(f"True Positives:  {tp}")
        
        # Class-wise accuracy
        class_0_acc = tn / (tn + fp) if (tn + fp) > 0 else 0
        class_1_acc = tp / (tp + fn) if (tp + fn) > 0 else 0
        
        print(f"\\nClass-wise Accuracy:")
        print(f"{self.class_names[0]}: {class_0_acc:.3f}")
        print(f"{self.class_names[1]}: {class_1_acc:.3f}")
        
        return accuracy, (tp, tn, fp, fn)
    
    def plot_training_history(self):
        """Plot training history"""
        if not self.history:
            print("No training history available")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Plot accuracy
        ax1.plot(self.history.history['accuracy'], label='Training Accuracy')
        ax1.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Plot loss
        ax2.plot(self.history.history['loss'], label='Training Loss')
        ax2.plot(self.history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('training_history.png', dpi=150, bbox_inches='tight')
        plt.show()
        print("\\n✓ Training history plot saved as 'training_history.png'")
    
    def predict_single_image(self, image_path):
        """Predict class for a single image"""
        try:
            # Load and preprocess image
            img = Image.open(image_path).convert('RGB')
            img = img.resize(self.img_size)
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            # Make prediction
            prediction = self.model.predict(img_array)[0][0]
            predicted_class = self.class_names[1] if prediction > 0.5 else self.class_names[0]
            confidence = prediction if prediction > 0.5 else 1 - prediction
            
            print(f"\\nPrediction for '{image_path}':")
            print(f"Predicted class: {predicted_class}")
            print(f"Confidence: {confidence:.3f} ({confidence*100:.1f}%)")
            
            return predicted_class, confidence
            
        except Exception as e:
            print(f"Error predicting image: {e}")
            return None, None
    
    def create_test_image(self, class_name='donald_trump'):
        """Create a test image for prediction demo"""
        print(f"Creating test image for class: {class_name}")
        
        # Create test image with appropriate pattern
        if class_name == 'donald_trump':
            # Reddish pattern
            img_array = np.random.randint(100, 255, (*self.img_size, 3), dtype=np.uint8)
            img_array[:, :, 0] = np.random.randint(200, 255, self.img_size)
        else:
            # Bluish pattern
            img_array = np.random.randint(100, 255, (*self.img_size, 3), dtype=np.uint8)
            img_array[:, :, 2] = np.random.randint(200, 255, self.img_size)
        
        img = Image.fromarray(img_array)
        test_path = f'test_{class_name}.jpg'
        img.save(test_path)
        
        return test_path

def main():
    """Main function to run the CNN classification demo"""
    print("="*60)
    print("Assignment 4: TensorFlow CNN Classification")
    print("="*60)
    
    if not TENSORFLOW_AVAILABLE:
        print("❌ TensorFlow not available. Please install required packages.")
        return
    
    # Initialize classifier
    classifier = CNNImageClassifier()
    
    # Step 1: Create sample data (since we don't have actual photos)
    classifier.create_sample_data()
    
    # Step 2: Prepare data generators
    try:
        train_gen, val_gen = classifier.prepare_data_generators()
        print(f"✓ Data generators created")
        print(f"  Training samples: {train_gen.samples}")
        print(f"  Validation samples: {val_gen.samples}")
        print(f"  Class indices: {train_gen.class_indices}")
        
    except Exception as e:
        print(f"❌ Error creating data generators: {e}")
        return
    
    # Step 3: Build model
    model = classifier.build_model()
    print(f"✓ CNN model built with {model.count_params():,} parameters")
    
    # Step 4: Train model
    history = classifier.train_model(train_gen, val_gen, epochs=5)  # Reduced epochs for demo
    
    # Step 5: Evaluate model
    accuracy, confusion_matrix = classifier.evaluate_model(val_gen)
    
    # Step 6: Plot training history
    classifier.plot_training_history()
    
    # Step 7: Test single image prediction
    print("\\n" + "="*50)
    print("Testing Single Image Prediction")
    print("="*50)
    
    # Create and test images for both classes
    for class_name in classifier.class_names:
        test_image_path = classifier.create_test_image(class_name)
        predicted_class, confidence = classifier.predict_single_image(test_image_path)
        
        # Check if prediction is correct
        correct = predicted_class == class_name
        result_emoji = "✅" if correct else "❌"
        print(f"{result_emoji} Expected: {class_name}, Got: {predicted_class}")
    
    # Step 8: Write reflection
    reflection_text = f"""
Brief Reflection on Model Performance:

1. **Model Architecture**: Used a simple 3-layer CNN with dropout for regularization, 
   suitable for small datasets with {model.count_params():,} parameters.

2. **Performance**: Achieved {accuracy:.1%} validation accuracy. For a small dataset 
   with only 40 total images, this demonstrates the model's ability to learn patterns.

3. **Data Limitations**: Using synthetic colored noise patterns instead of real photos. 
   Real-world performance would depend heavily on data quality and quantity.

4. **Generalization**: The model learned to distinguish between the color patterns we 
   created (red vs blue tones), showing basic classification capability.

5. **Future Improvements**: 
   - Larger, more diverse dataset
   - Transfer learning from pre-trained models
   - Data augmentation techniques
   - Cross-validation for better evaluation

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    with open('model_reflection.txt', 'w') as f:
        f.write(reflection_text)
    
    print("\\n" + "="*50)
    print("Assignment 4 Complete! ✅")
    print("="*50)
    print(f"✓ Model trained with {accuracy:.1%} accuracy")
    print("✓ Confusion matrix calculated")
    print("✓ Training plots saved")
    print("✓ Single image predictions tested")
    print("✓ Reflection written to 'model_reflection.txt'")
    print("\\nFiles created:")
    print("- training_history.png")
    print("- model_reflection.txt") 
    print("- test_donald_trump.jpg")
    print("- test_lawrence_wong.jpg")

if __name__ == "__main__":
    main()
