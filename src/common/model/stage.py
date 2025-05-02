class Stage:
    def __init__(self, stage_id: int, name: str, pos: tuple[int, int]):
        self.pos = pos
        self.stage_id = stage_id
        self.name = name
        self.is_completed = False
        self.is_unlocked = False



class StageMap:
    def __init__(self):
        self.stages: list[Stage] = []
        self.current_stage: Stage = None
        self.map_id: int = 0
        self.map_name: str = ""
        self.edges: list[tuple[int, int]] = []

    def add_stage(self, stage: Stage):
        self.stages.append(stage)

    def set_current_stage(self, stage: Stage):
        self.current_stage = stage

    def get_current_stage(self) -> Stage:
        return self.current_stage
    
    def get_stage_by_id(self, stage_id: int) -> Stage:
        for stage in self.stages:
            if stage.stage_id == stage_id:
                return stage
        return None
    
    def add_egde(self, edge: tuple[int, int]):
        self.edges.append(edge)
        
    def get_edges(self) -> list[tuple[int, int]]:
        return self.edges

