import gradio as gr

interface = gr.Interface(
    inputs=[gr.inputs.Image(label="Image")],
    outputs=[gr.outputs.Image(label="Output")],
)

# Show the interface
interface.launch(title="Image Demo")