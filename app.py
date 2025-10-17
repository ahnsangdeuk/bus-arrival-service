from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# 샘플 버스 정류장 데이터
BUS_STOPS = {
    "1001": {"name": "서울역", "location": "서울특별시 중구"},
    "1002": {"name": "강남역", "location": "서울특별시 강남구"},
    "1003": {"name": "홍대입구역", "location": "서울특별시 마포구"},
    "1004": {"name": "명동", "location": "서울특별시 중구"},
    "1005": {"name": "이태원", "location": "서울특별시 용산구"}
}

# 샘플 버스 노선 데이터
BUS_ROUTES = {
    "146": {"name": "146번", "stops": ["1001", "1002", "1003"]},
    "201": {"name": "201번", "stops": ["1002", "1004", "1005"]},
    "301": {"name": "301번", "stops": ["1001", "1004", "1005"]}
}

@app.route('/')
def home():
    return jsonify({
        "service": "Bus Arrival Service",
        "version": "1.0.0",
        "description": "버스 도착 시간 조회 서비스",
        "endpoints": {
            "/stops": "정류장 목록 조회",
            "/stops/<stop_id>": "특정 정류장 정보 조회",
            "/stops/<stop_id>/arrivals": "정류장별 버스 도착 정보 조회",
            "/routes": "버스 노선 목록 조회",
            "/routes/<route_id>": "특정 노선 정보 조회"
        }
    })

@app.route('/stops')
def get_stops():
    """모든 정류장 목록 조회"""
    return jsonify({
        "stops": BUS_STOPS
    })

@app.route('/stops/<stop_id>')
def get_stop(stop_id):
    """특정 정류장 정보 조회"""
    if stop_id not in BUS_STOPS:
        return jsonify({"error": "정류장을 찾을 수 없습니다"}), 404
    
    return jsonify({
        "stop_id": stop_id,
        **BUS_STOPS[stop_id]
    })

@app.route('/stops/<stop_id>/arrivals')
def get_arrivals(stop_id):
    """정류장별 버스 도착 정보 조회"""
    if stop_id not in BUS_STOPS:
        return jsonify({"error": "정류장을 찾을 수 없습니다"}), 404
    
    arrivals = []
    current_time = datetime.now()
    
    # 해당 정류장을 지나는 버스 노선들 찾기
    for route_id, route_info in BUS_ROUTES.items():
        if stop_id in route_info["stops"]:
            # 랜덤한 도착 시간 생성 (1-15분 후)
            arrival_minutes = random.randint(1, 15)
            arrival_time = current_time + timedelta(minutes=arrival_minutes)
            
            arrivals.append({
                "route_id": route_id,
                "route_name": route_info["name"],
                "arrival_time": arrival_time.strftime("%H:%M"),
                "remaining_minutes": arrival_minutes,
                "status": "정상운행" if arrival_minutes > 3 else "곧 도착"
            })
    
    # 도착 시간 순으로 정렬
    arrivals.sort(key=lambda x: x["remaining_minutes"])
    
    return jsonify({
        "stop_id": stop_id,
        "stop_name": BUS_STOPS[stop_id]["name"],
        "current_time": current_time.strftime("%H:%M"),
        "arrivals": arrivals
    })

@app.route('/routes')
def get_routes():
    """모든 버스 노선 목록 조회"""
    return jsonify({
        "routes": BUS_ROUTES
    })

@app.route('/routes/<route_id>')
def get_route(route_id):
    """특정 노선 정보 조회"""
    if route_id not in BUS_ROUTES:
        return jsonify({"error": "노선을 찾을 수 없습니다"}), 404
    
    route_info = BUS_ROUTES[route_id].copy()
    # 정류장 ID를 실제 정류장 정보로 변환
    route_info["stops"] = [
        {
            "stop_id": stop_id,
            **BUS_STOPS[stop_id]
        } for stop_id in route_info["stops"]
    ]
    
    return jsonify({
        "route_id": route_id,
        **route_info
    })

@app.route('/health')
def health_check():
    """서비스 상태 확인"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚌 버스 도착 서비스 시작 중...")
    print("📍 사용 가능한 정류장 ID: 1001, 1002, 1003, 1004, 1005")
    print("🚌 사용 가능한 노선 ID: 146, 201, 301")
    print("🌐 서비스 URL: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)