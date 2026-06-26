# =============================================================
# MCP CAPSTONE — Part 2: Insurance MCP Client + Qwen Agent
# =============================================================
 
import asyncio
import json
import os
import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
 
console = Console()
 
OLLAMA_URL  = "http://localhost:11434/api/chat"
MODEL_NAME  = "qwen2.5:3b"
SERVER_PATH = os.path.join(os.path.dirname(__file__), "insurance_server.py")
 
 
# =============================================================
# SECTION 1: QWEN VIA OLLAMA
# =============================================================
 
def call_qwen(prompt: str) -> str:
    """Send a prompt to Qwen via Ollama's REST API."""
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    try:
        response = httpx.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except httpx.ConnectError:
        return "ERROR: Cannot connect to Ollama. Is it running? Try: ollama serve"
    except Exception as e:
        return f"ERROR: {e}"
 
 
# =============================================================
# SECTION 2: REAL MCP TOOL DISCOVERY
# =============================================================
 
async def discover_tools(session: ClientSession) -> dict:
    """
    Call session.list_tools() — the real MCP tools/list request.
    Returns a dict of {tool_name: tool_description} for the LLM prompt.
    """
    tools_result = await session.list_tools()
    tool_map = {}
    for tool in tools_result.tools:
        tool_map[tool.name] = tool.description or "No description"
    return tool_map
 
 
# =============================================================
# SECTION 3: QWEN DECIDES WHICH TOOLS TO CALL
# =============================================================
def decide_tools(query: str, available_tools: dict) -> list:
 
    tools_description = "\n".join(
        f"{i+1}. {name}: {desc}"
        for i, (name, desc) in enumerate(available_tools.items())
    )
 
    prompt = f"""
You are an insurance assistant.
 
Available tools:
 
{tools_description}
 
Available customer IDs:
C001, C002, C003
 
Available policy IDs:
P1001, P1002, P1003
 
Available claim IDs:
CL001, CL002, CL003, CL004
 
User Query:
{query}
 
IMPORTANT:
- Return ONLY JSON
- No markdown
- No explanation
- Always return a JSON array
 
Example:
 
[
  {{
    "tool": "get_claim_status",
    "input": {{
      "claim_id": "CL001"
    }}
  }}
]
"""
 
    raw = call_qwen(prompt)
 
    console.print("\n[cyan]RAW QWEN RESPONSE:[/cyan]")
    console.print(raw)
 
    cleaned = (
        raw.strip()
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )
 
    try:
        result = json.loads(cleaned)
 
        if isinstance(result, dict):
            result = [result]
 
        if not isinstance(result, list):
            return []
 
        valid_calls = []
 
        for item in result:
            if isinstance(item, dict):
                valid_calls.append(item)
 
        return valid_calls
 
    except Exception as e:
        console.print(f"[red]JSON Parse Error:[/red] {e}")
        console.print(f"[yellow]Response:[/yellow] {cleaned}")
        return []
 
# =============================================================
# SECTION 4: REAL MCP TOOL CALLS via session.call_tool()
# =============================================================
 
async def execute_tools_via_mcp(
    session: ClientSession,
    tool_calls: list
) -> list:
 
    results = []
 
    for call in tool_calls:
 
        if not isinstance(call, dict):
            console.print(
                f"[red]Skipping invalid tool call:[/red] {call}"
            )
            continue
 
        tool_name = call.get("tool", "")
        tool_input = call.get("input", {})
 
        if not tool_name:
            console.print("[red]Missing tool name[/red]")
            continue
 
        console.print(
            f"[blue]MCP call_tool({tool_name}, {tool_input})[/blue]"
        )
 
        try:
 
            result = await session.call_tool(
                tool_name,
                arguments=tool_input
            )
 
            texts = []
 
            if hasattr(result, "content"):
 
                for item in result.content:
 
                    if hasattr(item, "text"):
                        texts.append(item.text)
 
            output_text = (
                " ".join(texts)
                if texts
                else "(empty result)"
            )
 
            console.print(
                f"[green]Result:[/green] {output_text}"
            )
 
            results.append(
                {
                    "tool": tool_name,
                    "input": tool_input,
                    "output": output_text
                }
            )
 
        except Exception as e:
 
            console.print(
                f"[red]Tool Error:[/red] {e}"
            )
 
            results.append(
                {
                    "tool": tool_name,
                    "input": tool_input,
                    "error": str(e)
                }
            )
 
    return results
 
 
