import csv
import os
import time
import concurrent.futures
import pandas as pd
from multiprocessing import cpu_count
import concurrent.futures
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
from rdflib import Graph, Literal, Namespace, URIRef, BNode
from rdflib.namespace import RDF, XSD
import threading
import requests