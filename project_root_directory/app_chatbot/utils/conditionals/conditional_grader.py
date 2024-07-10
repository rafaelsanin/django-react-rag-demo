from pprint import pprint
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

# LLM

local_llm = "llama3"


class HallucinationGrader:
    def __init__(self, model, format, temperature):
        self.llm = ChatOllama(base_url="http://ollama:11434", model=model, format=format,
                              temperature=temperature)
        self.prompt_template = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a grader assessing whether
            an answer is grounded in / supported by a set of facts. Give a binary 'yes' or 'no' score to indicate
            whether the answer is grounded in / supported by a set of facts. Provide the binary score as a JSON with a
            single key 'score' and no preamble or explanation. <|eot_id|><|start_header_id|>user<|end_header_id|>
            Here are the facts:
            \n ------- \n
            {documents}
            \n ------- \n
            Here is the answer: {generation}  <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["generation", "documents"],
        )
        self.hallucination_grader = self.prompt_template | self.llm | JsonOutputParser()


class AnswerGrader:
    def __init__(self, model, format, temperature):
        self.llm = ChatOllama(base_url="http://ollama:11434", model=model, format=format,
                              temperature=temperature)
        self.prompt_template = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a grader assessing whether an
            answer is useful to resolve a question. Give a binary score 'yes' or 'no' to indicate whether the answer is
            useful to resolve a question. Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
             <|eot_id|><|start_header_id|>user<|end_header_id|> Here is the answer:
            \n ------- \n
            {generation}
            \n ------- \n
            Here is the question: {question} <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["generation", "question"],
        )
        self.answer_grader = self.prompt_template | self.llm | JsonOutputParser()


def grade_generation_v_documents_and_question(state):
    """
    Determines whether the generation is grounded in the document and answers question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Decision for next node to call
    """
    hallucination_grader = HallucinationGrader(
        model=local_llm, format="json", temperature=0).hallucination_grader
    answer_grader = AnswerGrader(
        model=local_llm, format="json", temperature=0).answer_grader
    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )
    grade = score["score"]

    # Check hallucination
    if grade == "yes":
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        # Check question-answering
        print("---GRADE GENERATION vs QUESTION---")
        score = answer_grader.invoke(
            {"question": question, "generation": generation})
        grade = score["score"]
        if grade == "yes":
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        pprint("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"
