# main.py or a separate logging_config.py
import logging

from elasticsearch_dsl import connections

from sotanaut.db_handling.es_connection import create_connection
from sotanaut.db_handling.es_indexer import (
    ResearchPaper,
    ensure_elasticsearch_initialized,
    index_paper_to_elasticsearch,
)
from sotanaut.llm_handling.config.llm_settings import (
    GPT3_TURBO_1106_OPEN_AI_Config,
    GPT4_1106_OPEN_AI_Config,
)
from sotanaut.llm_handling.models.model_factory import ModelFactory

# from sotanaut.llm_handling.models.local_model_transformers import LocalTransformersModel
from sotanaut.llm_handling.models.open_ai_api_model import OpenAIModel
from sotanaut.llm_handling.parsing.llm_parser import LLMParser
from sotanaut.llm_handling.parsing.prompt_builder import PromptBuilder, PromptType
from sotanaut.paper_retrieval.downloader import PaperDownloader
from sotanaut.paper_retrieval.sources.arxiv import ArxivSource
from sotanaut.paper_retrieval.sources.google_scholar import GoogleScholarSource
from sotanaut.paper_retrieval.sources.pubmed import PubmedSource

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    create_connection()
    ensure_elasticsearch_initialized()

    model_settings = GPT4_1106_OPEN_AI_Config().get_params()
    model_type = model_settings["model_type"]
    model = ModelFactory.get_model(model_type, model_settings)

    sources = [
        ArxivSource(),
        # PubmedSource(),
        # GoogleScholarSource()
    ]
    prompt_builder = PromptBuilder()
    research_topic = "Trying to predict the cows birth time based on the body contractions"

    system_message = prompt_builder.get_system_message(prompt_type=PromptType.KEYWORD_GENERATION)
    user_prompt = prompt_builder.get_user_prompt(
        prompt_type=PromptType.KEYWORD_GENERATION,
        output_formats={"enumerated_list": None, "limit_output": {"limit_value": 5}},
        research_topic=research_topic,
    )

    # response = model.run_inference(system_message, user_prompt)
    # print(response)

    # keywords = LLMParser.parse_enumerated_output(response)
    # print(keywords)
    # keywords = ["Flower Image Classification","Plant Identification","Botanical Recognition","Floral Category Detection","Computer Vision in Botany","Machine Learning for Flowers","Deep Learning for Plants","CNN for Plant Identification","SVM for Floral Categories","RGB Analysis for Flowers","Color Spectrum Extraction for Plants","Feature Selection for Flower Images","Data Augmentation for Botanical Datasets","Transfer Learning for Plant Identification","Ensemble Methods for Flower Classification","Performance Evaluation in Flower Recognition","Benchmark Datasets for Plant Identification","Challenges in Flower Image Classification","Future Directions in Floral Recognition Research"]
    # # keywords = ["precision agriculture", "crop yield prediction", "disease detection in plants", "soil nutrient analysis using ML"]
    # # keywords = ["fraud detection using deep learning", "stock market prediction algorithms", "customer spending pattern analysis", "credit scoring with ML"]
    # keywords = [
    #     "Cow parturition prediction",
    #     "Bovine birth timing contractions",
    #     "Predictive models for calving",
    #     "Labor contraction monitoring in cows",
    #     "Machine learning in cow birth prediction",
    #     # "AI/ML solutions",
    #     # "Pre-calving behavior patterns",
    #     # "Automated calving detection systems",
    #     # "Cattle parturition signs",
    #     # "Real-time monitoring of bovine labor",
    #     # "Precision livestock farming calving",
    # ]
    keywords = [
        "Cattle Parturition Prediction",
        "Bovine Birth Timing",
        "Cow Labor Contraction Monitoring",
        "Machine Learning in Livestock Birth Predictions",
        "Predictive Analytics for Animal Birthing",
    ]
    papers = []
    for source in sources:
        papers.extend(source.get_papers(keywords, max_results=5))
    for paper in papers:
        paper_downloader = PaperDownloader(paper)
        file_path = paper_downloader.download_paper(folder_path="downloaded/")
        index_paper_to_elasticsearch(paper, file_path)

    # paper_descriptions = [
    #     f"{(paper_num+1)}. {paper.short_description()}" for paper_num, paper in enumerate(papers)
    # ]

    # system_message = prompt_builder.get_system_message(prompt_type=PromptType.PAPER_FILTERING)
    # user_prompt = prompt_builder.get_user_prompt(
    #     prompt_type=PromptType.PAPER_FILTERING,
    #     output_formats={"enumerated_list": None, "concise": None},
    #     research_topic=research_topic,
    #     papers=paper_descriptions,
    # )

    # print(system_message)
    # print(user_prompt)

    # response = model.run_inference(system_message, user_prompt)
    # filtered_paper_titles = LLMParser.parse_enumerated_output(response)

    # print(response)
    # print(filtered_paper_titles)
    # choosen_papers = [paper for paper in papers if any(filtered_title in paper.title for filtered_title in filtered_paper_titles)]
    # print(choosen_papers)
    # for paper in choosen_papers:
    #     print(paper.link)
    #     paper.download_paper("downloaded")
