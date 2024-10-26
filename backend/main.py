from fastapi import FastAPI, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENALEX_BASE_URL = "https://api.openalex.org/authors"
SEMANTIC_SCHOLAR_BASE_URL = "https://api.semanticscholar.org/graph/v1/author/search"

professor_list = [
    "Michael I. Jordan", "Andrew Ng", "Geoffrey Hinton", "Yoshua Bengio", 
    "Jürgen Schmidhuber", "Hideo Inaba", "Ali H. Sayed", "Martin Abadi", 
    "John A. Rogers", "Carlo Ratti", "Ronald C. Kessler", "Shing-Tung Yau", 
    "David Patterson", "Gérard Berry", "John Ioannidis"
]

async def fetch_professor_data(name: str):
    async with httpx.AsyncClient() as client:
        try:
            # Fetch data from OpenAlex
            response_openalex = await client.get(
                OPENALEX_BASE_URL,
                params={"filter": f"display_name.search:{name}"}
            )
            if response_openalex.status_code == 200 and response_openalex.json().get("results"):
                first_result = response_openalex.json()["results"][0]
                citation_count = first_result.get("cited_by_count", "Not Available")
                publication_count = first_result.get("works_count", "Not Available")
                display_name = first_result["display_name"]

                # Fetch author image from Semantic Scholar
                response_semanticscholar = await client.get(
                    SEMANTIC_SCHOLAR_BASE_URL,
                    params={"query": name, "fields": "url"}
                )
                image_url = None
                if response_semanticscholar.status_code == 200:
                    results = response_semanticscholar.json().get("data")
                    if results:
                        image_url = results[0].get("url")

                return {
                    "name": display_name,
                    "citation_count": citation_count,
                    "publication_count": publication_count,
                    "image_url": image_url or "Image Not Available"
                }
        except Exception as e:
            print(f"Error fetching data for {name}: {e}")
        return None  # Return None if there was an error

async def get_all_professor_data():
    tasks = [fetch_professor_data(professor) for professor in professor_list]
    return await asyncio.gather(*tasks)

@app.get("/professors-data")
async def get_professors_data():
    data = await get_all_professor_data()
    return [professor for professor in data if professor is not None]

@app.get("/professor-data/{professor_name}")
async def get_professor_data_endpoint(professor_name: str):
    professor_data = await fetch_professor_data(professor_name)
    if professor_data:
        return professor_data
    else:
        raise HTTPException(status_code=404, detail="Professor not found")
