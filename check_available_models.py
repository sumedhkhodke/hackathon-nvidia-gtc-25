"""Script to check available NVIDIA Nemotron models via API."""
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_available_models():
    """Query NVIDIA API to list available models."""
    api_key = os.getenv("NVIDIA_API_KEY")
    
    if not api_key:
        print("❌ NVIDIA_API_KEY not found in environment!")
        return
    
    print("🔍 Querying NVIDIA API for available models...\n")
    print(f"API Key (first 10 chars): {api_key[:10]}...\n")
    
    try:
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )
        
        # List all available models
        models = client.models.list()
        
        print("=" * 80)
        print("📋 AVAILABLE MODELS")
        print("=" * 80)
        
        # Filter for Nemotron models
        nemotron_models = []
        all_models = []
        
        for model in models.data:
            all_models.append(model.id)
            if 'nemotron' in model.id.lower():
                nemotron_models.append(model.id)
        
        print(f"\n✅ Total models available: {len(all_models)}")
        print(f"✅ Nemotron models found: {len(nemotron_models)}\n")
        
        if nemotron_models:
            print("🤖 NEMOTRON MODELS:")
            print("-" * 80)
            for i, model_id in enumerate(sorted(nemotron_models), 1):
                print(f"{i:2}. {model_id}")
        else:
            print("⚠️  No Nemotron models found. Showing all models:\n")
            print("🤖 ALL AVAILABLE MODELS:")
            print("-" * 80)
            for i, model_id in enumerate(sorted(all_models), 1):
                print(f"{i:3}. {model_id}")
        
        print("\n" + "=" * 80)
        print("🎯 RECOMMENDED FOR PRIZE TRACK:")
        print("=" * 80)
        
        prize_track_models = {
            "Nemotron-Nano-12B-v2-VL": ["nemotron-nano-12b-v2-vl", "nemotron-12b-vl", "nano-12b"],
            "Nemotron-Safety-Guard-8B-v3": ["nemotron-safety-guard-8b-v3", "nemotron-safety", "llama-3.1-nemotron-safety"],
            "Nemotron-nano-9b-v2": ["nemotron-nano-9b-v2", "nano-9b", "nemotron-9b"],
            "Nemotron-super-49b-v1_5": ["nemotron-super-49b", "llama-3.3-nemotron-super", "nemotron-49b"]
        }
        
        for prize_model, search_terms in prize_track_models.items():
            print(f"\n🔍 Looking for '{prize_model}':")
            matches = []
            for model_id in all_models:
                model_lower = model_id.lower()
                if any(term in model_lower for term in search_terms):
                    matches.append(model_id)
            
            if matches:
                print(f"   ✅ Found: {', '.join(matches)}")
            else:
                print(f"   ❌ Not found - needs search pattern adjustment")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"❌ Error querying API: {str(e)}")
        print("\nPossible issues:")
        print("  1. API key is invalid or expired")
        print("  2. Network connection issue")
        print("  3. API endpoint has changed")
        print("\n💡 Get a new API key at: https://build.nvidia.com/")


if __name__ == "__main__":
    check_available_models()

