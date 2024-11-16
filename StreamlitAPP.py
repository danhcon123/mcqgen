import os
import json
import traceback
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluation_chain
from src.mcqgenerator.logger import logging