import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Xavier A P | MLOps Engineer")

# === VERCEL-PROOF PATHING ===
# This ensures Vercel can always find your static files and templates, 
# regardless of where it spins up the serverless function.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

PROJECTS = [
    {
        "id": "pack-vote",
        "title": "Pack Vote",
        "tagline": "Agentic multi-LLM travel planner",
        "metrics": ["98% Latency ↓", "60% Cost ↓"],
        "tech": ["FastAPI", "Redis", "Twilio", "MLflow"],
        "github": "https://github.com/XAVIER-A-P/Pack-Vote--Agentic-AI-Travel-Planner",
        "deployment": "https://packvote.xaviermlops.dev",
        "summary": {
            "reason": "Standard LLM APIs were too slow for synchronous, real-time group voting.",
            "details": "Built a multi-model gateway with ranked-choice voting and SMS via Twilio. Orchestrated model tracking and evaluation via custom Python and MLflow.",
            "achievements": "Cut latency by 98% and optimized token usage for a 60% cost drop.",
            "challenges": "Handling rate limits and race conditions during concurrent agent interactions."
        },
        "production": "Implemented Redis caching for frequent queries and circuit breakers for external API validation.",
        
        # ========================================== #
        # PASTE PACK VOTE MERMAID SYNTAX BELOW       #
        # ========================================== #
        "mermaid": """
graph TD
    User[User Frontend] -->|HTTP/WebSocket| API[FastAPI Backend]
    API --> Gateway[AI Model Gateway]
    API --> Voting[Voting Engine]
    
    subgraph "Agentic Layer"
    Gateway -->|Router| OpenAI[OpenAI GPT-4o]
    Gateway -->|Router| Anthropic[Claude 3.5]
    Gateway -->|Tool Call| Tools[Pricing Tool]
    Tools -->|API Request| Amadeus[Amadeus Flight API]
    Tools -.->|Cache Hit/Miss| Redis[(Redis Cache)]
    end
    
    subgraph "Data Layer"
    API --> DB[(PostgreSQL)]
    end

        """
    },
    {
        "id": "banana-death",
        "title": "Days to Banana Death",
        "tagline": "Computer vision regression pipeline",
        "metrics": ["Real-time Inference", "Automated CI/CD"],
        "tech": ["TensorFlow", "FastAPI", "Render", "Computer Vision"],
        "github": "https://github.com/XAVIER-A-P/Days-To-Banana-Death",
        "deployment": "https://bananadeath.xaviermlops.dev",
        "summary": {
            "reason": "Needed a lightweight, end-to-end CV pipeline to predict fruit ripeness on edge devices.",
            "details": "Trained a regression model using TensorFlow, wrapped in a FastAPI backend with deep check data validation.",
            "achievements": "Deployed a fully automated inference loop capable of 30fps processing on CPU.",
            "challenges": "Quantizing the model to run efficiently without requiring heavy GPU instances."
        },
        "production": "Configured automated CI/CD pipelines via GitHub Actions and established a production feedback loop using S3.",
        
        # ========================================== #
        # PASTE BANANA DEATH MERMAID SYNTAX BELOW    #
        # ========================================== #
        "mermaid": """
        graph LR;
            Camera-->FastAPI;
            FastAPI-->Model[TF Lite Model];
            Model-->Prediction;
            Prediction-->UI;
        """
    },
    {
        "id": "shelf-scanner",
        "title": "Shelf-Scanner",
        "tagline": "Automated inventory tracking via edge computer vision",
        "metrics": ["99.9% Uptime", "Edge Deployment"],
        "tech": ["Python", "OpenCV", "Docker", "Prometheus"],
        "github": "https://github.com/XAVIER-A-P/Shelf-Scanner",
        "deployment": "https://shelfscanner.xaviermlops.dev",
        "summary": {
            "reason": "Manual inventory auditing is error-prone and slow; required an automated optical solution.",
            "details": "Developed an object detection pipeline deployed via Docker containers to edge devices.",
            "achievements": "Achieved continuous scanning with 99.9% availability.",
            "challenges": "Managing container lifecycle and logging on remote, resource-constrained edge hardware."
        },
        "production": "Fully containerized deployment with Prometheus endpoints for real-time memory and CPU monitoring.",
        
        # ========================================== #
        # PASTE SHELF-SCANNER MERMAID SYNTAX BELOW   #
        # ========================================== #
        "mermaid": """
graph TD
    Client[Mobile Browser / HTMX] -->|POST /scan-ui| FastAPI[FastAPI Server]
    FastAPI -->|1. Upload Image| S3[(AWS S3)]
    FastAPI -->|2. Check IP Limit| Redis[(Redis Cache)]
    
    FastAPI -->|3A. Primary Vision| GPT4[GPT-4o Vision]
    GPT4 -- Success --> RecEngine[Recommendation Engine]
    GPT4 -- Timeout/Error --> Fallback[Google Vision OCR]
    Fallback --> Cleanup[GPT-3.5 Text Cleanup]
    Cleanup --> RecEngine
    
    RecEngine -->|4. Generate Scores| GPT3[GPT-3.5-Turbo]
    GPT3 --> FastAPI
    
    FastAPI -->|5. Save History| DB[(PostgreSQL)]
    FastAPI -->|6. Render Partial| Client
    
        """
    }
]

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "projects": PROJECTS[:3]})

@app.get("/projects")
async def projects(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request, "projects": PROJECTS})

# 1. This route serves the main blog page (the list of articles)
@app.get("/blog")
async def blog(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request})

# 2. This route serves the individual blog posts based on the URL clicked
@app.get("/blog/{slug}")
async def read_post(request: Request, slug: str):
    # This automatically looks for the matching HTML file in the templates/posts/ folder
    template_name = f"posts/{slug}.html"
    template_path = os.path.join(BASE_DIR, "templates", template_name)
    
    # Safety check: if the file doesn't exist, return a 404 error
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Blog post not found")
        
    # Optional: Dictionary mapping slugs to titles if you want to pass them to the template
    post_titles = {
        "llm-latency-reduction": "How I Reduced LLM Latency by 98%",
        "multimodal-pipelines": "Designing Fault-Tolerant Multimodal Pipelines",
        "mitigating-hallucinations": "Mitigating Hallucinations Using External API Validation",
        "mobilenetv2-cpu": "Choosing MobileNetV2 Over ResNet for CPU Inference"
    }
    title = post_titles.get(slug, "Technical Blog Post")
        
    return templates.TemplateResponse(template_name, {"request": request, "title": title})

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})