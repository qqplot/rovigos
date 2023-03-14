# rovigos

## 모델 실행 방법
- 데이터 형식은 `Data/rovigos` 에서 확인하시면 됩니다.
- `recbole` 설치 후 모델 돌릴 때에 로그와 함께 에러가 나면 연락주세요. 

- 실행가능한 모델 목록
- Pop, ConvNCF, SimpleX, BERT4Rec, GRU4Rec, SASRec, LightSANs, SRGNN, S3Rec

- 실행 예시
```sh
python run.py Pop
```


## 데이터 전처리
- `Data/` 경로의 샘플 데이터 예시를 확인해주세요.
- 샘플 데이터만 넣어놨습니다.
- 필요시 `preprocess.py`에서 데이터 경로를 변경하세요. 

```sh
python preprocess.py 
```
