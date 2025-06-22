import openai
import tiktoken
from datetime import datetime
from ..config import settings
from ..core.database import SessionLocal
from ..core.models import AILog

# Initialize tokenizer
tokenizer = tiktoken.get_encoding("cl100k_base")

# Cost tracking dictionary
ai_costs = {
    "last_reset": datetime.utcnow(),
    "daily_cost": 0.0
}

def calculate_token_cost(tokens: int, model: str = "gpt-4o") -> float:
    """Calculate cost based on OpenAI pricing"""
    pricing = {
        "gpt-4o": {"input": 5.00, "output": 15.00},  # $5/million input, $15/million output
        "gpt-4-turbo": {"input": 10.00, "output": 30.00}
    }
    return (tokens / 1_000_000) * pricing.get(model, pricing["gpt-4o"])["output"]

def generate_ai_summary(findings: dict) -> str:
    """Generate AI-powered summary with cost controls"""
    # Reset daily cost tracking at midnight UTC
    if datetime.utcnow().date() > ai_costs["last_reset"].date():
        ai_costs["daily_cost"] = 0.0
        ai_costs["last_reset"] = datetime.utcnow()
    
    # Check daily cost limit ($10/day default)
    if ai_costs["daily_cost"] > settings.max_daily_ai_cost:
        return "AI summary unavailable: Daily limit exceeded"
    
    prompt = f"""
    As a security expert, analyze these vulnerability scan results and provide a concise summary:
    
    {json.dumps(findings, indent=2)[:8000]}  # Truncate to 8000 chars
    
    Focus on:
    - Critical risks that need immediate attention
    - Potential business impact
    - Recommended remediation steps
    - Security best practices
    """
    
    # Calculate token usage
    input_tokens = len(tokenizer.encode(prompt))
    max_tokens = min(500, settings.max_ai_tokens_per_report or 500)
    
    try:
        response = openai.ChatCompletion.create(
            model=settings.ai_model or "gpt-4o",
            messages=[
                {"role": "system", "content": "You are a security analyst summarizing vulnerability scan results"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=max_tokens
        )
        
        # Track costs
        output_tokens = response.usage["completion_tokens"]
        total_tokens = response.usage["total_tokens"]
        cost = calculate_token_cost(total_tokens)
        ai_costs["daily_cost"] += cost
        
        # Log usage
        db = SessionLocal()
        try:
            log_entry = AILog(
                scan_id=findings.get("scan_id", "unknown"),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
                model=response.model
            )
            db.add(log_entry)
            db.commit()
        finally:
            db.close()
        
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"AI summary failed: {str(e)}")
        return "AI summary unavailable due to technical error"