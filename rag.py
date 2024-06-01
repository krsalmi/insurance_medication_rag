# rag_model.py
from helper import get_openai_api_key
from utils import get_doc_tools
from pathlib import Path
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.agent import AgentRunner
from llama_index.core import VectorStoreIndex
from llama_index.core.objects import ObjectIndex
import os
from typing import List, Optional

def get_doc_files(directory: str):
    pdf_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_files.append(filename)
    return pdf_files

def prepare_docs_to_tools(papers: Optional[List[str]], directory: str):
    paper_to_tools_dict = {}
    for paper in papers:
        print(f"Getting tools for paper: {paper}")
        print(Path(paper).stem)
        vector_tool, summary_tool = get_doc_tools(os.path.join(directory, paper), Path(paper).stem)
        paper_to_tools_dict[paper] = [vector_tool, summary_tool]
    all_tools = [t for paper in papers for t in paper_to_tools_dict[paper]]
    return all_tools

def prepare_object_wrapper(all_tools: Optional[List]):
    obj_index = ObjectIndex.from_objects(
        all_tools,
        index_cls=VectorStoreIndex,
    )
    obj_retriever = obj_index.as_retriever(similarity_top_k=3)
    return obj_retriever

def get_agent(obj_retriever: Optional, llm: Optional, system_prompt: str = None):
    agent_worker = FunctionCallingAgentWorker.from_tools(
        tool_retriever=obj_retriever,
        llm=llm, 
        system_prompt=""" \
        You are an agent designed to evaluate and modify prescription texts 
        to meet specific insurance criteria. You will receive the name of a 
        drug, the name of a disease, and a prescription text. Your task is to 
        check if the prescription meets the criteria for the drug related to 
        the disease. If the criteria are not met, propose modifications to the 
        text so that it aligns with the criteria. Use square brackets to indicate
        the changes. Only include necessary changes and avoid adding unnecessary
        information. Ensure the modifications address all AND and OR conditions
        within the criteria. Output only the modified perscription text and any
        changes you make in [] brackets.
        """,
        verbose=True
    )
    agent = AgentRunner(agent_worker)
    return agent

def initialize_agent():
    get_openai_api_key()
    llm = OpenAI(model="gpt-4-turbo")
    doc_dir = 'docs'

    papers = get_doc_files(doc_dir)
    all_tools = prepare_docs_to_tools(papers, doc_dir)
    obj_retriever = prepare_object_wrapper(all_tools)

    agent = get_agent(obj_retriever, llm)
    return agent
