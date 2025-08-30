"""
LLM Autonomy Levels - Practical Code Examples
This file demonstrates each autonomy level with working code examples.
"""

import datetime
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# LEVEL 0: DIRECT CODE (0% Autonomy)
# ============================================================================

class Level0_DirectCode:
    """Pure deterministic code without LLM involvement"""
    
    @staticmethod
    def calculator(operation: str, a: float, b: float) -> float:
        """Simple calculator with fixed operations"""
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            if b != 0:
                return a / b
            else:
                raise ValueError("Cannot divide by zero")
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    @staticmethod
    def weather_lookup(city: str) -> str:
        """Fixed weather responses"""
        weather_data = {
            "new york": "Sunny, 72°F",
            "london": "Cloudy, 15°C",
            "tokyo": "Rainy, 20°C"
        }
        return weather_data.get(city.lower(), "Weather data not available")

# Example usage:
# result = Level0_DirectCode.calculator("add", 5, 3)
# weather = Level0_DirectCode.weather_lookup("New York")


# ============================================================================
# LEVEL 1: SINGLE LLM CALL (20% Autonomy)
# ============================================================================

class Level1_SingleLLM:
    """Single LLM call for text generation"""
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    def chat_completion(self, user_message: str) -> str:
        """Simple chat completion"""
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
        response = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content
    
    def code_explanation(self, code: str) -> str:
        """Explain code functionality"""
        prompt = f"""
        Explain what this code does in simple terms:
        
        ```
        {code}
        ```
        """
        return self.chat_completion(prompt)

# Example usage:
# llm_level1 = Level1_SingleLLM(openai_client)
# explanation = llm_level1.code_explanation("def factorial(n): return 1 if n <= 1 else n * factorial(n-1)")


# ============================================================================
# LEVEL 2: CHAINS (40% Autonomy)
# ============================================================================

class Level2_Chains:
    """Sequential chain of operations"""
    
    def __init__(self, llm_client, search_tool):
        self.llm = llm_client
        self.search = search_tool
    
    def research_and_summarize_chain(self, topic: str) -> Dict[str, Any]:
        """Multi-step research and summarization"""
        
        # Step 1: Generate search queries
        query_prompt = f"Generate 3 specific search queries to research '{topic}'. Return only the queries, one per line."
        queries_response = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query_prompt}]
        )
        queries = queries_response.choices[0].message.content.strip().split('\n')
        
        # Step 2: Search for information
        search_results = []
        for query in queries[:3]:  # Limit to 3 queries
            results = self.search.search(query.strip())
            search_results.extend(results)
        
        # Step 3: Analyze and extract key points
        analysis_prompt = f"""
        Analyze these search results about '{topic}' and extract the key points:
        
        {str(search_results)}
        
        Provide a structured analysis with main themes and important details.
        """
        analysis = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": analysis_prompt}]
        )
        
        # Step 4: Create final summary
        summary_prompt = f"""
        Create a comprehensive summary about '{topic}' based on this analysis:
        
        {analysis.choices[0].message.content}
        
        Structure it with:
        1. Overview
        2. Key Points
        3. Current Status
        4. Future Implications
        """
        final_summary = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": summary_prompt}]
        )
        
        return {
            "topic": topic,
            "queries": queries,
            "search_results_count": len(search_results),
            "analysis": analysis.choices[0].message.content,
            "final_summary": final_summary.choices[0].message.content
        }

# Example usage:
# chain = Level2_Chains(openai_client, search_tool)
# result = chain.research_and_summarize_chain("Large Language Models")


# ============================================================================
# LEVEL 3: ROUTERS (60% Autonomy)
# ============================================================================

class QueryType(Enum):
    WEATHER = "weather"
    MATH = "math"
    GENERAL = "general"
    CODE = "code"
    RESEARCH = "research"

