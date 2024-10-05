# AI Document Chatbot

## Installation

To set up the project locally, follow these steps:

1. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your Groq API key**:
   - Obtain your Groq API key and add it in the application via the sidebar input.

3. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

4. Open your web browser and navigate to `http://localhost:8501` to access the chatbot interface.

## Usage

1. **Choose Document Type**: On the left sidebar, select the document type you want to interact with (Excel, SQL, or PDF).

   - **For Excel**:
     - Upload your Excel file.
     - Ask questions about the data, and the chatbot will provide insights based on the content.

   - **For SQL**:
     - Select your database type (SQLite or MySQL) and provide connection details if using MySQL.
     - Ask questions related to your database, and the chatbot will retrieve the relevant information.

   - **For PDF**:
     - Upload one or more PDF files.
     - Ask questions regarding the PDF content, and the chatbot will use RAG techniques to provide answers based on the document's context.

## How It Works

- The chatbot utilizes the Groq API to process user queries and generate responses.
- For Excel, data is loaded into a SQLite database for querying using SQL.
- For SQL databases, the application connects to the specified database and processes user queries.
- For PDFs, the application extracts text, splits it into manageable chunks, and uses embeddings for context-aware retrieval.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. **Fork the repository**.
2. **Create a new branch**:
   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Make your changes and commit them**:
   ```bash
   git commit -m 'Add some feature'
   ```

4. **Push to the branch**:
   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a pull request**.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the LangChain team for their amazing library that simplifies working with LLMs and building applications.
- Special thanks to the Groq API for providing access to powerful language models.
