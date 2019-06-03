import numpy as np
class brutal_ai:
    
    def __init__(self, map_instance):
        
        self._ref_map = map_instance
        self._sqrDist = self._ref_map.get_scale()
        self._direction_rep = {(self._sqrDist, 0): "D", (-self._sqrDist, 0): "A", (0, self._sqrDist): "S", (0, -self._sqrDist): "W"}
        
        
    def get_path(self):
        
        def cost_function(here: list, there: list):
            return np.sqrt((here[0] - there[0])**2 + (here[1] - there[1])**2)
            
        def reconstruct_path(cameFrom, Current):
            total_path = [Current]
            while Current in cameFrom.keys():
                Current = cameFrom[Current]
                total_path.append(Current)

            get_vector = lambda f, i: self._direction_rep[tuple((np.array(f) - np.array(i)).tolist())]
            
            path_lenth = len(total_path)
            total_path = [get_vector(total_path[n], total_path[n+1]) for n in range(path_lenth-1)]
            
            return total_path
        
        
        fCost, sCost = dict(), dict()
        for cor in self._ref_map.get_map():
            sCost[tuple(cor)], fCost[tuple(cor)] = 10**9, 10**9
        
        
        start = tuple(self._ref_map.get_snk_pos())
        end = tuple(self._ref_map.get_food_pos())
        
        camefrom = dict()
        sCost[start] = 0
        fCost[start] = cost_function(start, end)
    
        openSet = [start]
        closedSet = []
        
        while openSet:
            current = openSet[np.argmin([fCost[n] for n in openSet])]

            if current == end:
                return reconstruct_path(camefrom, current)
                
            openSet.remove(current)
            closedSet.append(current)
            
            neightbors = [(current[0] + self._sqrDist, current[1]), (current[0] - self._sqrDist, current[1]), (current[0], current[1] + self._sqrDist), (current[0], current[1] - self._sqrDist)]
            for neightbor in neightbors:
                if neightbor in self._ref_map.get_obstacles():
                    continue
                
                elif neightbor in closedSet:
                    continue
                
                tentative_sCost = sCost[current] + self._sqrDist
                
                if neightbor not in openSet:
                    openSet.append(neightbor)
                
                elif tentative_sCost >= fCost[neightbor]:
                    continue
                
                camefrom[neightbor] = current
                sCost[neightbor] = tentative_sCost
                fCost[neightbor] = sCost[neightbor] + cost_function(neightbor, end)

        raise Exception("PATH not found")
        
        
        

if __name__ == "__main__":
    from bin import Grid, Snake, Food

    grd = Grid.grid()
    