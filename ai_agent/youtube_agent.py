from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.schema import AgentAction, AgentFinish
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Ollama
from typing import List, Union
import re

# Import custom tools
from ai_agent.tools import YouTubeSearchTool

# Set up the YouTube search tool
youtube_tool = YouTubeSearchTool()

tools = [
    Tool(
        name="YouTube Search",
        func=youtube_tool.search,
        description="Useful for searching YouTube videos based on a query."
    )
]

# Updated template to encourage single-iteration search
template = """
You are a helpful AI assistant that finds the most relevant YouTube video based on the user's query.

Use the following tools to find the best video:

{tools}

Use the following format:

Query: the user's query
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
Thought: I now know the final answer
Final Answer: the best matching YouTube video is [video title] with link [video link].

Query: {query}
Thought: {agent_scratchpad}
"""

class CustomPromptTemplate(StringPromptTemplate):
    template: str
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps", [])
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\n"
        kwargs["agent_scratchpad"] = thoughts
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)

class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent has finished
        if "Final Answer:" in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output
            )
        
        # Parse the output for agent actions
        regex = r"Action:\s*(.*?)\n.*?Action Input:\s*(.*?)(?=\n|$)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        
        action = match.group(1).strip()
        action_input = match.group(2).strip()
        
        return AgentAction(
            tool=action,
            tool_input=action_input,
            log=llm_output
        )

# Create prompt
prompt = CustomPromptTemplate(
    template=template,
    tools=tools,
    input_variables=["query", "intermediate_steps"]
)

# Set up the Ollama LLM
llm = Ollama(model="codellama:latest")

# Set up the agent
llm_chain = LLMChain(llm=llm, prompt=prompt)
tool_names = [tool.name for tool in tools]
agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=CustomOutputParser(),
    stop=["\nObservation:"],
    allowed_tools=tool_names
)

# Create agent executor with max iterations
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, 
    tools=tools, 
    verbose=True,
    max_iterations=1  # Limit to one search iteration
)

def run_agent(query):
    return agent_executor.run(query)