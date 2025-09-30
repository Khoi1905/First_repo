import os
from jinja2 import Template

def render_prompt(template_path, **kwargs):
    template_path = os.path.join(os.path.dirname(__file__), template_path)
    with open(template_path, "r", encoding="utf-8") as f:
        template_str = f.read()
    template = Template(template_str)
    return template.render(**kwargs)

def ask_llm(llm, prompt):
    response = llm.invoke(prompt)
    if isinstance(response, str):
        return response
    return response.content