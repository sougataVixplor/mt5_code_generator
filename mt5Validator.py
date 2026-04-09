from gemini import get_gemini_response

def validate_mt5_code(mt5_code):
    prompt = f"""
    You are an expert MetaTrader 5 (MQL5) developer. 
    Review the following MT5 code for syntax errors, logical bugs, and best practices.
    If there are any issues, fix them and return the corrected, fully-functional MT5 code.
    If the code is already correct, return it as is.
    Do not include any explanations or conversational text. Return ONLY the complete MT5 code without any formatting markdown blocks if possible.
    If you must use markdown blocks, ensure it's ONLY standard ```mql5 blocks.
    
    Code:
    ```mql5
    {mt5_code}
    ```
    """
    response = get_gemini_response(prompt, isJson=False)
    
    # Attempt to clean markdown
    if "```mql5" in response:
        response = response.split("```mql5")[1].split("```")[0].strip()
    elif "```cpp" in response:
        response = response.split("```cpp")[1].split("```")[0].strip()
    elif "```" in response:
        response = response.split("```")[1].split("```")[0].strip()
        
    return response.strip()
