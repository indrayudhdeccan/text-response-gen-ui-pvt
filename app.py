import uuid
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

from llm import get_client, MODEL_OPTIONS
from storage.supabase import save_response


def handle_prompt(prompt: str, model_name: str):
    if not prompt.strip():
        return "", "Please enter a prompt."

    uid = str(uuid.uuid4())

    try:
        client = get_client(model_name)
        response = client.generate(prompt)
    except Exception as e:
        return "", f"LLM error: {e}"

    try:
        save_response(uid, prompt, response, model_name)
        status = f"Saved to Supabase  |  id: {uid}"
    except Exception as e:
        status = f"Response generated but failed to save: {e}"

    return response, status


with gr.Blocks(title="Text Response Generator") as demo:
    gr.Markdown("## Text Response Generator")

    with gr.Row():
        model_dropdown = gr.Dropdown(
            choices=MODEL_OPTIONS,
            value=MODEL_OPTIONS[0],
            label="Model",
        )

    prompt_box = gr.Textbox(
        label="Prompt",
        placeholder="Type your prompt here...",
        lines=4,
    )
    submit_btn = gr.Button("Generate", variant="primary")

    response_box = gr.Textbox(label="Response", lines=12, interactive=False)
    status_bar = gr.Textbox(label="Status", interactive=False)

    submit_btn.click(
        fn=handle_prompt,
        inputs=[prompt_box, model_dropdown],
        outputs=[response_box, status_bar],
    )

if __name__ == "__main__":
    demo.launch()
