import math
import pandas as pd

def haversine(lat1, lon1, lat2, lon2):
    """
    위도(lat1, lat2)와 경도(lon1, lon2)를 라디안 단위로 변환한 뒤,
    지구의 평균 반지름(R=6371km)을 사용하여 두 지점 간 구면 거리(km)를 반환.
    """
    R = 6371.0  # 지구 반지름 (km)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(d_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def calculate_store_distances_to_excel(stores, output_filename="store_distances.xlsx"):
    """
    stores: [("매장명", 위도, 경도), ...] 형태의 리스트
    모든 매장 쌍의 거리를 계산하여 결과를 DataFrame으로 생성한 후 Excel 파일로 저장.
    """
    results = []
    n = len(stores)
    for i in range(n):
        name1, lat1, lon1 = stores[i]
        for j in range(i+1, n):
            name2, lat2, lon2 = stores[j]
            dist_km = haversine(lat1, lon1, lat2, lon2)
            results.append({
                "from": name1,
                "to": name2,
                "distance": round(dist_km, 2)
            })
    df_results = pd.DataFrame(results)
    df_results.to_excel(output_filename, index=False)
    print(f"총 {len(df_results)} 건의 매장 간 거리를 '{output_filename}' 파일에 저장하였습니다.")

if __name__ == "__main__":
    # 37개 매장 정보
    stores = [
        ("#.인제현리부대삼겹본능흥부찜닭김치찜", 37.9546616913906, 128.317060430997),
        ("진영휴게소순천방향부대찌개점", 35.2800735928108, 128.715606787105),
        ("공수간충주롯데마트점", 36.9797794016076, 127.91435681854),
        ("백양사휴게소순천방향부대찌개점", 35.1487239218698, 126.769146619488),
        ("장안휴게소울산방향부대찌개점", 35.2109095858153, 129.006892487861),
        ("경산휴게소상행서울방향부대찌개점", 35.8646372926359, 128.626421653704),
        ("청송휴게소청주방향부대찌개점", 36.1242486305878, 128.091060483883),
        ("충북옥천휴게소부산방향부대찌개&철판구이점", 36.2968873406111, 127.595230624332),
        ("평택신장항아리갈비점", 36.3436501620033, 128.300944677308),
        ("낙동강구미휴게소상주방향부대찌개점", 36.3456908111956, 128.295820758905),
        ("#.대전관저부대찌개삼겹본능", 36.3513791998754, 127.437589284544),
        ("낙동강의성휴게소영천방향부대찌개점", 36.4555060704948, 129.013293857079),
        ("청송휴게소영덕방향부대찌개점", 36.456830707067, 129.012012766084),
        ("오창휴게소하남방향부대찌개점", 36.6206926741095, 127.435560097683),
        ("화성휴게소목포방향부대찌개점", 37.1435698773312, 126.881222889481),
        ("#.남양주화도부대삼겹본능", 37.2398081374085, 127.56798634379),
        ("치악휴게소하행춘천방향놀부부대찌개&철판구이점", 37.2536358076336, 128.048658735614),
        ("화성휴게소상행서울방향부대찌개점", 37.2581376441718, 127.0573638555),
        ("여주휴게소인천방향부대찌개점", 37.2627454533579, 127.408483040538),
        ("의왕휴게소서울방향부대찌개점", 37.3478741786877, 126.983174447952),
        ("#.강남신세계삼겹본능공수간호반식", 37.3719442989839, 127.297173507311),
        ("의왕휴게소의왕방향부대찌개점", 37.3968948571665, 126.984640905196),
        ("#.남양주별내삼겹본능공수간", 37.4138791282265, 127.253054052427),
        ("마장휴게소통영방향부대찌개점", 37.4183329933024, 127.125752137002),
        ("원주휴게소부산방향 부대찌개", 37.4352647, 127.9290165),
        ("강남고속버스터미널부대&철판구이점", 37.4762566667723, 127.044580743347),
        ("#.센트럴시티보쌈김치찜오불장군", 37.5038952, 127.0047519),
        ("춘천효자호반식(배달형)", 37.5064357442307, 127.006834366246),
        ("강원화천부대찌개&철판구이점", 37.5174942406627, 126.865497622785),
        ("#.남양주오남본옛통흥부찜닭삼겹본능점", 37.5390661071188, 127.127261140269),
        ("#.청주분평흥부찜닭삼겹본능김치찜", 37.5456668970621, 126.841453691077),
        ("#.남양주호평보쌈부대삼겹본능", 37.6541233, 127.2445941),
        ("치악휴게소상행부산방향놀부부대찌개&철판구이점", 37.7568695614699, 128.867379191016),
        ("강릉휴게소강릉방향부대찌개점", 37.7591513462111, 128.80531587225),
        ("#.경기양주덕정보쌈삼겹본능", 37.8372208, 127.0670135),
        ("의정부민락호반식(배달형)", 37.8729365675867, 127.737561802134),
        ("강릉휴게소인천방향놀부부대찌개&철판구이점", 38.105456044048, 127.704548124087),
        ("#.강원신철원부대찌개흥부찜닭삼겹본능공수간김치찜", 38.184018468471, 127.321907093109),
    ]
    
    calculate_store_distances_to_excel(stores)
