#hybrid search pipeline

import os
import json
import torch
import string
import numpy as np

from dotenv import load_dotenv
from openai import OpenAI
from v1 import get_latest_post
from sentence_transformers import SentenceTransformer, CrossEncoder #util
from sentence_transformers.util import http_get, semantic_search

from rank_bm25 import BM25Okapi
#Matches on overlapepd keywords not semantic similarity
#Sort of a double check after the encoders (encoders might miss acronyms/course codes etc)
from sklearn.feature_extraction import _stop_words
from tqdm.autonotebook import tqdm
#porgress bar library

print("CUDA available:", torch.cuda.is_available())

if not torch.cuda.is_available(): #forgot how to set this, does it have to be in a notebook to set?
    print("CUDA is not available. Using CPU instead.")
    raise SystemError("Error for now")

#make a huggingface account for faster & avoid limits
#is there a faster way to load weights and just store them?

load_dotenv()

chatgptkey = os.getenv("CHATGPTKEY")
client = OpenAI(api_key=chatgptkey)


bi_encoder = SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
bi_encoder.max_seq_length = 256 #truncates if too long
#top_k
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

#model = CrossEncoder("cross-encoder/stsb-distilroberta-base")
#model2 = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1')

prompt = get_latest_post()

#prob not the most efficent flow
def promptCleaner(prompt):
    prompt2 = []
    for tokens in prompt.lower().split():
        tokens += tokens.strip(string.punctuation)
        if len(tokens) > 0 and tokens not in _stop_words.ENGLISH_STOP_WORDS: #filters out common words like (the, is, and, etc)
            prompt2.append(tokens)
    return prompt2


#parse v1.py into prompt
sentences = [ #ai generated rn
    "I'm a second-year CS major really into machine learning and open-source. Notify me about hackathons, ML research talks on campus, and any internships at startups.",
    "Pre-med, sophomore. I want reminders about MCAT prep workshops, volunteering opportunities at hospitals, and scholarship deadlines.",
    "Hey, I just want to know when there's free food on campus lol. Also club fairs.",
    "Final-year mechanical engineering student looking for full-time roles in automotive or aerospace. Career fairs, recruiter info sessions, resume workshops please.",
    "I love theater and music. Tell me about auditions, open mic nights, and student-run productions.",
    "International student, first semester. I need info about visa workshops, ESL resources, and events to meet other people. Kind of nervous about everything tbh.",
    "Econ + Stats double major. Interested in quant finance, data science competitions, and any guest lectures from people in industry.",
    "Varsity swimmer. Mostly want notifications about athletics schedule changes, sports medicine clinics, and academic tutoring that works around training.",
    "Art history grad student. Museum trips, gallery openings, fellowship and grant deadlines, conference CFPs.",
    "Honestly not sure what I want to do yet. I'm a freshman exploring everything — send me a bit of everything: clubs, events, free workshops, whatever.",
    "Nursing student, night classes. Please only notify me about things on weekends or evenings. Health-related stuff and study groups.",
    "I'm into climate activism and sustainability. Protests, environmental club meetings, green-tech speakers, volunteer cleanups.",
    "Comp sci senior graduating in May — URGENT job leads only, please. No events, no clubs, just internships/full-time and networking.",
    "Psychology major interested in research. Want to hear about labs recruiting RAs, psych study participation (paid is a bonus), and stats workshops.",
    "Transfer student, just got here. Campus orientation events, where to find resources, commuter student groups.",
    "",
    "everything",
    "I want notifications about basketball, cooking, Spanish conversation practice, robotics, poetry, entrepreneurship, and astronomy.",
    "asdfjkl test test",
    "I'm interested in cybersecurity but NOT in anything involving public speaking or large group events."
]

corpus_embeddings = bi_encoder.encode(sentences, convert_to_tensor=True, show_progress_bar=True)
#am i supposed to include the prompt here?

tokenized_corpus = [] 
for passage in tqdm(sentences):
    tokenized_corpus.append(promptCleaner(passage))
bm25 = BM25Okapi(tokenized_corpus)

print(bm25)


def search(query, top_k=10):
    print("Input question:", query)

    ##### BM25 search (lexical search) #####
    bm25_scores = bm25.get_scores(promptCleaner(query))
    top_n = np.argpartition(bm25_scores, -5)[-5:]
    bm25_hits = [{"corpus_id": idx, "score": bm25_scores[idx]} for idx in top_n]
    bm25_hits = sorted(bm25_hits, key=lambda x: x["score"], reverse=True)

    print("Top-3 lexical search (BM25) hits")
    for hit in bm25_hits[0:3]:
        print("\t{:.3f}\t{}".format(hit["score"], sentences[hit["corpus_id"]].replace("\n", " ")))

    ##### Semantic Search #####
    # Encode the query using the bi-encoder and find potentially relevant sentences
    question_embedding = bi_encoder.encode(query, convert_to_tensor=True)
    question_embedding = question_embedding.cuda()
    hits = semantic_search(question_embedding, corpus_embeddings, top_k=top_k)
    hits = hits[0]  # Get the hits for the first (and only) query

    ##### Re-Ranking #####
    # Score all retrieved sentences with the cross_encoder
    cross_inp = [[query, sentences[hit["corpus_id"]]] for hit in hits]
    cross_scores = cross_encoder.predict(cross_inp)

    for idx in range(len(cross_scores)):
        hits[idx]["cross-score"] = cross_scores[idx]

    print("\n-------------------------\n")
    print("Top-3 Bi-Encoder Retrieval hits")
    hits = sorted(hits, key=lambda x: x["score"], reverse=True)
    for hit in hits[0:3]:
        print("\t{:.3f}\t{}".format(hit["score"], sentences[hit["corpus_id"]].replace("\n", " ")))

    print("\n-------------------------\n")
    print("Top-3 Cross-Encoder Re-ranker hits")
    hits = sorted(hits, key=lambda x: x["cross-score"], reverse=True)
    for hit in hits[0:3]:
        print("\t{:.3f}\t{}".format(hit["cross-score"], sentences[hit["corpus_id"]].replace("\n", " ")))

    return hits


search(prompt)


#queryEmbeddings = cross_encoder.encode(sentences)
#idealy store them somewhere so it doesn't retoggle every time, some sort of db


#similarities = model2.similarity(queryEmbeddings, model2.encode([prompt]))
#am i first storing their similarities to each other? or just always compare to prompt

""" response = client.responses.create(
    model="gpt-4.1-mini",
    input=""
) """
#doesn't save context
#do i need it to save context? 