# =============================================================
# SECTION 5: SYNTHESIZE FINAL ANSWER
# =============================================================
 
def synthesize_answer(query: str, tool_results: list) -> str:
    """Ask Qwen to form a natural language answer from the MCP tool results."""
    results_text = json.dumps(tool_results, indent=2)
 
    prompt = f"""Original question: {query}
 
Real data retrieved via MCP tools:
{results_text}
 
Write a clear, professional answer for the customer using this real data.
Include specific numbers and statuses. Keep to 2-4 sentences.
Do not mention MCP, tools, or JSON — just answer naturally.
"""
    return call_qwen(prompt)
 
 
# =============================================================
# SECTION 6: MAIN AGENT PIPELINE
# =============================================================
 
async def run_insurance_agent(queries: list):
    """
    Full pipeline using a REAL MCP connection:
      1. Launch insurance_server.py as a subprocess
      2. Connect via stdio_client + ClientSession
      3. initialize() -> real MCP handshake
      4. list_tools() -> real tool discovery
      5. For each query: Qwen decides tools -> call_tool() -> synthesize
    """
    server_params = StdioServerParameters(
        command="python",
        args=[SERVER_PATH],
    )
 
    console.print("[cyan]Launching MCP server and connecting...[/cyan]")
 
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
 
            # Real MCP initialize handshake
            await session.initialize()
            console.print("[green]MCP handshake complete (initialize)[/green]")
 
            # Real MCP tools/list discovery
            available_tools = await discover_tools(session)
            console.print(f"[green]Tools discovered (list_tools): {list(available_tools.keys())}[/green]\n")
 
            # Show discovered tools table
            table = Table(title="Discovered Tools from MCP Server", style="bold")
            table.add_column("Tool",        style="cyan",  width=22)
            table.add_column("Description", style="white", width=55)
            for name, desc in available_tools.items():
                table.add_row(name, desc[:55] if desc else "-")
            console.print(table)
            console.print()
 
            # Process each query through the full MCP pipeline
            for query in queries:
                console.print(f"\n[bold white]Customer Query:[/bold white] {query}")
                console.print("[cyan]Qwen selecting tools...[/cyan]")
 
                tool_calls = decide_tools(query, available_tools)
 
                console.print("\n[yellow]Parsed Tool Calls:[/yellow]")
                console.print(tool_calls)
                console.print(type(tool_calls))
 
                if not tool_calls:
                    answer = call_qwen(query)
                    console.print(Panel(answer,
                        title="[bold green]Answer (direct)[/bold green]",
                        border_style="green"))
                    continue
 
                console.print(f"[cyan]Calling {len(tool_calls)} tool(s) via MCP...[/cyan]")
                tool_results = await execute_tools_via_mcp(session, tool_calls)
 
                answer = synthesize_answer(query, tool_results)
                console.print(Panel(answer,
                    title="[bold green]Answer[/bold green]",
                    border_style="green"))
 
 
# =============================================================
# SECTION 7: RUN
# =============================================================
 
DEMO_QUERIES = [
    "What is the status of claim CL001?",
    "Is there any fraud risk on claim CL003?",
    "How much premium does customer C001 owe?",
    "Show me the details for policy P1002",
    "Please renew policy P1003",
    "Tell me about customer C002 and their policy",
    "Run a fraud check on claim CL002 and show me the claim status too",
]
 
if __name__ == "__main__":
    console.print("\n[bold magenta]=== MCP INSURANCE CAPSTONE ===[/bold magenta]")
    console.print("[dim]Real MCP protocol: stdio_client + ClientSession + call_tool[/dim]\n")
 
    # Verify Ollama before starting the async MCP pipeline
    test = call_qwen("Say OK in one word")
    if "ERROR" in test:
        console.print(Panel(test,
            title="[bold red]Ollama Connection Failed[/bold red]",
            border_style="red"))
        console.print("Make sure Ollama is running: ollama serve")
        console.print("And model is pulled: ollama pull qwen2.5:3b")
        exit(1)
 
    console.print("[green]Ollama connected[/green]")
    asyncio.run(run_insurance_agent(DEMO_QUERIES))
    console.print("\n[bold yellow]=== Capstone Complete ===[/bold yellow]")
 