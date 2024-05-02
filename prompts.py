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
