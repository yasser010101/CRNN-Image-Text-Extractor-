# CRNN-Image-Text-Extractor-
Python program that can extract texts from image or screen by lowering the noise in the image then processing it by CRNN.

This script acts as a customized OCR pipeline specifically tuned for reading low-resolution system displays or terminal screens. It begins by pre-processing the raw image to maximize legibility; it doubles the image size and isolates the green color channel to ensure the text stands out sharply against dark backgrounds.

The heart of the recognition process is the CRNN (Convolutional Recurrent Neural Network) architecture provided by EasyOCR. This model first uses a ResNet-based convolutional layer to extract visual features, then passes them through a Bi-LSTM layer to predict the sequence of characters. After the engine extracts the raw text, the script runs a "refinement" phase. This stage uses a custom dictionary to auto-correct visual hallucinations—like mistaking "11 Pro" for "14 Dro"—and employs regular expressions to fix broken IP addresses. By combining CRNN deep learning with logical post-processing, the code transforms messy screenshots into accurate data.
