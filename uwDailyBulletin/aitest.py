import os
from dotenv import load_dotenv
from openai import OpenAI
from v1 import get_latest_post
from sentence_transformers import SentenceTransformer, util, CrossEncoder

load_dotenv()

chatgptkey = os.getenv("CHATGPTKEY")
client = OpenAI(api_key=chatgptkey)

model = CrossEncoder("cross-encoder/stsb-distilroberta-base")
model2 = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1')
prompt = str(get_latest_post())

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

queryEmbeddings = model2.encode(sentences)

print(queryEmbeddings)

response = client.responses.create(
    model="gpt-4.1-mini",
    input="What model is best to call with an api key for a notificatio service that is parsed by chatgpt to send to only the appriopriate users"
)
#doesn't save context
#do i need it to save context? 

print(response.output_text)













