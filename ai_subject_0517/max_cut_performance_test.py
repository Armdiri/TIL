import time
import random
from collections import defaultdict

# 친밀도 데이터 정의
closeness = {
    ('부장', '과장'): 8,
    ('부장', '대리'): 3,
    ('부장', '사원'): 1,
    ('부장', '인턴'): 1,
    ('과장', '대리'): 7,
    ('과장', '사원'): 2,
    ('대리', '사원'): 6,
    ('대리', '인턴'): 4,
    ('사원', '인턴'): 5
}

def generate_test_graph(n_nodes):
    """테스트용 그래프 생성"""
    graph = defaultdict(dict)
    positions = [f'직원{i}' for i in range(n_nodes)]
    
    # 기존 친밀도 데이터를 기반으로 확장
    base_positions = ['부장', '과장', '대리', '사원', '인턴']
    base_graph = defaultdict(dict)
    for (p1, p2), weight in closeness.items():
        base_graph[p1][p2] = weight
        base_graph[p2][p1] = weight
    
    # 기본 5명의 데이터를 복사
    for i in range(min(5, n_nodes)):
        for j in range(i+1, min(5, n_nodes)):
            p1, p2 = base_positions[i], base_positions[j]
            if p2 in base_graph[p1]:
                graph[positions[i]][positions[j]] = base_graph[p1][p2]
                graph[positions[j]][positions[i]] = base_graph[p1][p2]
    
    # 추가 노드에 대한 랜덤 친밀도 생성
    for i in range(5, n_nodes):
        for j in range(i+1, n_nodes):
            weight = random.randint(1, 10)
            graph[positions[i]][positions[j]] = weight
            graph[positions[j]][positions[i]] = weight
    
    return graph, positions

def max_cut_brute_force(graph, positions):
    """브루트포스 방식으로 Max-Cut 계산"""
    n = len(positions)
    max_cut = 0
    best_partition = None
    
    # 모든 가능한 분할 시도 (2^(n-1) - 1)
    for i in range(1, 2**(n-1)):
        partition = []
        for j in range(n):
            if (i >> j) & 1:
                partition.append(positions[j])
        
        # 컷의 크기 계산
        cut_size = 0
        for u in partition:
            for v in positions:
                if v not in partition and v in graph[u]:
                    cut_size += graph[u][v]
        
        if cut_size > max_cut:
            max_cut = cut_size
            best_partition = (partition, [v for v in positions if v not in partition])
    
    return max_cut, best_partition

def test_performance():
    """성능 테스트 실행"""
    node_counts = list(range(2, 21))  # 2부터 20까지의 노드 수 테스트
    execution_times = []
    max_nodes = 0
    
    print("=== Max-Cut 알고리즘 성능 테스트 ===")
    print("친밀도 데이터를 기반으로 한 확장 테스트")
    print("기본 5명의 친밀도 데이터를 유지하고 나머지는 랜덤 생성")
    
    for n in node_counts:
        print(f"\nTesting with {n} nodes...")
        graph, positions = generate_test_graph(n)
        
        start_time = time.time()
        try:
            max_cut, partition = max_cut_brute_force(graph, positions)
            execution_time = time.time() - start_time
            execution_times.append(execution_time)
            
            print(f"Nodes: {n}, Execution Time: {execution_time:.2f} seconds")
            print(f"Max Cut Value: {max_cut}")
            
            if execution_time < 60:  # 1분 이내에 실행되는 경우
                max_nodes = n
            else:
                print("Execution time exceeded 60 seconds, stopping test.")
                break
                
        except Exception as e:
            print(f"Error with {n} nodes: {str(e)}")
            break
    
    print(f"\n=== 테스트 결과 요약 ===")
    print(f"최대 처리 가능 노드 수 (60초 이내): {max_nodes}")
    print("\n노드 수별 실행 시간:")
    for i, n in enumerate(node_counts[:len(execution_times)]):
        print(f"{n} nodes: {execution_times[i]:.2f} seconds")

if __name__ == "__main__":
    test_performance() 