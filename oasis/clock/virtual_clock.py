# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
"""
Virtual Clock for deterministic simulation time.

This module provides a VirtualClock class that enables:
- Discrete tick-based simulation time (detached from wall-clock)
- Within-tick timestamp variation (different events in same tick get different times)
- Causality enforcement (dependent events always have later timestamps)
- Human-readable datetime mapping for export/display
"""
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Optional, Set, Tuple


@dataclass
class VirtualClock:
    """
    Deterministic simulation clock with within-tick variation and causality support.
    
    This clock provides a fully internal, deterministic time system that is
    completely detached from real-world wall-clock time. Time only advances
    when you explicitly call `advance_tick()`.
    
    Key features:
    - Discrete ticks: Each call to `advance_tick()` moves forward by a configurable
      duration (default: 1 day = 86400 seconds).
    - Within-tick variation: Multiple events in the same tick get different
      timestamps via random offsets within the tick's time range.
    - Causality: Dependent events (e.g., comments on posts) are guaranteed to
      have timestamps after their parent events.
    - Determinism: Seeded randomness ensures reproducible timestamps across runs.
    - Human-readable export: Virtual timestamps can be converted to datetimes.
    
    Attributes:
        tick_duration_s: Duration of each tick in virtual seconds (default: 86400 = 1 day).
        epoch: The datetime that corresponds to virtual time 0 (default: 2024-01-01).
        seed: Random seed for deterministic timestamp generation.
        tick: Current tick number (starts at 0).
    
    Example:
        >>> clock = VirtualClock(tick_duration_s=86400, seed=42)
        >>> 
        >>> # Generate timestamps for events in tick 0
        >>> post_time = clock.event_time(agent_id=1, action_hint="create_post")
        >>> comment_time = clock.event_time(agent_id=2, parent_time=post_time, action_hint="comment")
        >>> assert comment_time > post_time  # Causality enforced
        >>> 
        >>> # Advance to next tick
        >>> clock.advance_tick()
        >>> new_time = clock.event_time(agent_id=1)
        >>> assert new_time >= clock.tick_duration_s  # In tick 1's range
        >>> 
        >>> # Convert to human-readable datetime
        >>> print(clock.to_datetime(post_time))  # e.g., 2024-01-01 14:32:17
    """
    
    # Configuration (set at init, generally don't change)
    tick_duration_s: int = 86400  # Default: 1 tick = 1 day (in seconds)
    epoch: datetime = field(default_factory=lambda: datetime(2024, 1, 1, 0, 0, 0))
    seed: int = 42
    
    # State
    tick: int = 0
    
    # Internal tracking (not set by user)
    _rng: random.Random = field(default=None, init=False, repr=False)
    _event_counter: Dict[Tuple[int, int], int] = field(
        default_factory=dict, init=False, repr=False
    )
    _used_times: Dict[int, Set[int]] = field(
        default_factory=dict, init=False, repr=False
    )
    
    def __post_init__(self):
        """Initialize random number generator with seed."""
        self._rng = random.Random(self.seed)
        self._event_counter = {}
        self._used_times = {}
    
    def advance_tick(self, n: int = 1) -> None:
        """
        Advance simulation time by n ticks.
        
        This is the only way time moves forward in the virtual clock.
        Call this at the end of each simulation step (env.step()).
        
        Args:
            n: Number of ticks to advance (default: 1).
        """
        self.tick += n
        # Clear per-tick tracking for clean state
        # (old tick data can be kept for debugging, but clear event counter)
        self._event_counter = {}
    
    def tick_start_s(self) -> int:
        """
        Get the start of the current tick in virtual seconds since epoch.
        
        Returns:
            Virtual seconds at the start of the current tick.
        """
        return self.tick * self.tick_duration_s
    
    def tick_end_s(self) -> int:
        """
        Get the end of the current tick in virtual seconds since epoch.
        
        Returns:
            Virtual seconds at the end of the current tick (inclusive).
        """
        return (self.tick + 1) * self.tick_duration_s - 1
    
    def event_time(
        self,
        agent_id: int,
        parent_time: Optional[int] = None,
        action_hint: str = ""
    ) -> int:
        """
        Generate a virtual timestamp for an event.
        
        This method generates unique, deterministic timestamps within the current
        tick. If a parent_time is provided, the generated timestamp is guaranteed
        to be greater than the parent (causality enforcement).
        
        Args:
            agent_id: The agent performing the action. Used for deterministic seeding.
            parent_time: If set, this event must come AFTER parent_time.
                        Use this for comments (parent = post), reactions, replies, etc.
            action_hint: Optional string describing the action (e.g., "create_post").
                        Used for deterministic seeding to ensure different action types
                        get different timestamps even from the same agent.
        
        Returns:
            Virtual timestamp in seconds since epoch.
        
        Example:
            >>> # Independent event (e.g., creating a post)
            >>> post_time = clock.event_time(agent_id=5, action_hint="create_post")
            >>> 
            >>> # Dependent event (e.g., comment on the post)
            >>> comment_time = clock.event_time(agent_id=7, parent_time=post_time, action_hint="comment")
            >>> assert comment_time > post_time
        """
        tick_start = self.tick_start_s()
        tick_end = self.tick_end_s()
        
        # Determine valid time range
        if parent_time is not None:
            # Causality: must come strictly after parent
            min_time = parent_time + 1
        else:
            min_time = tick_start
        
        max_time = tick_end
        
        # Handle edge case: parent was at end of tick (or beyond)
        if min_time > max_time:
            # Spill into next "second" beyond tick boundary
            # This maintains causality even at tick edges
            return parent_time + 1
        
        # Generate deterministic seed based on event identity
        event_key = (self.tick, agent_id)
        event_index = self._event_counter.get(event_key, 0)
        self._event_counter[event_key] = event_index + 1
        
        # Create a local RNG seeded with event-specific values
        local_seed = hash((self.seed, self.tick, agent_id, action_hint, event_index))
        local_rng = random.Random(local_seed)
        
        # Generate timestamp within valid range
        generated_time = local_rng.randint(min_time, max_time)
        
        # Ensure uniqueness within the tick (optional, for strict ordering)
        used = self._used_times.setdefault(self.tick, set())
        attempts = 0
        max_attempts = max_time - min_time + 1
        while generated_time in used and attempts < max_attempts:
            generated_time = (generated_time + 1)
            if generated_time > max_time:
                generated_time = min_time
            attempts += 1
        
        used.add(generated_time)
        return generated_time
    
    def to_datetime(self, virtual_time_s: int) -> datetime:
        """
        Convert virtual seconds to a datetime object.
        
        This is useful for displaying timestamps in human-readable format
        or exporting data for analysis.
        
        Args:
            virtual_time_s: Virtual timestamp in seconds since epoch.
        
        Returns:
            datetime object representing the virtual time.
        """
        return self.epoch + timedelta(seconds=virtual_time_s)
    
    def to_iso_string(self, virtual_time_s: int) -> str:
        """
        Convert virtual seconds to ISO format datetime string.
        
        Args:
            virtual_time_s: Virtual timestamp in seconds since epoch.
        
        Returns:
            ISO format datetime string (e.g., "2024-01-01 14:32:17").
        """
        return self.to_datetime(virtual_time_s).strftime("%Y-%m-%d %H:%M:%S")
    
    def from_datetime(self, dt: datetime) -> int:
        """
        Convert a datetime to virtual seconds.
        
        Args:
            dt: datetime object to convert.
        
        Returns:
            Virtual timestamp in seconds since epoch.
        """
        delta = dt - self.epoch
        return int(delta.total_seconds())
    
    # ==================== Backward Compatibility ====================
    # These methods maintain compatibility with the legacy Clock interface
    
    @property
    def time_step(self) -> int:
        """
        Alias for tick (backward compatibility with legacy Clock).
        
        Returns:
            Current tick number.
        """
        return self.tick
    
    @time_step.setter
    def time_step(self, value: int):
        """Set tick value (backward compatibility)."""
        self.tick = value
    
    def get_time_step(self) -> str:
        """
        Get tick as string (backward compatibility with legacy Clock).
        
        Returns:
            Current tick as a string.
        """
        return str(self.tick)
    
    def time_transfer(self, now_time: datetime, start_time: datetime) -> datetime:
        """
        Legacy method for datetime-based time (backward compatibility).
        
        Note: This method exists for backward compatibility but is NOT
        recommended for use with VirtualClock. Use event_time() instead.
        
        For VirtualClock, this returns the epoch plus current tick's duration,
        ignoring the now_time parameter (since VirtualClock is detached from
        wall-clock time).
        
        Args:
            now_time: Ignored in VirtualClock (kept for interface compatibility).
            start_time: Ignored in VirtualClock (kept for interface compatibility).
        
        Returns:
            datetime corresponding to current tick start.
        """
        # Return datetime based on current tick, ignoring wall-clock
        return self.to_datetime(self.tick_start_s())
    
    def reset(self) -> None:
        """
        Reset the clock to initial state.
        
        Resets tick to 0 and clears all internal tracking.
        """
        self.tick = 0
        self._rng = random.Random(self.seed)
        self._event_counter = {}
        self._used_times = {}
    
    def __str__(self) -> str:
        """String representation showing current state."""
        return (
            f"VirtualClock(tick={self.tick}, "
            f"tick_duration_s={self.tick_duration_s}, "
            f"current_range=[{self.tick_start_s()}, {self.tick_end_s()}])"
        )

