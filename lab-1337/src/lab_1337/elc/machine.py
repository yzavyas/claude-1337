"""State machine for enhancement lifecycle."""

from typing import Callable, Optional

from transitions import Machine
from rich.console import Console

from lab_1337.elc.models import EnhancementStatus, status_color

console = Console()


class LifecycleMachine:
    """
    State machine for LEP/IMP lifecycle.

    Enforces valid transitions and triggers callbacks.

    Lifecycle:
        draft → discussion → fcp → accepted → implemented
                              ↘ rejected
                              ↘ postponed
    """

    states = [s.value for s in EnhancementStatus]

    transitions = [
        # Normal progression
        {
            "trigger": "start_discussion",
            "source": EnhancementStatus.DRAFT.value,
            "dest": EnhancementStatus.DISCUSSION.value,
        },
        {
            "trigger": "enter_fcp",
            "source": EnhancementStatus.DISCUSSION.value,
            "dest": EnhancementStatus.FCP.value,
        },
        {
            "trigger": "accept",
            "source": EnhancementStatus.FCP.value,
            "dest": EnhancementStatus.ACCEPTED.value,
        },
        {
            "trigger": "implement",
            "source": EnhancementStatus.ACCEPTED.value,
            "dest": EnhancementStatus.IMPLEMENTED.value,
        },
        # Alternative outcomes from FCP
        {
            "trigger": "reject",
            "source": EnhancementStatus.FCP.value,
            "dest": EnhancementStatus.REJECTED.value,
        },
        {
            "trigger": "postpone",
            "source": [EnhancementStatus.FCP.value, EnhancementStatus.DISCUSSION.value],
            "dest": EnhancementStatus.POSTPONED.value,
        },
        # Reopen postponed
        {
            "trigger": "reopen",
            "source": EnhancementStatus.POSTPONED.value,
            "dest": EnhancementStatus.DISCUSSION.value,
        },
    ]

    def __init__(
        self,
        initial_state: str = EnhancementStatus.DRAFT.value,
        on_accept: Optional[Callable] = None,
        on_implement: Optional[Callable] = None,
    ):
        """
        Initialize lifecycle machine.

        Args:
            initial_state: Starting state
            on_accept: Callback when entering accepted state (for IMP scaffolding)
            on_implement: Callback when entering implemented state
        """
        self.state = initial_state
        self._on_accept = on_accept
        self._on_implement = on_implement

        self.machine = Machine(
            model=self,
            states=self.states,
            transitions=self.transitions,
            initial=initial_state,
            auto_transitions=False,  # Only allow defined transitions
            send_event=True,  # Pass event data to callbacks
        )

        # Register callbacks
        self.machine.on_enter_accepted("_handle_accept")
        self.machine.on_enter_implemented("_handle_implement")

    def _handle_accept(self, event):
        """Called when entering accepted state."""
        if self._on_accept:
            self._on_accept(event)

    def _handle_implement(self, event):
        """Called when entering implemented state."""
        if self._on_implement:
            self._on_implement(event)

    def transition_to(self, target_status: EnhancementStatus) -> bool:
        """
        Attempt to transition to target status.

        Returns True if successful, False if transition not allowed.
        """
        current = EnhancementStatus(self.state)
        target = target_status

        # Map target status to trigger
        trigger_map = {
            EnhancementStatus.DISCUSSION: "start_discussion",
            EnhancementStatus.FCP: "enter_fcp",
            EnhancementStatus.ACCEPTED: "accept",
            EnhancementStatus.REJECTED: "reject",
            EnhancementStatus.POSTPONED: "postpone",
            EnhancementStatus.IMPLEMENTED: "implement",
        }

        trigger = trigger_map.get(target)
        if not trigger:
            console.print(f"[red]No transition defined to {target.value}[/red]")
            return False

        # Check if transition is valid
        if not self.machine.get_triggers(self.state):
            console.print(f"[red]No transitions available from {self.state}[/red]")
            return False

        if trigger not in self.machine.get_triggers(self.state):
            valid = ", ".join(self.machine.get_triggers(self.state))
            console.print(
                f"[red]Cannot transition from {current.value} to {target.value}[/red]\n"
                f"[dim]Valid transitions: {valid}[/dim]"
            )
            return False

        # Execute transition
        getattr(self, trigger)()

        console.print(
            f"[{status_color(current)}]{current.value}[/{status_color(current)}] → "
            f"[{status_color(target)}]{target.value}[/{status_color(target)}]"
        )
        return True

    @property
    def available_transitions(self) -> list[str]:
        """Get available transition triggers from current state."""
        return self.machine.get_triggers(self.state)

    @property
    def current_status(self) -> EnhancementStatus:
        """Get current status as enum."""
        return EnhancementStatus(self.state)
