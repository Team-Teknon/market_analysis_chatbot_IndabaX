# market_analysis_chatbot_IndabaX - Hackathon Challenge#1
| <img src="https://github.com/tettey-exploits/market_analysis_chatbot_IndabaX/blob/main/Screenshot%20from%202024-07-13%2000-37-24.png?raw=true"> |
|:--:| 
| *A Prototype of A Data Analysis Tool for Market Performance* |



Here's a step-by-step procedure to get your chatbot-powered data analysis tool running on a local machine:

### Prerequisites
1. **Python Installed**: Ensure you have Python 3.7+ installed on your machine.
2. **Install Streamlit**: If you haven't already, install Streamlit using pip.
   ```sh
   pip install streamlit
   ```
<!-- 3. **Setup Google Cloud**: Please follow this tutorial: https://cloud.google.com/sdk/docs/install. When promted, the name of the project is `farmnets-try`. Select it among the list of options and proceed. -->

### Procedure

1. **Clone the Repository or Download the Code**:
   - If your project is hosted on a version control platform like GitHub, clone the repository.
     ```sh
     git clone https://github.com/tettey-exploits/market_analysis_chatbot_IndabaX.git
     ```
   - Alternatively, download the project files and extract them to your desired location.

2. **Navigate to the Project Directory**:
   - Open a terminal (or command prompt) and navigate to the directory containing your project files.
     ```sh
     cd path/to/your/project
     ```

3. **Create a Virtual Environment (Optional but Recommended)**:
   - Create a virtual environment to isolate your project dependencies.
     ```sh
     python -m venv myenv
     ```
   - Activate the virtual environment.
     - On Windows:
       ```sh
       myenv\Scripts\activate
       ```
     - On macOS/Linux:
       ```sh
       source myenv/bin/activate
       ```

4. **Install Required Dependencies**:
  - Install all required dependencies using pip. If you have a `requirements.txt` file, use it to install dependencies.
    ```sh
    pip install -r requirements.txt
    ```

5. **Set the environment variable**:
  - Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of the JSON file that contains your credentials. This variable applies only to your current shell session, so if you open a new session, set the variable again.
  Download the file at:
    ```sh
    https://drive.google.com/file/d/1cvBwGpmAljXn6A0urgpm--GEyBBGCZUt/view?usp=sharing
    ```
  - Linux or macOS:
    ```sh
    export GOOGLE_APPLICATION_CREDENTIALS="farmnets-try-46d4bbb04e15.json"
    ```
  - Windows:
    - For PowerShell:
    ```sh
    $env:GOOGLE_APPLICATION_CREDENTIALS="farmnets-try-46d4bbb04e15.json"
    ```
    - For command prompt:
    ```sh
    set GOOGLE_APPLICATION_CREDENTIALS=farmnets-try-46d4bbb04e15.json
    ```


6. **Run the Streamlit App**:
   - Start the Streamlit app using the `streamlit run` command followed by the name of your main Python script (e.g., `main.py`).
     ```sh
     streamlit run main.py
     ```

7. **Access the App in a Web Browser**:
   - Once the app is running, Streamlit will provide a local URL (typically `http://localhost:8501`). Open this URL in a web browser to access your chatbot-powered data analysis tool.

### Example Command Summary

```sh
# Step 1: Clone the repository
git clone https://github.com/tettey-exploits/market_analysis_chatbot_IndabaX.git

# Step 2: Navigate to the project directory
cd path/to/your/project

# Step 3: Create a virtual environment (optional)
python -m venv myenv
source myenv/bin/activate  # On macOS/Linux
# myenv\Scripts\activate  # On Windows

# Step 4: Install required dependencies
pip install -r requirements.txt

# Step 5: Set the environment variable
export GOOGLE_APPLICATION_CREDENTIALS="farmnets-try-1792e1acf49f.json"

# Step 6: Run the Streamlit app
streamlit run main.py
```
