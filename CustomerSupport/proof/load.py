from strands.models import BedrockModel
def load_model():
    return BedrockModel(
        model_id="amazon.titan-text-express-v1",
        temperature=0.2,
        max_tokens=512,
    )