class Level3_Router:
    """Router that directs queries to appropriate handlers"""
    
    def __init__(self, llm_client):
        self.llm = llm_client
        self.routes = {
            QueryType.WEATHER: self._handle_weather,
            QueryType.MATH: self._handle_math,
            QueryType.GENERAL: self._handle_general,
            QueryType.CODE: self._handle_code,
            QueryType.RESEARCH: self._handle_research
        }
    
    def route_query(self, user_query: str) -> str:
        """Route query to appropriate handler"""
        
        # Router LLM decides the category
        routing_prompt = f"""
        Classify this user query into one of these categories:
        - weather: Questions about weather, temperature, climate
        - math: Mathematical calculations, equations, problems
        - general: General conversation, simple questions
        - code: Programming, coding, technical implementation
        - research: Complex topics requiring detailed research
        
        Query: "{user_query}"
        
        Respond with only the category name.
        """
        
        response = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": routing_prompt}]
        )
        
        route_decision = response.choices[0].message.content.strip().lower()
        
        # Map to enum
        try:
            query_type = QueryType(route_decision)
        except ValueError:
            query_type = QueryType.GENERAL  # Default fallback
        
        # Execute appropriate handler
        return self.routes[query_type](user_query)
    
    def _handle_weather(self, query: str) -> str:
        """Weather-specific processing"""
        prompt = f"Answer this weather query with current information: {query}"
        return self._llm_call(prompt, "You are a weather expert assistant.")
    
    def _handle_math(self, query: str) -> str:
        """Math-specific processing"""
        prompt = f"Solve this mathematical problem step by step: {query}"
        return self._llm_call(prompt, "You are a mathematics tutor. Show your work clearly.")
    
    def _handle_general(self, query: str) -> str:
        """General conversation"""
        return self._llm_call(query, "You are a helpful, friendly assistant.")
    
    def _handle_code(self, query: str) -> str:
        """Code-specific processing"""
        prompt = f"Help with this coding question: {query}"
        return self._llm_call(prompt, "You are an expert programmer. Provide clear, well-commented code.")
    
    def _handle_research(self, query: str) -> str:
        """Research-specific processing"""
        prompt = f"Research and provide detailed information about: {query}"
        return self._llm_call(prompt, "You are a research assistant. Provide comprehensive, well-structured information.")
    
    def _llm_call(self, user_message: str, system_message: str) -> str:
        """Helper method for LLM calls"""
        response = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content

# Example usage:
# router = Level3_Router(openai_client)
# result = router.route_query("What's the weather like in Paris?")


# ============================================================================
# LEVEL 4: STATE MACHINES / AGENTS (80% Autonomy)
# ============================================================================

@dataclass
class AgentStep:
    action: str
    input: str
    output: str
    timestamp: datetime.datetime

class AgentState:
    def __init__(self, query: str):
        self.original_query = query
        self.steps: List[AgentStep] = []
        self.final_answer: str = None
        self.is_finished = False
        self.iteration_count = 0
        self.max_iterations = 10
    
    def add_step(self, action: str, input_data: str, output: str):
        step = AgentStep(action, input_data, output, datetime.datetime.now())
        self.steps.append(step)
        self.iteration_count += 1
        
        if self.iteration_count >= self.max_iterations:
            self.is_finished = True

class Level4_ReactAgent:
    """ReAct (Reasoning and Acting) Agent with tools"""
    
    def __init__(self, llm_client, tools: Dict[str, callable]):
        self.llm = llm_client
        self.tools = tools
    
    def solve(self, query: str) -> str:
        """Main agent loop"""
        state = AgentState(query)
        
        while not state.is_finished and state.final_answer is None:
            # Agent reasoning step
            next_action = self._plan_next_action(state)
            
            if next_action["action"] == "final_answer":
                state.final_answer = next_action["content"]
                state.is_finished = True
            else:
                # Execute tool
                tool_name = next_action["action"]
                tool_input = next_action["input"]
                
                if tool_name in self.tools:
                    try:
                        tool_output = self.tools[tool_name](tool_input)
                        state.add_step(tool_name, tool_input, str(tool_output))
                    except Exception as e:
                        error_msg = f"Tool error: {str(e)}"
                        state.add_step(tool_name, tool_input, error_msg)
                else:
                    error_msg = f"Unknown tool: {tool_name}"
                    state.add_step("error", tool_input, error_msg)
        
        return state.final_answer or "Could not solve the query within iteration limit."
    
    def _plan_next_action(self, state: AgentState) -> Dict[str, str]:
        """Agent decides next action"""
        
        # Prepare context
        steps_context = ""
        for step in state.steps:
            steps_context += f"Action: {step.action}\nInput: {step.input}\nOutput: {step.output}\n\n"
        
        available_tools = ", ".join(self.tools.keys())
        
        planning_prompt = f"""
        You are an AI agent solving this query: "{state.original_query}"
        
        Available tools: {available_tools}
        
        Previous steps:
        {steps_context}
        
        Think step by step and decide your next action. You can either:
        1. Use a tool: Respond with JSON {{"action": "tool_name", "input": "tool_input"}}
        2. Provide final answer: Respond with JSON {{"action": "final_answer", "content": "your_answer"}}
        
        What is your next action?
        """
        
        response = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": planning_prompt}]
        )
        
        # Parse response (simplified - in production, use proper JSON parsing)
        response_text = response.choices[0].message.content.strip()
        
        # Simple parsing (in production, use robust JSON parsing)
        if "final_answer" in response_text.lower():
            return {"action": "final_answer", "content": response_text}
        else:
            # Extract action and input (simplified)
            return {"action": "search", "input": state.original_query}

