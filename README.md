# PT_shark_chatbot

## 실행 방법

1. 환경 설정
```python
!pip install -r requirements.txt
```
2. API KEY 설정

  .env 파일을 설정하거나
  os.environ으로 설정해주세요

3. 실행
```
streamlit run main.py
```
### 사용 방법
👻 사용 방법  👻 : \n1. 왼쪽의 사이드바에 사용자 정보를 입력하세요.\n2. "(Click) 운동 계획표 받아보기"를 눌러주세요.\n3. 계획표에 대해 궁금한 내용이 있다면, 왼쪽에 "질문하기" 에 입력 후 버튼을 클릭해주세요.\n4. 계획표를 수정하고 싶다면, "계획표 수정하기"를 클릭해주세요.\n5. 구글링할 내용이 있다면, 아래에 "질문하기" 입력 후 버튼을 클릭해주세요.

### 수정 방법
코드 내부의 Template 폼을 수정하여 계획표를 수정합니다.

기존의 포맷 =
```python
template = Template("""
            --- INSTRUCTION ---
            아래의 USER INFO를 바탕으로 계획표를 작성해줘
            1.{workout day}이 아닌 요일은 '휴식'으로 작성해주세요 
            예를들어 월요일, 수요일이 {workout day}이라면 화요일,목요일,금요일,토요일,일요일은 {workout day}이 아닙니다.
            2.계획표는 markdown table 형식으로 작성해줘
            3.{운동 부위}와 {운동 종목}은 자세히 작성해줘
            4.만약 트레이닝 종목이 {헬스}면 {운동 종목}을 2가지를 관련된 링크와 함께 넣어줘
            5.만약 트레이닝 종목이 {요가}면, 요가 동작이 아닌 요가 종류를 링크로 알려줘
            6.만약 트레이닝 종목이 {맨몸운동}이면, calisthenics의 동작 2가지를 링크와 함께 알려줘
            7.계획표는 2주차까지만 작성해줘
            
            

            --- USER INFO ---
            {키} : $height cm
            {몸무게} : $weight kg
            {성별} : $gender
            {나이} : $age
            {운동 경력} : $experience year
            {운동} : $place
            {운동 목적} : $trainer
            {workout day} : $w_plan

            --- RESULT EXAMPLE ---
            트레이닝 종목 : 헬스
            |주차 |요일| 운동 부위 | 운동 종목(+링크) |
            |---|----|------|----------|
            |1|월요일|상체(삼두,어깨)|[벤치프레스](https://www.youtube.com./example "벤치프레스") 40kg 10회 3세트, ...|
            |1|화요일|휴식|  |
            ...
            """
            )
```


  




<img width="700" alt="main page" src="https://github.com/InhwanCho/PT_shark_chatbot/assets/111936229/45038476-c374-4fcd-86cb-b5fbf5ba82ac">

<img width="700" alt="헬스 2주 플랜" src="https://github.com/InhwanCho/PT_shark_chatbot/assets/111936229/08371168-7f71-4f06-a0b3-bde043da05d3">

<img width="700" alt="발화에 의해 수정된 계획표" src="https://github.com/InhwanCho/PT_shark_chatbot/assets/111936229/613d6f0f-374f-4f11-a892-26bbd90218f7">

<img width="700" alt="맨몸 운동 예시" src="https://github.com/InhwanCho/PT_shark_chatbot/assets/111936229/699667e7-c58f-49f2-9cbb-c23f7dd6e872">
