from commons.view_transition import SingleViewTransition, ViewTransition
from commons.interfaces import ViewUpdater

class ViewTransitionSingle(ViewUpdater):
    def __init__(self, transition: ViewTransition):
        self.transition = transition

    def update(self) -> bool:
        return self.transition.update()

class ViewTransitionSwitcher(ViewUpdater):
    def __init__(self, transition_in: SingleViewTransition, transition_out: SingleViewTransition):
        transition_in.update_progress_func(True)
        transition_out.update_progress_func(False)
        self.transitions = [transition_in, transition_out]
        self.current_transition = 0

    def update(self) -> bool:
        if self.transitions[self.current_transition].update():
            return True
        self.current_transition = 1 - self.current_transition
        return self.current_transition == 1
