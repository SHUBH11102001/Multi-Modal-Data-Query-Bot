# Document-AI-Chatbot-using-Groq

AI Document Chatbot
Welcome to the AI Document Chatbot project! This application allows users to interact with various document formats, including Excel, SQL databases, and PDF files, using an AI-driven chatbot interface. The chatbot is built with Streamlit, LangChain, and the Groq API, providing an intuitive experience for data exploration and inquiry.

Table of Contents
Features
Technologies Used
Installation
Usage
How It Works
Contributing
License
Acknowledgments
Features
Excel Interaction: Upload an Excel file to query and analyze data interactively.
SQL Database Communication: Connect to SQLite or MySQL databases to ask questions and retrieve information.
PDF Document Q&A: Upload PDF files to engage in conversational retrieval-augmented generation (RAG) tasks, allowing users to ask questions based on the document's content.
Session Management: Maintain chat history across user sessions for more context-aware responses.
Error Handling: Provides user-friendly error messages for smoother interaction.
Technologies Used
Streamlit: For building the web application interface.
LangChain: For creating and managing AI interactions.
Groq API: For leveraging powerful language models (Llama3) for chat capabilities.
Pandas: For data manipulation and analysis of Excel files.
SQLAlchemy: For connecting to and interacting with SQL databases.
FAISS: For efficient vector storage and retrieval in PDF Q&A tasks.
SQLite/MySQL: For database interaction.
Installation
To set up the project locally, follow these steps:

Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/ai-document-chatbot.git
cd ai-document-chatbot
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Set your Groq API key:

Obtain your Groq API key and add it in the application via the sidebar input.
Run the Streamlit application:

bash
Copy code
streamlit run app.py
Open your web browser and navigate to http://localhost:8501 to access the chatbot interface.

Usage
Choose Document Type: On the left sidebar, select the document type you want to interact with (Excel, SQL, or PDF).

For Excel:

Upload your Excel file.
Ask questions about the data, and the chatbot will provide insights based on the content.
For SQL:

Select your database type (SQLite or MySQL) and provide connection details if using MySQL.
Ask questions related to your database, and the chatbot will retrieve the relevant information.
For PDF:

Upload one or more PDF files.
Ask questions regarding the PDF content, and the chatbot will use RAG techniques to provide answers based on the document's context.
How It Works
The chatbot utilizes the Groq API to process user queries and generate responses.
For Excel, data is loaded into a SQLite database for querying using SQL.
For SQL databases, the application connects to the specified database and processes user queries.
For PDFs, the application extracts text, splits it into manageable chunks, and uses embeddings for context-aware retrieval.
Contributing
Contributions are welcome! If you would like to contribute to this project, please follow these steps:

Fork the repository.
Create a new branch:
bash
Copy code
git checkout -b feature/YourFeature
Make your changes and commit them:
bash
Copy code
git commit -m 'Add some feature'
Push to the branch:
bash
Copy code
git push origin feature/YourFeature
Open a pull request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Thanks to the LangChain team for their amazing library that simplifies working with LLMs and building applications.
Special thanks to the Groq API for providing access to powerful language models.
