import google.generativeai as genai
import json
import os

def prepare_ai_prompt(analysis_summary: dict) -> str:
    """
    Prepares a prompt for an AI model with processed summary tables.
    """
    prompt = """
    Please provide a concise factual commentary on the following data analysis summary.
    Focus on data quality, trends, and anomalies, data quality issues, and potential improvements. Please format the output in Markdown.

    **Descriptive Statistics:**
    {descriptive_stats}

    **Group-by Aggregations:**
    {groupby_aggregations}

    **Correlation Matrix:**
    {correlation_matrix}
    """.format(
        descriptive_stats=json.dumps(analysis_summary.get('descriptive_statistics', {}), indent=2),
        groupby_aggregations=json.dumps(analysis_summary.get('groupby_aggregations', {}), indent=2),
        correlation_matrix=json.dumps(analysis_summary.get('correlation_matrix', {}), indent=2)
    )
    return prompt

def get_ai_commentary(prompt: str) -> dict:
    """
    Sends the prompt to the Gemini API and captures the AI's textual response.
    """
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            # Try to read from api.json if environment variable is not set
            try:
                with open("api.json", "r") as f:
                    config = json.load(f)
                    api_key = config.get("GEMINI_API_KEY")
            except FileNotFoundError:
                return {"error": "api.json not found and GEMINI_API_KEY environment variable not set."}
            except json.JSONDecodeError:
                return {"error": "Error decoding api.json. Make sure it's valid JSON."}

        if not api_key:
            return {"error": "GEMINI_API_KEY not found in environment variables or api.json."}

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.0)
        )
        return {"commentary": response.text}
    except Exception as e:
        return {"error": str(e)}

def get_data_specific_ai_response(user_question: str, analysis_summary: dict) -> dict:
    """
    Sends a user's question and data summary to the Gemini API, restricting the AI
    to answer only based on the provided data.
    """
    prompt = f"""
    You are an expert data analyst. Based ONLY on the following data analysis summary, answer the user's question.
    Do NOT use any external knowledge. If the answer cannot be derived from the provided data, state that clearly.
    Please format the output in Markdown.
    Data Analysis Summary:
    Descriptive Statistics: {json.dumps(analysis_summary.get('descriptive_statistics', {}), indent=2)}
    Group-by Aggregations: {json.dumps(analysis_summary.get('groupby_aggregations', {}), indent=2)}
    Correlation Matrix: {json.dumps(analysis_summary.get('correlation_matrix', {}), indent=2)}

    User Question: {user_question}

    Answer:
    """
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            try:
                with open("api.json", "r") as f:
                    config = json.load(f)
                    api_key = config.get("GEMINI_API_KEY")
            except FileNotFoundError:
                return {"error": "api.json not found and GEMINI_API_KEY environment variable not set."}
            except json.JSONDecodeError:
                return {"error": "Error decoding api.json. Make sure it's valid JSON."}

        if not api_key:
            return {"error": "GEMINI_API_KEY not found in environment variables or api.json."}

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.0)
        )
        return {"answer": response.text}
    except Exception as e:
        return {"error": str(e)}