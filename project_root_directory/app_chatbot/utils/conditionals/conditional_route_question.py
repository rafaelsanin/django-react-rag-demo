from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

# LLM

local_llm = "llama3"


class QuestionRouter:
    def __init__(self, model, format, temperature):
        self.llm = ChatOllama(base_url="http://ollama:11434", model=model, format=format,
                              temperature=temperature)
        self.prompt_template = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an expert at routing a
            user question to a vectorstore or web search. Use the vectorstore for questions exclusively related to the JavaScript front-end web framework react.
            You do not need to be stringent with the keywords in the question related to these topics. Otherwise, use web-search. Give a binary choice 'web_search'
            or 'vectorstore' based on the question. Return the a JSON with a single key 'datasource' and
            no preamble or explanation. Question to route: {question} <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["question"],
        )
        self.question_router = self.prompt_template | self.llm | JsonOutputParser()


def route_question(state):
    """
    Route question to web search or RAG.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    question_router = QuestionRouter(
        model=local_llm, format='json', temperature=0).question_router
    print("---ROUTE QUESTION---")
    question = state["question"]
    print(question)
    source = question_router.invoke({"question": question})
    print(source)
    print(source["datasource"])
    if source["datasource"] == "web_search":
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return "websearch"
    elif source["datasource"] == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return "vectorstore"
