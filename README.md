# ShelfStockScanner Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
3. [Project Overview](#project-overview)
   - [Components](#components)
   - [Workflow](#workflow)
4. [Usage](#usage)
   - [Configuration](#configuration)
   - [Running the Scanner](#running-the-scanner)
   - [Viewing Results](#viewing-results)
5. [Contributing](#contributing)
6. [License](#license)

---

## 1. Introduction <a name="introduction"></a>

ShelfStockScanner is a Python-based project that uses various computer vision techniques, Convolutional Neural Networks (CNNs), and external APIs to scan and catalog items on store shelves. This documentation provides detailed information on how to set up and use the ShelfStockScanner project.

## 2. Getting Started <a name="getting-started"></a>

### Prerequisites <a name="prerequisites"></a>

Before using ShelfStockScanner, ensure you have the following prerequisites installed:

- Python 3.6 or higher
- OpenCV (cv2) with Hough Lines, Non-Maximal Suppression, and Geometric Image Transformation support
- TensorFlow for CNN-based image recognition
- Google Image Search API credentials
- Google Cloud Platform API credentials for image storage and data cataloging

### Installation <a name="installation"></a>

1. Clone the ShelfStockScanner repository from GitHub:

   ```bash
   git clone https://github.com/yourusername/ShelfStockScanner.git
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## 3. Project Overview <a name="project-overview"></a>

### Components <a name="components"></a>

ShelfStockScanner consists of the following major components:

- **Region of Interest (ROI) Extraction:** Uses OpenCV for Hough Line detection, Non-Maximal Suppression, and Geometric Image Transformation to identify and isolate shelves and items.

- **Image Recognition:** Utilizes Convolutional Neural Networks (CNNs) for recognizing items on shelves.

- **Data Sources:** Relies on the Google Image Search API for obtaining images of items and the Google Cloud Platform API for image storage and data cataloging.

### Workflow <a name="workflow"></a>

1. **Image Acquisition:** The system captures images of store shelves.

2. **ROI Extraction:** OpenCV processes the images to identify and extract regions of interest (shelves and items).

3. **Image Recognition:** CNNs analyze the extracted ROIs to recognize the items on the shelves.

4. **Google Image Search API:** Images of recognized items are fetched from Google Image Search for reference.

5. **Google Cloud Platform API:** Recognized item data, along with associated images, is stored in Google Cloud for cataloging and analysis.

## 4. Usage <a name="usage"></a>

### Configuration <a name="configuration"></a>

Before running the ShelfStockScanner, you need to configure it by editing the `CONFIG.py` file. Here's an example configuration:

```
#GOOGLE IMAGE SEARCH KVPs
gis = {
    "api_key": "",
    "project_id": "",
}


#GOOGLE CLOUD PLATFORM KVPs
gcp = {
    "conn": "",
    "user": "",
    "password": "",
    "driver": "",
    "db": ""
}
```

Make sure to replace the placeholders with your actual API keys and paths.

### Running the Scanner <a name="running-the-scanner"></a>

To run the ShelfStockScanner, execute the following command:

```bash
python GCP_SIM.py
```

The scanner will capture images, process them, recognize items, and store the results in the specified output directory.

### Viewing Results <a name="viewing-results"></a>

You can view the results in the output directory specified in the configuration file. It will contain recognized items, associated images, and cataloging information.

## 5. Contributing <a name="contributing"></a>

Contributions to ShelfStockScanner are welcome! Feel free to fork the repository, make improvements, and submit pull requests. Be sure to follow the project's coding and documentation guidelines.

---

Thank you for using ShelfStockScanner! If you have any questions or encounter any issues, please refer to the GitHub repository's issue tracker or reach out to the project maintainers. Happy scanning!
