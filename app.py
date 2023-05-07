import gradio as gr
import os

def flip(i):
    return i.rotate(180)

css = "footer {display: none !important;} .gradio-container {min-height: 0px !important;}"

with gr.Blocks(css=css) as demo:
    with gr.Row():
        with gr.Column():
            img_i = gr.Image(label="Input Image", type="pil")
        with gr.Column():
            img_o = gr.Image(label="Output Image")
    with gr.Row():
        btn = gr.Button(value="Flip Image")
    btn.click(flip, inputs=[img_i], outputs=[img_o])

    examples = gr.Examples(
        [ 
            os.path.join(os.path.dirname(__file__), "images/cheetah1.jpg"),
            os.path.join(os.path.dirname(__file__), "images/lion.jpg"),
        ],
        img_i,
        img_o,
        flip
    )


    
    
demo.launch()