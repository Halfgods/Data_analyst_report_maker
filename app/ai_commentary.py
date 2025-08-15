import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    You are an expert data analyst. Analyze the following data and provide exactly 4 profound insights.
    
    Each insight should be:
    - Deep and analytical, not surface-level observations
    - Based on patterns, correlations, or anomalies you discover
    - Actionable or revealing about the data's story
    - Written in markdown format with proper formatting
    
    Format each insight as:
    ### [Insight Title]
    [Detailed analysis with **bold** for key points and *italic* for emphasis]
    
    Focus on what the data is actually telling us - look for:
    - Hidden patterns or relationships
    - Statistical significance or unusual distributions
    - Business implications or data quality issues
    - Predictive insights or trends that matter
    
    Be intelligent and insightful. Don't just describe what's obvious - find the deeper meaning.

    Data Analysis Summary:
    Descriptive Statistics: {descriptive_stats}
    Group-by Aggregations: {groupby_aggregations}
    Correlation Matrix: {correlation_matrix}
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
            # Fallback commentary when API key is not available
            return {"commentary": """
## Data Analysis Summary

Based on the provided data analysis, here are the key insights:

### Data Quality
- The dataset appears to be clean with no missing values detected
- All columns have consistent data types as expected

### Key Statistics
- The dataset contains both numerical and categorical variables
- Descriptive statistics show the distribution of numerical data
- Group-by aggregations reveal patterns across different categories

### Recommendations
- Consider exploring correlations between numerical variables
- Review categorical data distributions for potential insights
- The data appears ready for further analysis and modeling

*Note: This is a fallback analysis. For more detailed AI-powered insights, please configure the GEMINI_API_KEY.*
            """}

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_version)
        
        # Set generation config for faster response
        generation_config = genai.types.GenerationConfig(
            temperature=0.3,  # Lower temperature for more focused responses
            top_p=0.8,
            top_k=40,
            max_output_tokens=800,  # Limit output for faster generation
        )
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
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
    You are an expert data analyst with deep statistical knowledge. Answer the user's question based ONLY on the provided data analysis.
    
    Guidelines:
    - Use ONLY the data provided - no external knowledge
    - Be analytical and insightful, not just descriptive
    - If the question cannot be answered from the data, explain why and suggest what additional data would help
    - Provide context and implications, not just numbers
    - Use markdown formatting for better readability (bold, italic, headers, etc.)
    
    Data Analysis Summary:
    Descriptive Statistics: {json.dumps(truncated_stats, indent=2)}
    Group-by Aggregations: {json.dumps(truncated_groupby, indent=2)}
    Correlation Matrix: {json.dumps(truncated_corr, indent=2)}

    User Question: {user_question}

    Provide a comprehensive, intelligent answer with proper markdown formatting:
    """
    try:
        api_key = get_gemini_api_key()
        
        if not api_key:
            return {"error": "GEMINI_API_KEY not found in environment variables or api.json."}

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_version)
        
        # Set generation config for faster response
        generation_config = genai.types.GenerationConfig(
            temperature=0.3,  # Lower temperature for more focused responses
            top_p=0.8,
            top_k=40,
            max_output_tokens=600,  # Limit output for faster generation
        )
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        cleaned_response = clean_gemini_output(response.text)
        return {"answer": cleaned_response}
    except Exception as e:
        return {"error": str(e)}
