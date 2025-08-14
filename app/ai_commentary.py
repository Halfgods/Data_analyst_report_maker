import google.generativeai as genai
import json
import os

def get_gemini_api_key() -> str:
    """
    Centralized API key loader with fallback to api.json file.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        try:
            with open("api.json", "r") as f:
                api_key = json.load(f).get("GEMINI_API_KEY")
        except:
            pass
    return api_key

def truncate_dict(d, max_items=20):
    """
    Truncate large dictionaries to prevent prompt overflow.
    """
    if isinstance(d, dict) and len(d) > max_items:
        return dict(list(d.items())[:max_items])
    return d

def clean_gemini_output(response_text: str) -> str:
    """
    Clean Gemini model output by removing extra formatting.
    """
    cleaned = response_text.strip()
    cleaned = cleaned.replace("```markdown", "")
    cleaned = cleaned.replace("```", "")
    return cleaned.strip()

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

def get_ai_commentary(prompt: str, model_version: str = "gemini-1.5-flash") -> dict:
    """
    Sends the prompt to the Gemini API and captures the AI's textual response.
    """
    try:
        api_key = get_gemini_api_key()
        
        if not api_key:
            return {"error": "GEMINI_API_KEY not found in environment variables or api.json."}

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_version)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.0)
        )
        
        cleaned_response = clean_gemini_output(response.text)
        return {"commentary": cleaned_response}
    except Exception as e:
        return {"error": str(e)}

def get_data_specific_ai_response(user_question: str, analysis_summary: dict, model_version: str = "gemini-1.5-flash") -> dict:
    """
    Sends a user's question and data summary to the Gemini API, restricting the AI
    to answer only based on the provided data.
    """
    # Truncate large data structures to prevent token limits
    truncated_stats = truncate_dict(analysis_summary.get('descriptive_statistics', {}), max_items=15)
    truncated_groupby = truncate_dict(analysis_summary.get('groupby_aggregations', {}), max_items=10)
    truncated_corr = truncate_dict(analysis_summary.get('correlation_matrix', {}), max_items=10)
    
    prompt = f"""
    You are an expert data analyst. Based ONLY on the following data analysis summary, answer the user's question.
    Do NOT use any external knowledge. If the answer cannot be derived from the provided data, state that clearly.
    Please format the output in Markdown.
    Data Analysis Summary:
    Descriptive Statistics: {json.dumps(truncated_stats, indent=2)}
    Group-by Aggregations: {json.dumps(truncated_groupby, indent=2)}
    Correlation Matrix: {json.dumps(truncated_corr, indent=2)}

    User Question: {user_question}

    Answer:
    """
    try:
        api_key = get_gemini_api_key()
        
        if not api_key:
            return {"error": "GEMINI_API_KEY not found in environment variables or api.json."}

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_version)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.0)
        )
        
        cleaned_response = clean_gemini_output(response.text)
        return {"answer": cleaned_response}
    except Exception as e:
        return {"error": str(e)}
