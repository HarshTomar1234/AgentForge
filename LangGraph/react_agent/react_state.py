import operator
from typing import Annotated, TypedDict, Union, List, Tuple

from langchain_core.agents import AgentAction, AgentFinish

"""

## **1. `AgentAction`**

**Purpose:** Represents a **single step** taken by an agent during execution.

When an agent decides it needs to use a **tool** or perform an **intermediate action** before returning the final answer, LangChain encapsulates this decision in an `AgentAction` object.

### **Definition**

```python
from langchain_core.agents import AgentAction

class AgentAction:
    tool: str            # The name of the tool the agent wants to use
    tool_input: Any      # The input that will be passed to the tool
    log: str             # Log of the reasoning/thought process for debugging
```

### **Key Points**

* Returned when the agent **hasn't finished yet** and needs to **use a tool**.
* The agent will pause, execute the specified tool with `tool_input`, and then continue.
* Used internally by LangChain’s executor to manage multi-step reasoning.

### **Example**

```python
from langchain_core.agents import AgentAction

action = AgentAction(
    tool="Calculator",
    tool_input="2 + 2",
    log="I will use the calculator to find the sum."
)

print(action.tool)        # Calculator
print(action.tool_input)  # 2 + 2
print(action.log)         # I will use the calculator to find the sum.
```

---

## **2. `AgentFinish`**

**Purpose:** Represents the **final output** of the agent when it has completed its reasoning.

When the agent decides it has enough information and doesn't need any more tools, it returns an **`AgentFinish`** object instead of an `AgentAction`.

### **Definition**

```python
from langchain_core.agents import AgentFinish

class AgentFinish:
    return_values: dict   # The final answer(s) produced by the agent
    log: str             # Log of reasoning steps leading to the finish
```

### **Key Points**

* Returned **at the end** of the agent’s reasoning.
* The `return_values` dictionary usually contains the **final answer**.
* Marks the completion of the agent’s run.

### **Example**

```python
from langchain_core.agents import AgentFinish

finish = AgentFinish(
    return_values={"output": "The sum of 2 + 2 is 4."},
    log="I calculated the result using the calculator tool."
)

print(finish.return_values["output"])  
# The sum of 2 + 2 is 4.
print(finish.log)  
# I calculated the result using the calculator tool.
```

---

## **3. Workflow Together**

LangChain agents alternate between **`AgentAction`** and **`AgentFinish`**:

1. **Agent** thinks about the problem.
2. Decides to use a **tool** → returns **`AgentAction`**.
3. Tool is executed, result comes back.
4. Agent processes result:

   * If more tools are needed → returns another **`AgentAction`**.
   * If it’s done → returns **`AgentFinish`**.

### **Illustrative Example**

```python
# Step 1 → Agent wants to use a tool
AgentAction(
    tool="Calculator",
    tool_input="2 + 2",
    log="Need to calculate 2 + 2."
)

# Step 2 → Tool gives result = 4

# Step 3 → Agent has enough info → finishes
AgentFinish(
    return_values={"output": "The sum of 2 + 2 is 4."},
    log="Calculation done, final answer prepared."
)
```

---

## **4. When You’ll Encounter Them**

* When **writing custom agents**.
* When **debugging** LangChain’s reasoning.
* When building **multi-step AI workflows** using tools.
* When using frameworks like **CrewAI** or **LangGraph**, which often wrap around these primitives.

---

## **Summary Table**

| **Aspect**   | **AgentAction**                        | **AgentFinish**                         |
| ------------ | -------------------------------------- | --------------------------------------- |
| **Purpose**  | Represents an **intermediate step**    | Represents the **final answer**         |
| **Triggers** | When the agent wants to use a **tool** | When the agent has the **final result** |
| **Contains** | `tool`, `tool_input`, `log`            | `return_values`, `log`                  |
| **Used in**  | Multi-step reasoning                   | Returning the final output              |

"""

class AgentState(TypedDict):
    input: str
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]