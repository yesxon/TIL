# 231227 ELK Stack

- **엘라스틱 서치 관련 순서도**
    1. **서비스**: 데이터가 생성되는 시작점
    2. **Logstash (Load Balancing을 거침)**: 데이터를 수집하고 필요에 따라 변환. 로드 밸런싱을 통해 요청들이 여러 서버로 균등하게 분산
    3. **Logstash에서 JSON 형식으로 변환**: Logstash에서 데이터는 Elasticsearch에 적합한 JSON 형식으로 변환
    4. **Kafka**: 변환된 데이터는 Kafka를 통해 신뢰성 있게 처리
    5. **Elasticsearch**: Kafka로부터 데이터를 받아 중앙 데이터 저장소에 저장
    6. **Kibana**: Elasticsearch에 저장된 데이터를 시각화하고 분석

- **특징 :**
    - NoSQL형식 > 유동적인 형식 및 자료형 (딕셔너리와 유사)
    
    ![Untitled](ElasticSearch/imgs/Untitled.png)
    
    [https://www.samsungsds.com/kr/insights/1232564_4627.html](https://www.samsungsds.com/kr/insights/1232564_4627.html) : NoSQL 관련 뉴스레터
    
    ![Untitled](ElasticSearch/imgs/Untitled 1.png)
    
    - 엘라스틱서치에서는 하나의 인덱스에 하나의 타입만을 구성할 수 있습니다. 그리고 기본적으로 HTTP를 통해 JSON 형식의 Restful API를 사용합니다.
    
    <aside>
    💡 **RESTFul API란?**
    HTTP 헤더(header)와 URL만 사용하여 다양한 형태의 요청을 할 수 있는 HTTP 프로토콜을 최대한 활용하도록 고안된 아키텍처
    
    </aside>
    
    - (SQL - UNIQUE로 인덱싱 > SELECT 제외한 모든 과정 속도 증가) 엘라스틱서치도 마찬가지로 삽입, 삭제 연산 느린 반면, 조회 빠름
    - 전문 검색(full text search)-여러 개의 인덱스나 여러 개의 필드 색인 가능
    - 오픈소스
    - 통계 분석-로그 데이터를 수집하고 한 곳에 모아 통계 분석
    - 멀티테넌시(multi-tenency)-검색한 필드명으로 여러 개의 인덱스 한 번에 조회 가능
    - 역인덱싱-단어가 포함된 특정 문서의 위치를 알아낸다
    - 분산 환경 지원-서버에 원본(Shard), 복제본(Replica-Shard)을 저장하고 이를 적절히 load balancing한다. Cluster > Node > Shard > Document > Field
    
    ![Untitled](ElasticSearch/imgs/Untitled 2.png)
    

- **단점**
    - 원본과 레플리카가 다 쓰이기 전까지 새로운 정보 검색 X, 준실시간. 약 1s의 latency 발생.
    - 비용이 많이 드는 작업을 실행하지 않는다. (분산 처리에 최적화 되어있는 검색엔진이기에) 따라서 전체적인 클러스터의 성능 향상을 위해 commit과 rollback이 없다.
- 실습
    
    경로 > code . : VSCode 경로 설정 명령어
    
    1. 엘라스틱서치 설치 후 실행
    2. YAML 설정파일 작성
    
    ```yaml
    #config/elasticsearch.yml
    
    cluster.name: woori-es #key
    node.name: woori-es-node01 #value : 딕셔너리 구조와 유사
    
    path:
      data: C:\ITStudy\03_elk\elasticsearch\data
      logs: C:\ITStudy\03_elk\elasticsearch\logs  
    
    network.host: 127.0.0.1
    
    discovery.type: "single-node"
    xpack.security.enabled: false #비밀번호 ㄴㄴ
    ```
    
    ELK는 9200번 localhost
    
    issues : curl 명령어를 Powershell에서 사용할 수 없었음. cmd에서 실행하기.
    
    ![Untitled](ElasticSearch/imgs/Untitled 3.png)
    
    - HTTP 통신의 CRUD
        
        : request와 response 반복, 무상태성을 가짐
        
        - RESTful API로 하나의 프로토콜에 각 상태를 부여
        - create - POST (전체 첨부)
        - update- PUT(전체 업데이트), PATCH(일부 업데이트)
        - delete - DELETE
        - read - GET, HEAD (첨부하는 데이터 없음)
    
    - ElasticSearch의 CRUD
        - CREATE - POST, PUT
        - READ - GET, 본문(조건)을 달아서 보내는 요청에는 POST
        - UPDATE - PUT (ELK는 PUT만 허용)
        - DELETE - DELETE
    
    ```yaml
    **# CREATE**
    PUT [인덱스 이름]/_doc/[_id값]  # ID값을 직접 부여
    {
      [문서 내용]
    POST [인덱스 이름]/
    {
      ID자동생성 [문서 내용]
    }
    
    **# SEARCH**
    GET [인덱스 이름]/_search
    POST [인덱스 이름]/_search
    
    **# READ(RETRIEVE)**
    GET [인덱스 이름]/_doc/[_id값]
    
    **# UPDATE**
    POST [인덱스 이름]/_update/[_id값]
    ```
    
    #POST -삽입 > doc id가 없으면 난수로 값을 생성
    
    #DOC 번호를 생성하는 이유: 수정할 일이 많은 인덱스일 경우
    #DOC 번호를 생성하지 않는 이유: 수정할 일이 적은 인덱스일 경우(로그 수집, 생성되고 있는 정보 보관용)
    
    #match_phrase: 입력된 순서대로 검색한다
    
    #NoSQL의 특징: 데이터가 너무 많아지면 세세한 정합성을 지키다가 에러 발생. 따라서 예외를 많이 허용
    
    ## 인덱스 관리
    
    - 모든 인덱스는 두 개의 정보 단위를 가지고 있습니다. 바로 settings 과 mappings입니다.
    
    ## Mappings
    
    <aside>
    💡 Mapping(맵핑)
    문서가 인덱스에 어떻게 색인되고 저장되는지 정의하는 부분을 의미합니다. SQL의 자료형과 유사한 방법입니다.
    
    </aside>
    
    ### 동적 맵핑 vs 명시적 맵핑
    
    엘라스틱서치가 자동으로 생성하는 맵핑을 동적 맵핑(dynamic mapping) (- 인덱스명/자료 넣으면 자동으로 자료형 생성)이라고 부릅니다. 반대로 사용자가 문서의 각 필드에 데이터를 어떠한 형태로 저장할 것인지를 타입이라는 설정으로 맵핑을 지정해 주는 방법은 명시적 맵핑(explicit mapping)(빈 인덱스를 만들어 놓고, 그 안에 자료를 집어넣음) 이라고 부릅니다.
    
    ## 엘라스틱서치의 필드 타입 종류
    
    | 분류 | 종류 |
    | --- | --- |
    | 심플 타입 | text, keyword, date, long, double, boolean, ip 등 |
    | 계층 구조를 지원하는 타입 | object, nested 등 |
    | 그 외 특수한 타입 | geo_point, geo_shape 등 |
    
    ## 배열
    
    엘라스틱서치에는 배열을 표현하는 별도의 타입 구분 X. long 타입의 필드에 단일 숫자 데이터 혹은 배열 데이터 삽입 가능.
    
    ```jsx
    PUT 인덱스명
    	{
    		"mappings": {
    			"properties": {
    				"longField": {
    				"type": "long"
    				},
    				"keywordField": {
    					"type": "keyword"
    				}
    			}
    		}
    }
    ```
    
    ## Object type과 Nested 타입
    
    - Object Type
        - JSON 문서는 필드의 하위에 다른 필드를 여럿 포함하는 객체 데이터를 담을 수 있는데, object 타입은 이런 형태의 데이터를 담는 필드 타입
        
        ```jsx
        POST 인덱스명/_doc/
        {
          "object명": {
            "필드명1": "컬럼명1",
            "필드명2": "컬럼명2"
          }
        }
        ```
        
        - 
    - Nested Type
        - nested 타입은 객체 배열의 각 객체를 내부적으로 별도의 루씬 문서로 분리해 저장합니다.
        - 배열의 원소가 100개라면 부모 문서까지 해서 101개의 문서가 내부적으로 생성
        - nested 쿼리라는 전용 쿼리를 이용해서 검색
        
        ```json
        PUT 인덱스명
        {
          "mappings": {
            "properties": {
              "객체명": {
                "type": "nested",
                "properties": {
                  "필드명1": {
                    "type": "keyword"
                  },
                  "필드명2": {
                    "type": "long"
                  }
                }
              }
            }
          }
        }
        ```
        
    
    ### 벌크 데이터
    
    ```yaml
    POST _bulk/ #벌크 데이터 입력하는 명령어
     
    #match_all, match, match_phrase, query_string
    GET test/_search
    {
      "query": {
        "match": {
          "필드명": "검색어"
        }
      }
    }
    #AND는 문자열 사이에 대문자로,
    #OR은 띄어쓰기로 표현됨
    GET /_search
    {
      "query": {
        "query_string": {
          "query":"검색어",
    			#필드 지정, 미지정도 이상 없음
          "default_field": "필드명" 
    			#또는 "fields" = ["필드1", "필드2"]
        }
      }
    }
    ```
    
    - bool query
        
        ![Untitled](ElasticSearch/imgs/Untitled 4.png)