from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time, timedelta
from typing import Dict, List, Tuple, Set, Any
import heapq
import hashlib
import copy

# ============================================================
# 1. Core Data Models
# ============================================================

@dataclass(frozen=True)
class Activity:
    id: str
    priority: int
    start_time: time
    end_time: time
    instructions: str


@dataclass
class CompiledConstraints:
    hard_constraints: List[Any] = field(default_factory=list)
    soft_constraints: List[Any] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScheduleState:
    schedule: Dict[str, List[Activity]]
    moved_activities: Set[str]
    score: float
    depth: int


@dataclass
class Move:
    activity_id: str
    day: str
    new_start: time
    new_end: time
    cost: float


# ============================================================
# 2. Instruction Compilation
# ============================================================

def compile_instructions(text: str) -> CompiledConstraints:
    constraints = CompiledConstraints()
    t = text.lower()

    if "must" in t or "cannot" in t:
        constraints.hard_constraints.append(text)

    if "prefer" in t or "ideally" in t:
        constraints.soft_constraints.append(text)

    if "morning" in t:
        constraints.preferences["preferred_time"] = ("08:00", "12:00")

    if "afternoon" in t:
        constraints.preferences["preferred_time"] = ("12:00", "17:00")

    if "avoid friday" in t:
        constraints.hard_constraints.append("forbidden_day:Friday")

    return constraints


# ============================================================
# 3. Conflict Detection
# ============================================================

def overlaps(a: Activity, b: Activity) -> bool:
    return not (a.end_time <= b.start_time or b.end_time <= a.start_time)


def find_conflicts(schedule: Dict[str, List[Activity]]) -> List[Tuple[Activity, Activity]]:
    conflicts = []
    for day, acts in schedule.items():
        for i in range(len(acts)):
            for j in range(i + 1, len(acts)):
                if overlaps(acts[i], acts[j]):
                    conflicts.append((acts[i], acts[j]))
    return conflicts


# ============================================================
# 4. Conflict Resolution Heuristic
# ============================================================

def conflict_resolution_order(a: Activity, b: Activity) -> Activity:
    if a.priority != b.priority:
        return a if a.priority < b.priority else b
    return a if len(a.instructions) > len(b.instructions) else b


# ============================================================
# 5. Move Generation
# ============================================================

def _time_to_delta(t: time) -> timedelta:
    return timedelta(hours=t.hour, minutes=t.minute)

def _delta_to_time(d: timedelta) -> time:
    mins = int(d.total_seconds() // 60) % (24 * 60)
    return time(mins // 60, mins % 60)


def generate_valid_moves(
    activity: Activity,
    schedule: Dict[str, List[Activity]],
    constraints: CompiledConstraints,
    top_k: int = 5
) -> List[Move]:

    moves = []
    duration = _time_to_delta(activity.end_time) - _time_to_delta(activity.start_time)

    for day_index, day in enumerate(schedule.keys()):
        for hour_shift in (-2, -1, 1, 2):
            start = _delta_to_time(
                _time_to_delta(activity.start_time) + timedelta(hours=hour_shift)
            )
            end = _delta_to_time(_time_to_delta(start) + duration)

            cost = abs(hour_shift) + day_index * 0.5
            moves.append(Move(activity.id, day, start, end, cost))

    return sorted(moves, key=lambda m: m.cost)[:top_k]


# ============================================================
# 6. Scoring
# ============================================================

def evaluate_partial(schedule):
    return -len(find_conflicts(schedule))

def evaluate_full(schedule):
    return 100.0 - 10.0 * len(find_conflicts(schedule))


# ============================================================
# 7. Hashing
# ============================================================

def hash_state(schedule):
    flat = []
    for day in sorted(schedule):
        for a in sorted(schedule[day], key=lambda x: x.id):
            flat.append(f"{day}:{a.id}:{a.start_time}-{a.end_time}")
    return hashlib.sha256("|".join(flat).encode()).hexdigest()


# ============================================================
# 8. Search Engine
# ============================================================

def resolve_schedule(
    base_schedule: Dict[str, List[Activity]],
    new_activity: Activity,
    max_depth: int = 6
) -> ScheduleState:

    schedule = copy.deepcopy(base_schedule)
    schedule.setdefault("Monday", []).append(new_activity)

    start = ScheduleState(
        schedule=schedule,
        moved_activities=set(),
        score=evaluate_partial(schedule),
        depth=0,
    )

    pq = [(-start.score, start)]
    visited = set()

    while pq:
        _, state = heapq.heappop(pq)

        h = hash_state(state.schedule)
        if h in visited:
            continue
        visited.add(h)

        conflicts = find_conflicts(state.schedule)
        if not conflicts:
            state.score = evaluate_full(state.schedule)
            return state

        if state.depth >= max_depth:
            continue

        a, b = conflicts[0]
        to_move = conflict_resolution_order(a, b)

        constraints = compile_instructions(to_move.instructions)
        moves = generate_valid_moves(to_move, state.schedule, constraints)

        for m in moves:
            new_sched = copy.deepcopy(state.schedule)

            for acts in new_sched.values():
                acts[:] = [x for x in acts if x.id != to_move.id]

            new_sched.setdefault(m.day, []).append(
                Activity(
                    to_move.id,
                    to_move.priority,
                    m.new_start,
                    m.new_end,
                    to_move.instructions,
                )
            )

            heapq.heappush(
                pq,
                (-evaluate_partial(new_sched),
                 ScheduleState(
                     new_sched,
                     state.moved_activities | {to_move.id},
                     evaluate_partial(new_sched),
                     state.depth + 1,
                 ))
            )

    return start
