import os
from dotenv import load_dotenv
import google.genai as genai
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
import pytz
from datetime import datetime

current_date=datetime.now().strftime("%B %d, %Y")
print(current_date)

api = load_dotenv()

api_keys = os.environ.get("GEMINI_API_KEY","not set")
print(f"Using key starting with: {api_keys[:8]}...")


def run_researcher(topic:str) -> str:
    
    """Run the research crew and return the final summary."""
    
    #---This run every time a user asks a question----
    local_tz = pytz.timezone('Asia/Singapore')
    current_date=datetime.now(local_tz).strftime("%B %d, %Y")
    print(f"DEBUG: current_date_singapore = {current_date}")
    
    # Initialize the search tool (reads SERPER_API_KEY from environment)
    search_tool = SerperDevTool(n_results=20)
    
    
    print(f"GEMINI_API_KEY present: {bool(os.getenv('GEMINI_API_KEY'))}")
    print(f"SERPER_API_KEY present: {bool(os.getenv('SERPER_API_KEY'))}")
    
    # Configure Gemini LLM with web search enabled
    #gemini_llm = LLM(
    #    #model="gemini-3.1-flash-lite-preview",
    #    model="openai/gemini-3.1-flash-lite-preview",
    #    #model="gemini/gemini-2.0-flash",
    #    #model="gemini/gemini-3-flash-preview",
    #    #model="gemini/gemini-3.1-flash-lite-preview",
    #    #model="gemini/gemini-3-flash-preview",
    #    #model="gemini-3.1-pro-preview",
    #    api_key=os.getenv("GEMINI_API_KEY"),
    #    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    #    temperature=0.7
    #)
    
    #local_llm = LLM(
    #model="ollama/llama3.2:3b",  # or "ollama/llama3.2", "ollama/qwen2.5", etc.
    #base_url="http://localhost:11434",  # Ollama's default address[citation:10]
    #temperature=0.7
    #)
    
    # Backend Selection
    
    llm_backend = os.getenv("LLM_BACKEND","gemini")
    
    # Use your self-hosted Ollama (DeepSeek or other model)
    if llm_backend == "ollama":
        
        # This line reads the value of the environment variable named OLLAMA_BASE_URL. 
        # If that variable exists, it assigns its value to ollama_base. 
        # If the variable does not exist, it assigns the fallback string "http://ollama.railway.internal:11434" instead.
        ollama_base = os.getenv("OLLAMA_BASE_URL","http://ollama.railway.internal:11434") 
        llm = LLM( 
            #model="ollama/deepseek-r1:1.5b",   # Change to whatever model you pulled
            #model="ollama/llama3.2:3b",   # Change to whatever model you pulled
            #model="ollama/qwen2.5-coder:1.5b",
            model="ollama/qwen2.5:3b",
            base_url=ollama_base,
            temperature=0.7,
            #verbose = True
            )
    else:
        
        # Use Gemini (original configuration)
        llm = LLM(
            model="openai/gemini-3.1-flash-lite-preview",
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            temperature=0.7
            )
       
     
    
    researcher = Agent(
        role="Senior Researcher",
        
        goal=f"""Find comprehensive and UP-TO-DATE information about {topic}. Today's date is {current_date}.You MUST use `SerperDevTool` to find the latest news, facts, and developments.
        When using 'SerperDevTool' you must include the current year (2026) in your search query to get the latest update.
        
        Use the search tool and ONLY report facts that has already happened. If a search result mentions a future date (like May 2026), ignore it.
        
        """,
        
        backstory=f"""Today is {current_date}.You are an expert researcher with access to a powerful web search tool. Your internal knowledge is outdated (cutoff January 2025).
        ALWAYS use the `SerperDevTool` to find the latest news and facts.
        You NEVER report events that are in the future. You only list facts with sources that are from today or earlier.""",
        
        
        
        llm=llm,
        tools=[search_tool], #This gives the agent web search ability
        verbose=True
    )
    
    writer = Agent(
        role="Content Writer",
        goal="Write a clear,simple to understand structured detail of the research. Aim for a length of at least 500 words",
        backstory="You turn research into engaging content. Only use the information provided by the researcher.",
        llm=llm,
        verbose=True
    )
    
    research_task = Task(
        description=f"""Research the topic '{topic}' thoroughly using the `SerperDevTool` tool.
        Today's date is {current_date}. Your search queries MUST include the current year (2026), but you must ignore any results that mention a date after today.
        Provide a bulleted list of facts with sources, only including fatcs that has already occurred.""",
       
        #Provide a bulleted list of key facts with sources. For any information after Jan 2025, cite your web sources.""",
        #description="Find the most recent news and developement",
        agent=researcher,
        expected_output="Bulleted list of facts with sources, all from today or earlier."
    )
        
    
    write_task = Task(
        description="Write a well-organized research. Use headings and paragraphs.Aim for a detailed, expansive article (500+ words). Use the information from the research only; do not invent data.",
        agent=writer,
        context=[research_task],
        expected_output="A markdown document with a title, sections, and key takeaways", 
        )
    
    
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
        memory=False,
        max_iter=10,
        max_time = 180
    )

    result = crew.kickoff(inputs={"topic": topic})
    
    # --- DEBUG: Print the researcher's raw output ---
    print("\n" + "="*60)
    print("RESEARCHER RAW OUTPUT (should contain search results)")
    print("="*60)
    print(result.tasks_output[0].raw)   # researcher's output
    print("\n" + "="*60)
    print("WRITER RAW OUTPUT (final answer)")
    print("="*60)
    print(result.raw)                   # writer's output
    print("="*60)

    return result.raw