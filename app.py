import gradio as gr

def search(image):
    print(type(image))
    return [image, image]

iface = gr.Interface(search, "image", outputs = ["image", "image"], description="Enter a search query")
iface.launch(share = True)