# Example tools for the agent
def search_tool(query: str) -> str:
    """Mock search tool"""
    return f"Search results for '{query}': Found relevant information about the topic."

def calculator_tool(expression: str) -> str:
    """Simple calculator tool"""
    try:
        # WARNING: eval is dangerous in production - use safe math parser
        result = eval(expression)
        return str(result)
    except:
        return "Error in calculation"

def time_tool(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Get current time"""
    return datetime.datetime.now().strftime(format_str)

# Example usage:
# agent_tools = {"search": search_tool, "calculator": calculator_tool, "time": time_tool}
# agent = Level4_ReactAgent(openai_client, agent_tools)
# result = agent.solve("What's 15% of 250 and when was this calculated?")


# ============================================================================
# LEVEL 5: AUTONOMOUS AGENTS (95%+ Autonomy)
# ============================================================================

class Goal:
    def __init__(self, description: str, priority: int = 1):
        self.description = description
        self.priority = priority
        self.created_at = datetime.datetime.now()
        self.status = "active"  # active, completed, paused, abandoned
        self.sub_goals: List['Goal'] = []

class LongTermMemory:
    def __init__(self):
        self.experiences: List[Dict] = []
        self.learned_patterns: Dict[str, Any] = {}
    
    def store_experience(self, action: str, context: str, result: str, success: bool):
        experience = {
            "action": action,
            "context": context,
            "result": result,
            "success": success,
            "timestamp": datetime.datetime.now()
        }
        self.experiences.append(experience)
    
    def retrieve_similar_experiences(self, context: str) -> List[Dict]:
        # Simplified similarity matching
        return [exp for exp in self.experiences if context.lower() in exp["context"].lower()]

class Level5_AutonomousAgent:
    """Fully autonomous agent that sets its own goals and plans"""
    
    def __init__(self, llm_client, tools: Dict[str, callable]):
        self.llm = llm_client
        self.tools = tools
        self.goals: List[Goal] = []
        self.memory = LongTermMemory()
        self.running = False
    
    def start(self, initial_objective: str = None):
        """Start autonomous operation"""
        self.running = True
        
        if initial_objective:
            initial_goal = Goal(initial_objective, priority=10)
            self.goals.append(initial_goal)
        
        while self.running and (self.has_active_goals() or self._should_generate_goals()):
            try:
                # Self-assessment
                situation = self._assess_current_situation()
                
                # Goal management
                self._update_goals(situation)
                
                # Planning and execution
                if self.has_active_goals():
                    self._execute_next_action()
                
                # Learning from experience
                self._reflect_and_learn()
                
            except Exception as e:
                print(f"Agent error: {e}")
                # In a real system, implement proper error recovery
    
    def stop(self):
        """Stop autonomous operation"""
        self.running = False
    
    def has_active_goals(self) -> bool:
        return any(goal.status == "active" for goal in self.goals)
    
    def _should_generate_goals(self) -> bool:
        """Decide if new goals should be generated"""
        if not self.goals:
            return True
        
        # Generate new goals if all current goals are completed or few remain
        active_goals = [g for g in self.goals if g.status == "active"]
        return len(active_goals) < 2
    
    def _assess_current_situation(self) -> Dict[str, Any]:
        """Assess current state and environment"""
        return {
            "active_goals": len([g for g in self.goals if g.status == "active"]),
            "completed_goals": len([g for g in self.goals if g.status == "completed"]),
            "recent_experiences": len(self.memory.experiences[-10:]),
            "current_time": datetime.datetime.now()
        }
    
    def _update_goals(self, situation: Dict[str, Any]):
        """Generate new goals or modify existing ones"""
        
        if self._should_generate_goals():
            new_goals = self._generate_new_goals(situation)
            self.goals.extend(new_goals)
    
    def _generate_new_goals(self, situation: Dict[str, Any]) -> List[Goal]:
        """Generate new goals based on current situation"""
        
        goal_generation_prompt = f"""
        You are an autonomous AI agent. Based on your current situation, generate 1-3 new goals.
        
        Current situation:
        - Active goals: {situation['active_goals']}
        - Completed goals: {situation['completed_goals']}
        - Recent experiences: {situation['recent_experiences']}
        
        Your available capabilities: {list(self.tools.keys())}
        
        Generate goals that are:
        1. Specific and actionable
        2. Beneficial for learning or productivity
        3. Achievable with your current tools
        
        Respond with one goal per line.
        """
        
        response = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": goal_generation_prompt}]
        )
        
        goal_descriptions = response.choices[0].message.content.strip().split('\n')
        return [Goal(desc.strip(), priority=5) for desc in goal_descriptions if desc.strip()]
    
    def _execute_next_action(self):
        """Execute the next action toward achieving goals"""
        
        # Select highest priority active goal
        active_goals = [g for g in self.goals if g.status == "active"]
        if not active_goals:
            return
        
        current_goal = max(active_goals, key=lambda g: g.priority)
        
        # Plan action for this goal
        action_plan = self._plan_action_for_goal(current_goal)
        
        # Execute action
        try:
            result = self._execute_action(action_plan)
            self.memory.store_experience(
                action_plan["action"],
                current_goal.description,
                result,
                "success" in result.lower()
            )
            
            # Check if goal is completed
            if self._is_goal_completed(current_goal, result):
                current_goal.status = "completed"
                
        except Exception as e:
            self.memory.store_experience(
                action_plan["action"],
                current_goal.description,
                f"Error: {str(e)}",
                False
            )
    
    def _plan_action_for_goal(self, goal: Goal) -> Dict[str, str]:
        """Plan specific action for a goal"""
        
        similar_experiences = self.memory.retrieve_similar_experiences(goal.description)
        
        planning_prompt = f"""
        Plan the next action to achieve this goal: "{goal.description}"
        
        Available tools: {list(self.tools.keys())}
        
        Similar past experiences:
        {str(similar_experiences[-3:]) if similar_experiences else "None"}
        
        What specific action should be taken next? Respond with:
        {{"action": "tool_name", "input": "specific_input"}}
        """
        
        response = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": planning_prompt}]
        )
        
        # Simplified parsing (use proper JSON parsing in production)
        return {"action": "search", "input": goal.description}
    
    def _execute_action(self, action_plan: Dict[str, str]) -> str:
        """Execute a planned action"""
        
        tool_name = action_plan["action"]
        tool_input = action_plan["input"]
        
        if tool_name in self.tools:
            return self.tools[tool_name](tool_input)
        else:
            return f"Error: Tool '{tool_name}' not available"
    
    def _is_goal_completed(self, goal: Goal, last_result: str) -> bool:
        """Determine if a goal has been completed"""
        
        evaluation_prompt = f"""
        Goal: "{goal.description}"
        Latest result: "{last_result}"
        
        Has this goal been sufficiently completed? Respond with only "YES" or "NO".
        """
        
        response = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": evaluation_prompt}]
        )
        
        return "yes" in response.choices[0].message.content.lower()
    
    def _reflect_and_learn(self):
        """Reflect on recent experiences and update learned patterns"""
        
        recent_experiences = self.memory.experiences[-5:]
        if len(recent_experiences) < 3:
            return
        
        reflection_prompt = f"""
        Reflect on these recent experiences and identify patterns:
        
        {str(recent_experiences)}
        
        What patterns do you notice? What should be remembered for future decisions?
        """
        
        response = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": reflection_prompt}]
        )
        
        # Store insights (simplified)
        self.memory.learned_patterns[f"insight_{datetime.datetime.now()}"] = response.choices[0].message.content

# Example usage:
# autonomous_agent = Level5_AutonomousAgent(openai_client, agent_tools)
# autonomous_agent.start("Learn about machine learning and create a summary")


# ============================================================================
# DEMONSTRATION RUNNER
# ============================================================================

def demonstrate_all_levels():
    """Demonstrate all autonomy levels"""
    
    print("=== LLM AUTONOMY LEVELS DEMONSTRATION ===\n")
    
    # Level 0
    print("LEVEL 0 - Direct Code:")
    calc_result = Level0_DirectCode.calculator("add", 10, 5)
    print(f"Calculator: 10 + 5 = {calc_result}")
    
    weather_result = Level0_DirectCode.weather_lookup("New York")
    print(f"Weather: {weather_result}\n")
    
    # Note: Levels 1-5 require actual LLM client and tools
    print("Levels 1-5 require LLM client setup and API keys.")
    print("See the class implementations above for usage examples.\n")
    
    print("=== AUTONOMY COMPARISON ===")
    levels = [
        ("Level 0", "Direct Code", "0%", "Deterministic logic"),
        ("Level 1", "Single LLM", "20%", "Text generation"),
        ("Level 2", "Chains", "40%", "Sequential processing"),
        ("Level 3", "Routers", "60%", "Dynamic routing"),
        ("Level 4", "Agents", "80%", "Tool usage & reasoning"),
        ("Level 5", "Autonomous", "95%+", "Self-directed goals")
    ]
    
    for level, name, autonomy, description in levels:
        print(f"{level}: {name:<12} | {autonomy:<4} Autonomy | {description}")

if __name__ == "__main__":
    demonstrate_all_levels()
