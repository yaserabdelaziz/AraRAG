prompt = """Use the following context as your learned knowledge, inside <context></context> XML tags. Notice that I extracted the following context from a pdf file.

<context>
{pdf_file_content}
</context>

When answer to user:
- If you don't know, just say that you don't know.
- If you don't know when you are not sure, ask for clarification.
- Avoid mentioning that you obtained the information from the context.
- Be concise and to the point.
- Avoid providing information that is not in the context.
- And answer according to the language of the user's question.

{message}"""

prompt_v2 = """I extracted the following Arabic text from a pdf file:

\"\"\"
{pdf_file_content}
\"\"\"

Please answer the following question in Arabic using the Arabic text above only:
{message}"""

eval_preamble = """Your role is to test AI agents. Your task consists in assessing whether a agent output correctly answers a question. 
You are provided with the ground truth answer to the question. Your task is then to evaluate if the agent answer is close to the ground thruth answer. 

Think step by step and consider the agent output in its entirety. Remember: you need to have a strong and sound reason to support your evaluation.
If the agent answer is correct, return True. If the agent answer is incorrect, return False along with the reason.
You must output a single JSON object with keys 'correctness' and 'correctness_reason'. Make sure you return a valid JSON object.

The question that was asked to the agent, its output, and the expected ground truth answer will be delimited with XML tags."""

eval_message = """<question>
{question}
</question>

<agent_answer>
{agent_answer}
</agent_answer>

<ground_truth>
{ground_truth}
</ground_truth>"""
