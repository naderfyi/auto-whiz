from flask import Flask, redirect, request, jsonify, session
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import pandas as pd
from langchain.globals import set_verbose
import json
from flask_cors import CORS
from langchain.prompts.prompt import PromptTemplate
from pandas import json_normalize
from flask import send_from_directory, current_app
import os

set_verbose(False)
load_dotenv()
app = Flask(__name__)
CORS(app)
app.secret_key = 'nader'

@app.route('/img/<path:filename>')
def send_img(filename):
    # Assuming images are stored in 'static/img'
    img_directory = os.path.join(current_app.root_path, 'static', 'img')
    return send_from_directory(img_directory, filename)

def load_data(json_filepath):
    with open(json_filepath, 'r') as file:
        data = json.load(file)

    # Attempt to flatten the data
    flat_data = []
    for car_key, car_value in data.items():
        try:
            flat_record = json_normalize(car_value)
            flat_data.append(flat_record)
        except Exception as e:
            print(f"Error processing key {car_key}: {e}")
            continue

    if not flat_data:
        return pd.DataFrame()

    df = pd.concat(flat_data, ignore_index=True)
    return df

def get_vectorstore(df):
    # Select relevant columns for embeddings, based on the car data structure you have
    relevant_columns = [
        'car_name', 
        'price_info.germany',
        'range_info.City - Cold Weather *', 
        'range_info.Highway - Cold Weather *', 
        'range_info.Combined - Cold Weather *', 
        'range_info.City - Mild Weather *', 
        'range_info.Highway - Mild Weather *', 
        'range_info.Combined - Mild Weather *', 
        'performance_info.acceleration', 
        'performance_info.top_speed', 
        'performance_info.electric_range', 
        'performance_info.total_power', 
        'performance_info.total_torque', 
        'performance_info.drive', 
        'battery_info.nominal_capacity', 
        'battery_info.battery_type', 
        'battery_info.number_of_cells', 
        'battery_info.architecture', 
        'battery_info.warranty_period', 
        'battery_info.warranty_mileage', 
        'battery_info.useable_capacity', 
        'battery_info.cathode_material', 
        'battery_info.pack_configuration', 
        'battery_info.nominal_voltage', 
        'battery_info.form_factor', 
        'battery_info.name___reference', 
        'charging_info.home_destination.charge_port', 
        'charging_info.home_destination.port_location', 
        'charging_info.home_destination.charge_power', 
        'charging_info.fast_charging.fastcharge_port', 
        'charging_info.fast_charging.fc_port_location', 
        'charging_info.fast_charging.fastcharge_power_max', 
        'charging_info.fast_charging.fastcharge_power_10-80%', 
        'charging_info.plug_charge.plug_&_charge_supported', 
        'v2x_info.v2l.v2l_supported', 
        'v2x_info.v2l.max_output_power', 
        'v2x_info.v2h.v2h_via_ac_supported', 
        'v2x_info.v2h.max_output_power', 
        'v2x_info.v2g.v2g_via_ac_supported', 
        'v2x_info.v2g.max_output_power', 
        'efficiency_info.evdb_real_range.range', 
        'efficiency_info.evdb_real_range.vehicle_consumption', 
        'efficiency_info.wltp_ratings_tel.range', 
        'efficiency_info.wltp_ratings_tel.rated_consumption', 
        'efficiency_info.wltp_ratings_tel.vehicle_consumption', 
        'efficiency_info.wltp_ratings_teh.range', 
        'efficiency_info.wltp_ratings_teh.rated_consumption', 
        'efficiency_info.wltp_ratings_teh.vehicle_consumption', 
        'real_energy_consumption.city_cold weather_cold_weather', 
        'real_energy_consumption.highway_cold weather_cold_weather', 
        'real_energy_consumption.combined_cold weather_cold_weather', 
        'real_energy_consumption.city_mild weather_mild_weather', 
        'real_energy_consumption.highway_mild weather_mild_weather', 
        'real_energy_consumption.combined_mild weather_mild_weather'
    ]
    
    # Combine selected columns into a single text description
    car_descriptions = df[relevant_columns].astype(str).agg(' '.join, axis=1)
    
    # Assume the rest of the function processes these descriptions with embedding and vector store creation
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=car_descriptions, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    model_name = "gpt-3.5-turbo"
    temperature = 0.7
    
    qa_template = """
        Welcome to AutoWhiz Mercedes-Benz's AI Assistant, your personal guide to finding the perfect vehicle!
        
        Let's embark on this journey together to discover your dream ride.
        I can only talk about the Mercedes-Benz brand.
        If I am asked about non EV cars, I will try to convince them with the benefits of EV cars and why they should consider getting one.
        I am here to assist you in selecting the ideal Mercedes-Benz vehicle tailored precisely to your desires, needs, and budget.
        I will Keep your answers brief and concise, yet engaging and friendly.
        I will Sound human, and avoid sounding too robotic or scripted.
        Please provide me with some context to better understand your preferences and requirements.
        context: {context}
        Now, what questions do you have regarding Mercedes-Benz vehicles or the car-buying process?
        question: {question}
        """
        
    # Define the PromptTemplate
    QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["context","question" ])

    # Initialize the chat model
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)

    # Initialize memory
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    # Create the conversation chain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={'prompt': QA_PROMPT}
    )

    return conversation_chain

@app.route('/', methods=['GET', 'POST'])
def index():
    cars_json = "ev_vehicles.json"
    
    df_car = load_data(cars_json)
    if df_car.empty:
        return jsonify({'error': 'Data not loaded correctly'}), 500

    vectorstore = get_vectorstore(df_car)

    # Recreate the conversation chain for each request
    conversation_chain = get_conversation_chain(vectorstore)

    if request.method == 'POST':
        user_question = request.form.get('user_question')
        if not user_question:
            return jsonify({'error': 'No question provided'}), 400

        response = handle_userinput(user_question, conversation_chain)
        return jsonify({'response': response, 'user_question': user_question})

    return jsonify({'message': 'Welcome to the EV Vehicles FAQ Bot'})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session.pop('chat_history', None)
    return redirect('/')

@app.route('/set_api_key', methods=['POST'])
def set_api_key():
    api_key = request.form.get('api_key')
    if not api_key:
        return jsonify({'error': 'API key is required'}), 400
    #session['API_KEY'] = api_key
    os.environ['API_KEY'] = api_key
    return jsonify({'message': 'API key set successfully'}), 200

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