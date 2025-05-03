# Max-Flow Min-Cut Theorem

## 1. 기본 개념
### 네트워크 흐름(Network Flow)
- 방향 그래프 G = (V, E)에서
- 각 간선 (u,v) ∈ E는 용량 c(u,v) ≥ 0을 가짐
- 소스(source) s와 싱크(sink) t가 존재
- 모든 정점 v ∈ V - {s,t}에 대해 들어오는 흐름과 나가는 흐름이 같음

### 컷(Cut)
- 소스 s와 싱크 t를 포함하는 두 개의 부분집합 S와 T로 그래프를 분할
- 컷의 용량: S에서 T로 가는 모든 간선의 용량의 합
- 컷의 흐름: S에서 T로 가는 흐름에서 T에서 S로 가는 흐름을 뺀 값

## 2. Max-Flow Min-Cut Theorem
### 정리
- 네트워크에서 최대 유량은 최소 컷의 용량과 같다
- 즉, max flow = min cut

### 증명의 핵심
1. 최대 유량 f가 존재할 때, 잔여 네트워크(residual network)에서 s에서 도달 가능한 정점들의 집합 S를 정의
2. S의 여집합 T는 t를 포함
3. S와 T 사이의 모든 간선은 용량을 모두 사용한 상태
4. 따라서 이 컷의 용량이 최대 유량과 같음

## 3. Ford-Fulkerson 알고리즘
### 기본 아이디어
- 증가 경로(augmenting path)를 찾아 유량을 증가
- 잔여 네트워크에서 s에서 t까지의 경로를 찾음
- 경로의 최소 잔여 용량만큼 유량을 증가

### 구현
```python
def ford_fulkerson(graph, source, sink):
    # 초기화
    flow = 0
    residual = graph.copy()
    
    while True:
        # BFS로 증가 경로 찾기
        path, min_capacity = find_augmenting_path(residual, source, sink)
        if not path:
            break
            
        # 유량 증가
        flow += min_capacity
        for u, v in path:
            residual[u][v] -= min_capacity
            residual[v][u] += min_capacity
    
    return flow

def find_augmenting_path(residual, source, sink):
    # BFS로 증가 경로 찾기
    queue = [source]
    parent = {source: None}
    
    while queue:
        u = queue.pop(0)
        for v, capacity in residual[u].items():
            if v not in parent and capacity > 0:
                parent[v] = u
                if v == sink:
                    # 경로 복원
                    path = []
                    current = sink
                    min_capacity = float('inf')
                    while current != source:
                        prev = parent[current]
                        path.append((prev, current))
                        min_capacity = min(min_capacity, residual[prev][current])
                        current = prev
                    return path, min_capacity
                queue.append(v)
    
    return None, 0
```

## 4. 응용 분야
- 네트워크 라우팅
- 이미지 분할
- 작업 할당
- 매칭 문제
- 프로젝트 선택

## 5. 시간 복잡도
- 기본 Ford-Fulkerson: O(E * f) (f는 최대 유량)
- Edmonds-Karp 알고리즘: O(VE²)
- Dinic's 알고리즘: O(V²E)

## 6. 참고 자료
- Introduction to Algorithms (CLRS)
- Network Flows: Theory, Algorithms, and Applications
- Algorithm Design (Kleinberg & Tardos) 