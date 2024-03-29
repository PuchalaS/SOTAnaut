# main.py or a separate logging_config.py
import logging
from pathlib import Path

from elasticsearch_dsl import connections

from sotanaut.app.components.app_utils import generate_insights
from sotanaut.app.components.llm_loader import get_model
from sotanaut.app.components.llm_paper_retriever import LLMPaperRetriver
from sotanaut.db_handling.es_connection import ESConnection
from sotanaut.db_handling.es_indexer import ResearchPaper
from sotanaut.llm_handling.config.llm_settings import (
    GPT3_TURBO_1106_OPEN_AI_Config,
    GPT4_1106_OPEN_AI_Config,
)

# from sotanaut.llm_handling.models.local_model_transformers import LocalTransformersModel
from sotanaut.llm_handling.parsing.prompt_builder import PromptBuilder, PromptType
from sotanaut.paper_retrieval.downloader import PaperDownloader
from sotanaut.paper_retrieval.sources.arxiv import ArxivSource
from sotanaut.paper_retrieval.sources.google_scholar import GoogleScholarSource
from sotanaut.paper_retrieval.sources.pubmed import PubmedSource
from sotanaut.paper_retrieval.utils.helpers import find_best_match

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    es_connection = ESConnection()
    model = get_model("GPT3_TURBO_1106")
    paper_retriever = LLMPaperRetriver(model)

    sources = [
        ArxivSource(),
        PubmedSource(),
        GoogleScholarSource(),
    ]
    research_topic = "Trying to predict the cows birth time based on the body contractions"

    # keywords = paper_retriever.get_keywords(research_topic)
    # print(keywords)
    keywords = [
        "Cow parturition prediction",
        "Bovine birth timing contractions",
        "Predictive models for calving",
        "Labor contraction monitoring in cows",
        "Machine learning in cow birth prediction",
        # "AI/ML solutions",
        # "Pre-calving behavior patterns",
        # "Automated calving detection systems",
        # "Cattle parturition signs",
        # "Real-time monitoring of bovine labor",
        # "Precision livestock farming calving",
    ]
    papers = paper_retriever.search_for_papers(keywords, research_topic)
    FOLDER_TO_DOWNLOAD = Path("downloaded")
    # INDEX = "research-papers"
    for paper in papers:
        paper_pdf_path = FOLDER_TO_DOWNLOAD / f"{paper.id}.pdf"

        if not paper_pdf_path.exists():
            if download_path := PaperDownloader(paper).download_paper(
                folder_path=FOLDER_TO_DOWNLOAD
            ):
                print(f"Downloaded {paper.title}")
        else:
            print(f"Paper `{paper.title}` is already downloaded")

        if not ResearchPaper.get_document_with_id(paper.id):
            ResearchPaper.index_paper(paper, paper_pdf_path)
            print(f"Saved `{paper.title}` to es database")
        else:
            print(f"`{paper.title}` already in db")

    # summary = generate_insights(research_topic)
    # print(summary)

    # response = model.run_inference(system_message, user_prompt)
    # print(response)
    # filtered_paper_titles = LLMParser.parse_enumerated_output(response)
    # print(filtered_paper_titles)
    # choosen_papers = [find_best_match(llm_output_title ,papers) for llm_output_title in filtered_paper_titles]
    # paper_status = {}
    # for paper in papers: # choosen_papers:
    #     saved_to_db = False
    #     paper_downloader = PaperDownloader(paper)
    #     if file_path := paper_downloader.download_paper(
    #         folder_path="downloaded/"
    #     ):
    #         print(paper.id)
    #         saved_to_db = index_paper_to_elasticsearch(paper, file_path)
    #     paper_status[paper.title] = saved_to_db
    # print(paper_status)
