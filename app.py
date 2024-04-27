from flask import Flask, redirect, request, render_template, session
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import pandas as pd
from langchain.globals import set_verbose
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.messages import SystemMessage

set_verbose(False)

set_verbose(False)
load_dotenv()
app = Flask(__name__)
app.secret_key = 'nader'

def load_csv_data():
    csv_file = "ev_vehicles.csv"
    try:
        return pd.read_csv(csv_file)
    except Exception as e:
        print(e)
        return pd.DataFrame()

def get_vectorstore(df):
    # Select relevant columns for embeddings
    relevant_columns = ['Exterior_Color__c', 'Interior_Color__c', 'Vehicle_Definition__c', 'List_Price__c', 'Steering_Type__c']
    # Combine selected columns into a single text description
    car_descriptions = df[relevant_columns].astype(str).agg(' '.join, axis=1)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=car_descriptions, embedding=embeddings)
    return vectorstore

@app.route('/', methods=['GET', 'POST'])
def index():
    df = load_csv_data()
    if df.empty:
        return render_template('index.html')

    vectorstore = get_vectorstore(df)

    # Recreate the conversation chain for each request
    conversation_chain = get_conversation_chain(vectorstore)

    if request.method == 'POST':
        user_question = request.form.get('user_question')
        response = handle_userinput(user_question, conversation_chain)
        return render_template('index.html', response=response, user_question=user_question)

    return render_template('index.html')

def get_conversation_chain(vectorstore):
    model_name = "gpt-3.5-turbo"
    temperature = 0.7

    general_system = r""" 
    Welcome to the Mercedes-Benz AutoWhiz, your expert AI for Mercedes-Benz vehicles!

    As your personal EV consultant, I'm dedicated to guiding you through our exceptional range of electric vehicles. My aim is to understand your specific needs and preferences to recommend the perfect Mercedes-Benz EV that aligns with your lifestyle and aspirations. 

    Please note that our discussions will solely focus on Mercedes-Benz vehicles. I am specifically designed not to engage in discussions about competitor brands or non-electric models.

    Given the context below, please provide a concise answer to the inquiry, and I will follow up with the best Mercedes-Benz EV options tailored to your needs.

    ----
    {context}
    ----
    """


    general_user = "User Question:\n```\n{question}\n```"

    messages = [
        SystemMessage(content=("You are an expert AI Sales Manager for Mercedes-Benz electric vehicles! As a personal EV consultant, you are dedicated to guiding users through the exceptional range of electric vehicles, focusing on sustainability, advanced technology, and unparalleled luxury. Your aim is to understand specific needs to recommend the perfect Mercedes-Benz EV that aligns with users' lifestyles. Please note that discussions are focused exclusively on Mercedes-Benz vehicles.")),        
        SystemMessagePromptTemplate.from_template(general_system),
        HumanMessagePromptTemplate.from_template(general_user),
    ]

    qa_prompt = ChatPromptTemplate.from_messages(messages)

    # Initialize the chat model
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)

    # Initialize memory
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    # Create the conversation chain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={'prompt': qa_prompt}
    )

    return conversation_chain

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session.pop('chat_history', None)  # This removes the chat history from the session
    return redirect('/')  # Redirects back to the main index page

def handle_userinput(user_question, conversation_chain):
    # Ensure chat history is initialized
    if 'chat_history' not in session:
        session['chat_history'] = []

    # Generate response from the conversational chain
    response = conversation_chain.invoke({'question': user_question})

    # Prepare a serializable format of the response, e.g., extracting just the textual response
    response_text = [msg.content for msg in response['chat_history'] if hasattr(msg, 'content')]

    # Flatten the chat history and update session
    session['chat_history'].extend(response_text)  # Use extend to add new messages to the flat list

    # Ensure to commit session changes
    session.modified = True

    return response_text

if __name__ == '__main__':
    app.run(debug=True)