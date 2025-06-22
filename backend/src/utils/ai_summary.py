import openai
from ..config import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_ai_summary(findings: dict) -> str:
    """Generate AI-powered summary of security findings"""
    prompt = f"""
    As a security expert, analyze these vulnerability scan results and provide a concise summary:
    
    {json.dumps(findings, indent=2)}
    
    Focus on:
    - Critical risks that need immediate attention
    - Potential business impact
    - Recommended remediation steps
    - Security best practices
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a security analyst summarizing vulnerability scan results"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )
    
    return response.choices[0].message.content