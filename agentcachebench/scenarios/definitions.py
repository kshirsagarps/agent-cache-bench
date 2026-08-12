from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class ScenarioSpec:
    scenario_id: str
    name: str
    description: str
    mutation_type: str  # "none", "exact", "tool_append", "prefix_edit", "mid_insert", "pause_decay"
    pause_ms: float
    reset_cache_between_steps: bool = False

SCENARIO_CATALOG: Dict[str, ScenarioSpec] = {
    "S0": ScenarioSpec(
        scenario_id="S0",
        name="Cold Recomputation",
        description="No cache reuse; cache is cleared between steps.",
        mutation_type="none",
        pause_ms=0.0,
        reset_cache_between_steps=True
    ),
    "S1": ScenarioSpec(
        scenario_id="S1",
        name="Exact Continuation",
        description="Unchanged previous context with sequential prompt appending.",
        mutation_type="exact",
        pause_ms=100.0,
        reset_cache_between_steps=False
    ),
    "S2": ScenarioSpec(
        scenario_id="S2",
        name="Tool Result Appended",
        description="LLM -> Tool -> Tool output appended -> LLM execution.",
        mutation_type="tool_append",
        pause_ms=1000.0,
        reset_cache_between_steps=False
    ),
    "S3": ScenarioSpec(
        scenario_id="S3",
        name="Context Mutation",
        description="Prefix modification, middle insertion, or file block replacement.",
        mutation_type="mid_insert",
        pause_ms=1000.0,
        reset_cache_between_steps=False
    ),
    "S4": ScenarioSpec(
        scenario_id="S4",
        name="Pause & Cache Interruption",
        description="Varying inter-tool pause durations under memory pressure.",
        mutation_type="pause_decay",
        pause_ms=30000.0,  # 30s pause
        reset_cache_between_steps=False
    )
}
