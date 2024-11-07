# AI Document Chatbot

Welcome to the AI Document Chatbot project! This application allows users to interact with various document formats, including Excel, SQL databases, and PDF files, using an AI-driven chatbot interface. The chatbot is built with Streamlit, LangChain, and the Groq API, providing an intuitive experience for data exploration and inquiry.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **Excel Interaction**: Upload an Excel file to query and analyze data interactively.
- **SQL Database Communication**: Connect to SQLite or MySQL databases to ask questions and retrieve information.
- **PDF Document Q&A**: Upload PDF files to engage in conversational retrieval-augmented generation (RAG) tasks, allowing users to ask questions based on the document's content.
- **Session Management**: Maintain chat history across user sessions for more context-aware responses.
- **Error Handling**: Provides user-friendly error messages for smoother interaction.

## Technologies Used

- **Streamlit**: For building the web application interface.
- **LangChain**: For creating and managing AI interactions.
- **Groq API**: For leveraging powerful language models (Llama3) for chat capabilities.
- **Pandas**: For data manipulation and analysis of Excel files.
- **SQLAlchemy**: For connecting to and interacting with SQL databases.
- **FAISS**: For efficient vector storage and retrieval in PDF Q&A tasks.
- **SQLite/MySQL**: For database interaction.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-document-chatbot.git
   cd ai-document-chatbot

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Groq API key**:
   - Obtain your Groq API key and add it in the application via the sidebar input.

4. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```
   
5. Open your web browser and navigate to `http://localhost:8501` to access the chatbot interface.

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

Demo link--https://multi-modal-data-query-bot-kqeiaptzccxbdcgqxa29rt.streamlit.app/

## How It Works

- The chatbot utilizes the Groq API to process user queries and generate responses.
- For Excel, data is loaded into a SQLite database for querying using SQL. Excel should be well structured for this purpose.
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
   

## Acknowledgments

- Thanks to the LangChain team for their amazing library that simplifies working with LLMs and building applications.
- Special thanks to the Groq API for providing access to powerful language models.
