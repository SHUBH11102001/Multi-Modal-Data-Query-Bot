import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
import tempfile
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables.history import RunnableWithMessageHistory
from pathlib import Path
import sqlite3
from langchain.callbacks import StreamlitCallbackHandler

st.set_page_config(page_title="AI Document Chatbot", page_icon="🤖")


st.title("🤖 AI Document Chatbot")


api_key = st.sidebar.text_input(label="Groq API Key", type="password")


doc_type = st.sidebar.selectbox("Choose the document type you want to interact with:", ["Excel", "SQL", "PDF"])

if not api_key:
    st.info("Please enter your Groq API Key.")
else:
    
    llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

    
    if f"{doc_type}_messages" not in st.session_state:
        st.session_state[f"{doc_type}_messages"] = [{"role": "assistant", "content": "How can I help you with the data?"}]

    #Excel chatbot--
    if doc_type == "Excel":
        st.title("📊 Talk to your Excel")

        uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)

            with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_db_file:
                db_path = temp_db_file.name

            engine = create_engine(f"sqlite:///{db_path}")
            df.to_sql(name='data', con=engine, if_exists='replace', index=False)

            db = SQLDatabase(engine)

            toolkit = SQLDatabaseToolkit(db=db, llm=llm)
            agent = create_sql_agent(
                llm=llm,
                toolkit=toolkit,
                verbose=True,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                handle_parsing_errors=True
            )

            
            for msg in st.session_state["Excel_messages"]:
                st.chat_message(msg["role"]).write(msg["content"])

          
            user_query = st.chat_input(placeholder="How can I help you with the data")

            if user_query:
                st.session_state["Excel_messages"].append({"role": "user", "content": user_query})
                st.chat_message("user").write(user_query)

                last_assistant_message = st.session_state["Excel_messages"][-1]["content"] if len(st.session_state["Excel_messages"]) > 1 else ""
                prompt = f"Context: The database has a table called 'data'. Previous assistant message: {last_assistant_message}. User query: {user_query}. Please provide only a final answer or a single action."

                
                with st.chat_message("assistant"):
                    streamlit_callback = StreamlitCallbackHandler(st.container())  
                    try:
                        response = agent.run(prompt, callbacks=[streamlit_callback])
                    except Exception as e:
                        response = f"Error: {str(e)}"
                    st.session_state["Excel_messages"].append({"role": "assistant", "content": response})
                    st.write(response)

    # SQL Database Chatbot 
    elif doc_type == "SQL":
        st.title("🦜 Talk to your SQL Database")

        db_uri = st.sidebar.selectbox("Choose the database type:", ["SQLite", "MySQL"])

        if db_uri == "MySQL":
            mysql_host = st.sidebar.text_input("Provide MySQL Host")
            mysql_user = st.sidebar.text_input("MySQL User")
            mysql_password = st.sidebar.text_input("MySQL Password", type="password")
            mysql_db = st.sidebar.text_input("MySQL Database")

        if db_uri == "SQLite":
            db_filepath = Path(__file__).parent / "student.db"
            creator = lambda: sqlite3.connect(f"file:{db_filepath}?mode=ro", uri=True)
            db = SQLDatabase(create_engine("sqlite:///", creator=creator))
        elif db_uri == "MySQL":
            if not (mysql_host and mysql_user and mysql_password and mysql_db):
                st.error("Please provide all MySQL connection details.")
                st.stop()
            db = SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))

        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True
        )

        
        for msg in st.session_state["SQL_messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

        
        user_query = st.chat_input(placeholder="Ask anything from the database")

        if user_query:
            st.session_state["SQL_messages"].append({"role": "user", "content": user_query})
            st.chat_message("user").write(user_query)

            
            with st.chat_message("assistant"):
                streamlit_callback = StreamlitCallbackHandler(st.container())  
                try:
                    response = agent.run(user_query, callbacks=[streamlit_callback])
                except Exception as e:
                    response = f"Error: {str(e)}"
                st.session_state["SQL_messages"].append({"role": "assistant", "content": response})
                st.write(response)

    # PDF Chatbot 
    elif doc_type == "PDF":
        st.title("Conversational RAG With PDF Uploads and Chat History")

        session_id = st.text_input("Session ID", value="default_session")

        if "store" not in st.session_state:
            st.session_state.store = {}

        uploaded_files = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=True)

        if uploaded_files:
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            documents = []
            for uploaded_file in uploaded_files:
                temppdf = "./temp.pdf"
                with open(temppdf, "wb") as file:
                    file.write(uploaded_file.getvalue())

                loader = PyPDFLoader(temppdf)
                docs = loader.load()
                documents.extend(docs)

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
            splits = text_splitter.split_documents(documents)
            vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
            retriever = vectorstore.as_retriever()

            contextualize_q_system_prompt = (
                "Given a chat history and the latest user question, "
                "formulate a standalone question which can be understood without the chat history."
            )
            contextualize_q_prompt = ChatPromptTemplate.from_messages([
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ])

            history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

            system_prompt = (
                "You are an assistant for question-answering tasks. "
                "Use the following pieces of retrieved context to answer the question. "
                "If you don't know the answer, say that you don't know. "
                "\n\n{context}"
            )
            qa_prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ])

            question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
            rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

            def get_session_history(session: str) -> BaseChatMessageHistory:
                if session_id not in st.session_state.store:
                    st.session_state.store[session_id] = ChatMessageHistory()
                return st.session_state.store[session_id]

            conversational_rag_chain = RunnableWithMessageHistory(
                rag_chain, get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer"
            )

            user_input = st.text_input("Your question:")
            if user_input:
                session_history = get_session_history(session_id)

                
                response = conversational_rag_chain.invoke({
                    'input': user_input
                }, {
                    'configurable': {
                        'session_id': session_id
                    }
                })

                
                st.write(response['answer'])  
