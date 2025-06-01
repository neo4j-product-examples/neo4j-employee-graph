import os
import json
import asyncio

import getpass
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pypdf import PdfReader
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
from typing import List
from tqdm.asyncio import tqdm as tqdm_async

from person import Person, get_short_id


def read_resumes_from_directory(directory="resume-pdfs"):
    """
    Read all PDFs from a directory and return a list of text strings
    """
    resumes = []

    # Check if directory exists
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return resumes

    # Get all PDF files from the directory
    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print(f"No PDF files found in '{directory}'.")
        return resumes

    # Process each PDF file
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory, pdf_file)

        try:
            # Extract text from PDF
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                # IMPORTANT Create a unique id for each person.
                # In this case we can do it by file name but may vary by use case
                # It is important to think about how things are identified in entity extraction
                # so that they get properly resolved in the graph
                # Usually you do not want to use names.
                person_id = get_short_id(pdf_file)
                text += f"PersonID: {person_id}\n"
                for page in pdf_reader.pages:
                    text += page.extract_text()

            resumes.append(text)
            print(f"Processed: {pdf_file} ({len(text)} characters)")
        except Exception as e:
            print(f"Error with {pdf_file}: {str(e)}")

    print(f"Total resumes loaded: {len(resumes)}")
    return resumes


def chunks(xs, n=10):
    n = max(1, n)
    return [xs[i:i + n] for i in range(0, len(xs), n)]



class TextExtractor:
    def __init__(self,
                 llm_with_struct_output,
                 prompt_template: PromptTemplate):
        self.llm = llm_with_struct_output
        self.prompt_template = prompt_template

    async def extract(self, texts: List[str], semaphore) -> BaseModel:
        async with semaphore:
            prompt = self.prompt_template.invoke({'texts': '\n\n'.join(texts)})
            # Use structured LLM for extraction
            entity: BaseModel = await self.llm.ainvoke(prompt)
        return entity


    async def extract_all(self, texts: List[str], chunk_size=1, max_workers=10) -> List[BaseModel]:
        # Create a semaphore with the desired number of workers
        semaphore = asyncio.Semaphore(max_workers)

        # Create tasks with the semaphore
        text_chunks = chunks(texts, chunk_size)
        tasks = [self.extract(text_chunk, semaphore) for text_chunk in text_chunks]

        # Explicitly update progress using `tqdm` as tasks complete
        entities: List[BaseModel] = []
        with tqdm_async(total=len(tasks), desc="extracting texts") as pbar:
            for future in asyncio.as_completed(tasks):
                result = await future
                entities.append(result)
                pbar.update(1)  # Increment progress bar for each completed task
        return entities


def main():
    # Load resumes
    resumes = read_resumes_from_directory()

    #Get LLM api key
    load_dotenv('.env', override=True)
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI AI API key: ")

    # Define Prompt and LLM with structured output
    people_prompt_template = PromptTemplate.from_template("""
    You are extracting information from resumes according to the people schema. Below is the resume.
    Only include information explicitly listed in the resume.
    # Resume
    {texts}
    """)
    llm = ChatOpenAI(model="gpt-4.1", temperature=0).with_structured_output(Person)

    # Perform entity extraction
    text_extractor = TextExtractor(llm, people_prompt_template)
    people = asyncio.run(text_extractor.extract_all(resumes))

    # Save extracted entities to json file
    people_list = [person.model_dump() for person in people]
    with open('extracted-people-data.json', 'w') as json_file:
        json.dump(people_list, json_file, indent=4)

    print("JSON file created: extracted-people-data.json")

if __name__ == "__main__":
    main()


