# 231228

**토큰이란?** 

교환 가치를 가지고 있는 데이터

예)

클라이언트 - 서버

id, pw → 

       ← 난수화 된 인증토큰

ELK index

클라이언트 - 서버

단어 → 

←단어 토큰 인덱스doc번호

### 텍스트 분석

- whitespace - 공백으로 단어 분리
- stop - 불용어 제거(a, the, 특수문자 등)
- keyword - 분석을 수행하지 않고 통으로 출력
- fingerprint - 정렬된 텍스트 토크나이징, 알파벳으로 타 언어 검색이 가능하도록 정렬
    
    ```jsx
    POST _analyze
    {
    "analyzer": "keyword",
    "text": "Hello, HELLO, what a wonderful World!"
    }
    ```
    
    ```jsx
    POST _analyze
    {
    "tokenizer": {
    "type": "ngram",
    "min_gram": 3,
    "max_gram": 4,
    "token_chars": ["letter"] //단어 단위에서 쪼개기, 이외에도 digit(숫자), punctuation(구두점)이 있음
    },
    "text": "Hello, World!"
    }
    ```
    

![Untitled](https://github.com/yesxon/TIL/blob/main/ElasticSearch/imgs/Untitled5.png)

- 토큰 필터
    - lowercase:  모든 대문자를 소문자로 변경
    - stop : 불용어(stopword)들은 검색 토큰에서 제외
    - snowball: -s, -ing 등을 제거
    - synonym : 유의어, 이음동의어
    
    ```jsx
    POST _analyze
    {
      "filter": [ "lowercase" ],
      "text": "Hello, World!"
    }
    ```
    

- 한글 형태소 분석: nori 플러그인
    
    ```bash
    $ bin/elasticsearch-plugin install analysis-nori 
    #에러가 발생해서 플러그인 설치가 안 됐음. bat
    #Transform encountered an exception: [Search rejected due to missing shards [[.slo-observability.sli-v2][0]]. Consider using `allow_partial_search_results` setting to bypass this error.]; Will automatically retry [1/-1]org.elasticsearch.action.search.SearchPhaseExecutionException:
    ```
    
    - 한국어 형태소 분석, 초성 검색, 한영 오타 변환 등의 역할 수행
    
    ![Untitled](https://github.com/yesxon/TIL/blob/main/ElasticSearch/imgs/Untitled6.png)
    
    - **토크나이저(nori_tokenizer)**
        - **user_dictionary**: 사용자 정의 사전
        - **decompound_mode**: 복합 명사를 토크나이저가 처리
            - none: 복합명사로 분리하지 않음
            - discard: 복합명사로 분리하고 원본 삭제
            - mixed: 복합명사로 분리하고 원본 유지
    - **토큰 필터**
        - nori_part_of_speech: 품사 태그와 일치하는 토큰 제거
        - nori_readingform: 한자를 한글로 변경
        - nori_number: 한글로 쓰인 숫자를 number로 변경
    
    ```jsx
    PUT nori_poem
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_analyzer": {
              "tokenizer": "my_nori_tokenizer",
              "filter": [
                "nori_posfilter"
              ]
            }
          },
          "tokenizer": {
            "my_nori_tokenizer": {
              "type": "nori_tokenizer",
              "user_dictionary_rules": [
    						//Trouble-shooting 발생
                "라이너마리아릴케,0,14,N"
              ]
            }
          },
          "filter": {
            "nori_posfilter": {
              "type": "nori_part_of_speech",
              "stoptags": [
                "VV",
                "VX",
                "VCP",
                "VCN",
                "MM",
                "MAG",
                "MAJ",
                "IC",
                "JKS",
                "JKC",
                "JKG",
                "JKO",
                "JKB",
                "JKV",
                "JKQ",
                "JX",
                "JC",
                "EP",
                "EF",
                "EC",
                "ETN",
                "ETM",
                "XPN",
                "XSN",
                "XSV",
                "XSA",
                "XR",
                "SF",
                "SP",
                "SE",
                "SL",
                "SH",
                "SN",
                "UNA",
                "NA",
                "VSV"
              ]
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "text": {
            "type": "text",
            "analyzer": "my_analyzer"
          }
        }
      }
    }
    ```
    

### ISSUES

- 윤동주 별 헤는 밤 시 분석할 때 라이너 마리아 릴케를 하나의 토큰으로 사전 정의를 하고자 "user_dictionary_rules"에 추가함,
    1. “라이너 마리아 릴케” > failed, 띄어쓰기가 OR이므로
    2. “라이너마리아릴케” > failed
    3. “라이너 마리아 릴케,0,14,N” (표면형,시작점,길이,품사 형태) > failed, 이름을 모두 담아야하는 라이너가 전체 문장의 길이보다 짧다는 에러가 나옴. 
    - 결론: 스택오버플로우에 검색한 결과 엘라스틱서치는 검색 엔진이라 토큰화 하는 건 가능하지만, 이미 쪼갠 토큰을 이어 붙이는 건 어렵다고 나옴. 해결 방법을 아시는 분은 꼭!! 알려주세요!!
- 에러가 발생해서 nori 플러그인 설치가 안 됐음. 엘라스틱서치 엔진을 멈추고, 열려 있던 bat 파일을 닫아주니 실행됨. 그러나 또 다른 플러그인(kuromoji, smartcn) 설치 과정에서 같은 에러를 마주쳐서 결국 플러그인 zip파일을 내려 받아서 수동설치함!