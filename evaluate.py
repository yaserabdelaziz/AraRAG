import os
import json

import cohere
import pandas as pd
from dotenv import load_dotenv

load_dotenv(override=True)
from rag import RAG


def evaluate(co, question, agent_answer, ground_truth):
    preamble = """Your role is to test AI agents. Your task consists in assessing whether a agent output correctly answers a question. 
You are provided with the ground truth answer to the question. Your task is then to evaluate if the agent answer is close to the ground thruth answer. 

Think step by step and consider the agent output in its entirety. Remember: you need to have a strong and sound reason to support your evaluation.
If the agent answer is correct, return True. If the agent answer is incorrect, return False along with the reason.
You must output a single JSON object with keys 'correctness' and 'correctness_reason'. Make sure you return a valid JSON object.

The question that was asked to the agent, its output, and the expected ground truth answer will be delimited with XML tags."""
    message = f"""<question>
{question}
</question>

<agent_answer>
{agent_answer}
</agent_answer>

<ground_truth>
{ground_truth}
</ground_truth>"""
    response = co.chat(
        model='command-r',
        message=message,
        temperature=0.0,
        chat_history=[{"role": "system", "message": preamble}],
        prompt_truncation='AUTO',
        connectors=[]
    )
    json_response = json.loads(response.text[8:-4])
    correctness = json_response['correctness']
    correctness_reason = json_response['correctness_reason']
    return correctness, correctness_reason


if __name__ == '__main__':
    co = cohere.Client(os.getenv('COHERE_API_KEY'))
    rag = RAG()

    def df_evaluate(row):
        correctness, correctness_reason = evaluate(
            co,
            row["question"],
            row["agent_answer"],
            row["answer"]
        )
        row["correctness"] = correctness
        row["correctness_reason"] = correctness_reason
        return row

    eval_df = pd.read_csv("eval/eval_set.csv")
    eval_df["agent_answer"] = eval_df["question"].apply(lambda x: list(rag(x))[0])
    eval_df = eval_df.apply(df_evaluate, axis=1)
    eval_df.to_csv("eval/eval_set_results.csv", index=False)
    accuracy = eval_df["correctness"].mean()
    print(f"Accuracy: {accuracy}")
