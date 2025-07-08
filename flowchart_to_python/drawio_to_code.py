from parse_drawio import parse_drawio_xml
from query_deepseek import query_deepseek

def generate_prompt_from_blocks(blocks):

    lines = ["Convert the following flowchart into Python code:\n"]
    id_map = {block['id']: block for block in blocks}

    for block in blocks:

        desc = f"{block['type']}: {block['text']}"

        for con in block['connections']:

            target_text = id_map.get(con['to'], {}).get("text", "???")

            label = f" if '{con['label']}'" if con['label'] else ""

            desc += f" -> {target_text}{label}"# use to make decription for block of code

        lines.append(desc)

    return "\n".join(lines)

if __name__ == "__main__":
    file_path = "NumList.drawio"  
    api_key = "your-api-key" # Replace with your actual DeepSeek API key before running

    blocks = parse_drawio_xml(file_path)
    print("\n Generating Prompt...")
    #prompt for ai
    prompt = "You are a Python code generator that takes simplified flowchart-like \"blocked code\" as input. The input consists of steps labeled, with arrows indicating flow. Convert this into equivalent, clean Python code that preserves the logic. Do not explain anything—just return the raw code. Input Format Example: \"Start: Start → Ask For A Number Process: Ask For A Number → Generate a random number from 1-10 Process: Generate a random number from 1-10 → Is Inputted number the generated Number? Decision: Is Inputted number the generated Number? → End if 'Yes' → Ask For A Number if 'No' End: End\" Expected Output for Example Input: \"import random while True: num = int(input(\"Enter a number: \")) if num == random.randint(1,10): break\" Here is the Actual Input:\n" + generate_prompt_from_blocks(blocks) + "Output only the raw Python code with no formatting or extra text or emojis no need for extra titles or words, complete as fast as possible."
    
    print(prompt)

    print("\n Asking AI...")
    code = query_deepseek(prompt, api_key)

    print("\n Python Code:\n")

    print(code)



