import os
import requests
import pandas as pd
import time

def get_naver_driving_distance(start_lat, start_lon, end_lat, end_lon, client_id, client_secret):
    """
    네이버 클라우드의 Direction5 API를 이용해 두 지점(위도, 경도) 사이의 실제 주행 거리를 구함.
    네이버 API에서는 좌표 순서가 "경도,위도"로 지정됩니다.
    
    반환: 주행 거리 (킬로미터 단위)
    """
    # curl 샘플의 엔드포인트를 사용: https://maps.apigw.ntruss.com/map-direction/v1/driving
    url = "https://maps.apigw.ntruss.com/map-direction/v1/driving"
    # API는 좌표 순서가 "경도,위도"이므로 변환합니다.
    start = f"{start_lon},{start_lat}"
    goal = f"{end_lon},{end_lat}"
    
    params = {
        "start": start,
        "goal": goal,
        "option": "traoptimal"  # 최적 경로 옵션
    }
    # 헤더는 curl 샘플의 소문자 키를 그대로 사용합니다.
    headers = {
        "x-ncp-apigw-api-key-id": client_id,
        "x-ncp-apigw-api-key": client_secret
    }
    
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        raise Exception(f"API 요청 실패: {response.status_code} {response.text}")
    
    data = response.json()
    try:
        # 응답 JSON에서 실제 주행 거리는 미터 단위로 제공됩니다.
        distance_m = data["route"]["traoptimal"][0]["summary"]["distance"]
        return distance_m / 1000  # km 단위로 변환
    except Exception as e:
        raise Exception("API 응답 파싱 오류: " + str(e))

def calculate_distances_and_save(stores, client_id, client_secret, output_filename="최나영_store_distances_naver.xlsx"):
    """
    stores: [("매장명", 위도, 경도), ...] 형태의 리스트
    네이버 지도 API를 이용해 모든 매장 쌍의 실제 주행 거리를 계산한 후,
    결과를 'from', 'to', 'distance' 컬럼으로 구성하여 Excel 파일로 저장합니다.
    """
    results = []
    n = len(stores)
    for i in range(n):
        name1, lat1, lon1 = stores[i]
        for j in range(i+1, n):
            name2, lat2, lon2 = stores[j]
            try:
                distance_km = get_naver_driving_distance(lat1, lon1, lat2, lon2, client_id, client_secret)
            except Exception as e:
                print(f"Error between {name1} and {name2}: {e}")
                distance_km = None
            results.append({
                "from": name1,
                "to": name2,
                "distance": round(distance_km, 2) if distance_km is not None else None
            })
            # API 호출 제한을 피하기 위해 약간의 딜레이 추가 (필요 시 조정)
            time.sleep(0.2)
    
    df_results = pd.DataFrame(results)
    df_results.to_excel(output_filename, index=False)
    print(f"총 {len(df_results)} 건의 매장 간 거리를 '{output_filename}' 파일에 저장하였습니다.")

if __name__ == "__main__":
    # 네이버 API 인증 정보 (환경변수 또는 직접 입력)
    NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "y6p7r0ntrw")
    NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "U2Gb6vaQsVos23wmhlXkI3BiMUdvjSu9ntshFWW5")
    # 37개 매장 정보 (매장명, 위도, 경도)
    stores = [  ("최나영 자택",37.504922, 126.936292),
("최나영 거점", 37.504922, 126.936292),
    ("삼송동산부대찌개&철판구이점", 37.6435954991253, 126.884977255817),
    ("화곡보쌈부대찌개김치찜", 37.545788, 126.841572),
    ("포이부대찌개&철판구이점", 35.9808620295644, 128.398106404204),
    ("상암삼겹본능(단일전환)", 37.579568, 126.890355),
    ("공수간코엑스점", 37.511853, 127.059151),
    ("고양고양흥부찜닭삼겹본능공수", 37.703455, 126.901441),
    ("일산주엽역부대공수간점", 37.670179, 126.759766),
    ("목동파라곤부대삼겹본능김치찜", 37.529478, 126.875175),
    ("신림흥부찜닭삼겹본능공수간점", 37.476823, 126.937528),
    ("수서역부대찌개&철판구이점", 37.488198, 127.101713),
    ("사당부대김치찜", 37.475816, 126.981104),
    ("역삼2호부대찌개&철판구이점", 37.497772, 127.041576),
    ("강남씨티부대찌개&철판구이점", 37.501112, 127.027194),
    ("삼성1호보쌈부대", 37.507326, 127.063132),
    ("문래에이스부대삼겹본능김치찜", 37.514916, 126.898872),
    ("압구정부대(단일전환)", 37.524989, 127.027281),
    ("신정보쌈삼겹본능김치찜", 37.527012, 126.8586),
    ("양천구청부대찌개&철판구이점", 37.517534, 126.865232),
    ("용산역사아이파크보쌈부대", 37.529727, 126.964221),
    ("대림썬프라자부대삼겹본능김치찜", 37.496307, 126.907847),
    ("순화동부대찌개&철판구이점", 37.560257, 126.972028),
    ("충정로역부대찌개삼겹본능", 37.560248, 126.962407),
    ("명동부대찌개&철판구이점", 37.563242, 126.985138),
    ("을지로6가보쌈부대", 37.567777, 127.007616),
    ("방화부대흥부찜닭삼겹본능김치찜", 37.567776, 126.809698),
    ("신정흥부찜닭옛날통닭공수간부대", 37.526935, 126.858643),
    ("동대문홈플러스부대찌개&철판구이", 37.574731, 127.038693),
    ("상암1호부대", 37.579808, 126.890113),
    ("논현삼겹본능(단일전환)", 37.508885, 127.018825),
    ("불광역놀부부대찌개&철판구이점", 37.611586, 126.929999),
    ("후암부대점", 37.550763, 126.977314),
    ("파주탄현부대찌개김치찜", 37.82278, 126.726172),
    ("고양화정부대점", 37.633153, 126.83201),
    ("파주운정보쌈삼겹본능", 37.723385, 126.738696),

        ]
    
    calculate_distances_and_save(stores, NAVER_CLIENT_ID, NAVER_CLIENT_SECRET)
