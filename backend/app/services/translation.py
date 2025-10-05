import time
import hashlib
import httpx
from typing import Dict, Any
from app.config import settings
from app.schemas.translation import SimplifyRequest, SimplifyResponse


class TranslationService:
    def __init__(self):
        self.hf_api_url = f"https://api-inference.huggingface.co/models/{settings.MODEL_NAME}"
        self.hf_token = settings.HF_API_TOKEN
    
    async def simplify_text(self, request: SimplifyRequest) -> SimplifyResponse:
        """Simplify German text using Hugging Face model"""
        start_time = time.time()
        
        # Prepare input for model
        prompt = self._prepare_prompt(request.input, request.mode)
        
        try:
            # Call Hugging Face API
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.hf_api_url,
                    headers={"Authorization": f"Bearer {self.hf_token}"} if self.hf_token else {},
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "max_new_tokens": request.max_output_chars,
                            "temperature": 0.7,
                            "do_sample": True,
                            "return_full_text": False
                        }
                    }
                )
                
                if response.status_code != 200:
                    raise Exception(f"Hugging Face API error: {response.status_code} - {response.text}")
                
                result = response.json()
                
                # Extract generated text
                if isinstance(result, list) and len(result) > 0:
                    output = result[0].get("generated_text", "")
                elif isinstance(result, dict):
                    output = result.get("generated_text", "")
                else:
                    output = str(result)
                
                # Clean up the output
                output = self._clean_output(output, request.input)
                
                processing_time = int((time.time() - start_time) * 1000)
                
                return SimplifyResponse(
                    job_id=str(hashlib.md5(request.input.encode()).hexdigest()[:8]),
                    status="done",
                    model_version=settings.MODEL_VERSION,
                    output=output,
                    processing_time_ms=processing_time,
                    cache_hit=False
                )
                
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            return SimplifyResponse(
                job_id=str(hashlib.md5(request.input.encode()).hexdigest()[:8]),
                status="failed",
                model_version=settings.MODEL_VERSION,
                output=None,
                processing_time_ms=processing_time,
                cache_hit=False
            )
    
    def _prepare_prompt(self, text: str, mode: str) -> str:
        """Prepare prompt for the model"""
        mode_text = "Leichte Sprache" if mode == "light" else "Einfache Sprache"
        return f"Vereinfache den folgenden Text in {mode_text}:\n\n{text}"
    
    def _clean_output(self, output: str, original_input: str) -> str:
        """Clean and validate the model output"""
        # Remove the prompt from the output if it's included
        if "Vereinfache den folgenden Text" in output:
            output = output.split("Vereinfache den folgenden Text")[-1].strip()
        
        # Remove any remaining prompt text
        lines = output.split('\n')
        cleaned_lines = []
        for line in lines:
            if not line.startswith("Vereinfache") and not line.startswith("Der folgende Text"):
                cleaned_lines.append(line)
        
        output = '\n'.join(cleaned_lines).strip()
        
        # Ensure output is not empty and not too long
        if not output or len(output) < 10:
            return "Entschuldigung, ich konnte den Text nicht vereinfachen."
        
        # Limit output length
        if len(output) > 2000:
            output = output[:2000] + "..."
        
        return output
