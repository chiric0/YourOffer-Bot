import asyncio
import json
import os
import sys
from io import BytesIO

import fitz
import redis
import requests
import telebot
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt
from telebot import types