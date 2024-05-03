import os
import json

import cohere
import pandas as pd
from dotenv import load_dotenv

load_dotenv(override=True)
from rag import RAG
from prompts import eval_preamble, eval_message


def evaluate(co, question, agent_answer, ground_truth):
    response = co.chat(
        model='command-r',
        message=eval_message.format(question=question, agent_answer=agent_answer, ground_truth=ground_truth),
        temperature=0.0,
        chat_history=[{"role": "system", "message": eval_preamble}],
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
