# *The Dungeon Guardian*

You’re building an intelligent **autonomous NPC agent** called the **Sentient Guardian**, designed to **protect a dungeon** using a combination of:

- **GOAP-style symbolic planning**
- **LLM-based reasoning for decision justification, reflection, and goal generation**

The Sentient Guardian isn’t just reactive — it reasons, plans, and adapts using a simulated **internal monologue** powered by an LLM-style prompt engine (or local heuristic if not using an actual model).

This agent:

- Sets its own goals based on current world state and reflection
- Justifies actions in natural language
- Learns from prior failures or interruptions to refine its behavior (basic memory)

---

## 🏎️ **The Engine**

---

You’ll implement a system with these **three key layers**:

### 1. 🧠 **Cognitive Layer (LLM or prompt-engineered logic)**

Responsible for:

- Generating goals from the current state
- Reflecting on past failures
- Justifying or explaining chosen actions in natural language (e.g., “I chose to heal because I’m below 30% health and an enemy is nearby”)

**Can be implemented as:**

- A mocked prompt engine
- Simple call to an LLM (you may use the model zoo from OpenAI/Anthropic)
- Or just a deterministic pseudo-LLM module if needed

### 2. 🛠️ **Planning Layer (GOAP)**

Implements traditional GOAP:

- Actions with preconditions/effects
- A* or similar planner
- Outputs a valid plan for a given goal

### 3. 🎮 **Execution Layer (Simulation)**

Simulates:

- World state updates
- Action - success/failure
- Replanning if state changes (e.g., enemy reinforcement, resource loss)

---

## 🕹️ **Core Features You Must Build**

1. **World Model**:
    - At least 6 world state keys: health, stamina, potionCount, treasureThreatLevel, enemyNearby, isInSafeZone
2. **Action Set** (at least 6):
    - `HealSelf`, `AttackEnemy`, `Retreat`, `DefendTreasure`, `CallBackup`, `SearchForPotion`
3. **Goals**:
    - Examples: `Survive`, `EliminateThreat`, `ProtectTreasure`, `PrepareForBattle`
4. **LLM-style Output** (for at least 2 of these):
    - "Why did I pick this goal?"
    - "Why did this plan fail?"
    - "What will I do differently?"

🛠️ **Technical Specs**

---

- Language: Python
- LLM: your choice of language model(s)
- Memory: A simple JSON or list tracking past failures, choices, or goal outcomes
- Output: Console output showing steps, thoughts, and plans

---

### 🧪 **Evaluation Sample Scenarios**

### **Scenario 1: Low Health, No Healing Resources, Enemy Nearby**

**World State:**

```json
{
  "health": 20,
  "enemyNearby": true,
  "hasPotion": false,
  "treasureThreatLevel": "medium",
  "stamina": 5,
  "inSafeZone": false
}

```

**Expected Goal Priorities:**

- **Primary:** Survive (heal or retreat)
- **Secondary:** Protect treasure if possible

**Expected Agent Reasoning:**

- “My health is critically low and I don’t have potions. The enemy is close, so attacking now is risky.”
- “I should retreat to a safe zone to recover or search for healing items.”
- “If retreating isn’t possible, calling backup is my next best option.”

**Expected Plan:**

1. `Retreat` (if possible)
2. `CallBackup`
3. `SearchForPotion` (once safe)
4. `HealSelf` (if potion found)
5. `DefendTreasure`

---

### Scenario 2: **Healthy, Treasure Under Threat, Enemy Nearby**

**World State:**

```json
{
  "health": 85,
  "enemyNearby": true,
  "hasPotion": true,
  "treasureThreatLevel": "high",
  "stamina": 15,
  "inSafeZone": false
}

```

**Expected Goal Priorities:**

- **Primary:** Eliminate threat
- **Secondary:** Defend treasure

**Expected Agent Reasoning:**

- “I have high health and stamina, plus healing items if needed.”
- “The treasure is under serious threat; I must act aggressively.”
- “I will attack the enemy, but keep potions handy for healing if injured.”

**Expected Plan:**

1. `AttackEnemy`
2. `HealSelf` (if health drops below threshold during combat)
3. `DefendTreasure`
4. `CallForBackup` (if overwhelmed)

---

### Scenario 3: **No Enemy Nearby, Low Stamina, Potion Available**

**World State:**

```json
{
  "health": 70,
  "enemyNearby": false,
  "hasPotion": true,
  "treasureThreatLevel": "low",
  "stamina": 2,
  "inSafeZone": true
}

```

**Expected Goal Priorities:**

- **Primary:** Prepare for potential threats (restore stamina, maintain health)
- **Secondary:** Patrol area

**Expected Agent Reasoning:**

- “No immediate threat, but my stamina is low.”
- “I should heal and rest to prepare for the next enemy.”
- “After resting, I can patrol to monitor the treasure.”

**Expected Plan:**

1. `SearchForPotion`
2. `HealSelf` 
3. `DefendTreasure`

---

### Scenario 4: **Out of Potions, Enemy Near, Treasure Safe**

**World State:**

```json
{
  "health": 60,
  "enemyNearby": true,
  "hasPotion": false,
  "treasureThreatLevel": "low",
  "stamina": 10,
  "inSafeZone": false
}

```

**Expected Goal Priorities:**

- **Primary:** Eliminate threat
- **Secondary:** Search for potions if injured

**Expected Agent Reasoning:**

- “I have no potions but moderate health and stamina.”
- “The treasure isn’t currently threatened, but I should eliminate enemies quickly.”
- “If I get injured, I must retreat and search for potions.”

**Expected Plan:**

1. `AttackEnemy`
2. If health drops below 40%, `Retreat`
3. `SearchForPotion`
4. `HealSelf`
5. `DefendTreasure`

---

### Scenario 5: **Interrupted During Plan Execution**

**Initial World State:**

```json
{
  "health": 30,
  "enemyNearby": true,
  "hasPotion": true,
  "treasureThreatLevel": "high",
  "stamina": 10,
  "inSafeZone": false
}

```

**Planned Actions:**

- `HealSelf` → `AttackEnemy`

**During Execution:**

- The agent tries to heal but fails because the potion was stolen or spoiled.

**Expected Agent Reasoning:**

- “Healing failed. I must rethink my plan.”
- “Without healing, I should retreat or call for backup.”
- “I’ll update my goal to survive first.”

**New Plan:**

1. `Retreat`
2. `CallForBackup`

### 📦 **Deliverables**

- Source code
- README (how it works, how you simulate reasoning/LLM, how to run)
- Sample simulation output logs
- Send everything to [careers@affogato.ai](mailto:careers@affogato.ai) with subject line **‘Dungeon Guardian is here’**