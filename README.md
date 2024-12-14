# GeoMinLM: A Large Language Model for Geology and Mineral Survey in Yunnan Province

GeoMinLM is a powerful large language model tailored for geological and mineral exploration tasks in Yunnan Province. The model is specifically trained on geological and mineral survey data, and it aims to provide valuable insights into geological characteristics and mineral resources. GeoMinLM is designed for professionals involved in mineral resource evaluation, geological surveys, and related research.

### Features

- **Specialized Knowledge Base:** The model has been trained using a broad set of geological data from Yunnan Province, focusing on topics like mineral exploration and geological surveys.
- **User-Friendly Interface:** The model offers a command-line interface (CLI) for easy interaction and quick querying of geological and mineral-related data.

### How to Use GeoMinLM

1. **Download the Model:**
   You can download the pre-trained model from the following Google Drive link:  
   [Download GeoMinLM](...).

2. **Extract the Files:**
   Once you've downloaded the `GeoMinLM.tar.gz` file, extract it to your desired directory:

   ```bash
   tar -xzvf GeoMinLM.tar.gz
   ```

3. **Install Dependencies:**
   Ensure you have the necessary dependencies installed. You can install them via `pip` using the following command:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Model:**
   After extracting the files and installing the dependencies, navigate to the directory where `cli_demo.py` is located. To interact with the model, run the following command:

   ```bash
   python cli_demo.py
   ```

   This will start the command-line interface, where you can input geological queries related to Yunnan Province. The model will generate responses based on the trained data.

### Training Data Creation

If you're interested in creating your own training data or understanding the process of model training, please refer to the script `trople qa.py`. This script outlines the process for generating question-answer pairs and preparing data for training the model.

### License

This project is licensed under the MIT License.
