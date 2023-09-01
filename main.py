import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
from string import Template
from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage


# API키 설정 load_dotenv로 할 경우 비활성화
# os.environ['OPENAI_API_KEY']  = '...'
# os.environ['SERPAPI_API_KEY'] = '...'
    
def init():
    # API_KEY를 '.env'파일에서 받아오기
    load_dotenv()

    # 페이지 세팅
    st.set_page_config(
        page_title="Personal Trainer Shark!",
        page_icon="🦈"
    )

def sidebar():
    # 운동 계획표를 만들기위한 템플릿 생성
    
    w_plan = st.sidebar.multiselect('원하는 운동 요일을 입력해주세요 (다중 선택)',['월요일','화요일','수요일','목요일','금요일','토요일','일요일'])
    gender = st.sidebar.selectbox('성별을 입력해주세요',('남성', '여성'))
    height = st.sidebar.number_input('키(cm)를 입력해주세요',value=175)
    weight = st.sidebar.number_input('몸무게(kg)를 입력해주세요',value=70)
    age = st.sidebar.number_input('나이를 입력해 주세요',value= 30)
    experience = st.sidebar.number_input('운동 경력(년)을 입력해 주세요',value= 1)
    # 템플릿 설정
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

    return template.substitute(height=height,weight=weight,gender=gender,age=age,experience=experience,w_plan=w_plan,place=place,trainer=trainer)

def main():
    init()
    
    # 템플릿에 필요한 함수 전역변수로 설정
    global place,trainer
    # radio형식의 출력포멧을 수직 -> 수평으로 바꿔줌
    st.sidebar.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    st.sidebar.header('당신의 정보를 입력해 주세요.')
    place = st.sidebar.radio('트레이닝의 종목을 입력해주세요', options=['헬스','요가', '맨몸운동'])
    trainer = st.sidebar.radio('원하는 트레이닝 목적을 선택해주세요.', options=('무게증량','유연성 증가','재활운동','체형교정','체중감소','건강'))

    # LLM 모델 설정
    chat = ChatOpenAI(temperature=0.1,max_tokens=1024,model='gpt-3.5-turbo')
    
    # 최종 출력을 위한 메시지 세션 활성화
    # GPT모델의 역할 부여 
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=f"당신은 {place}의 {trainer}을 위한 트레이너입니다.")
        ]
        st.session_state.users = []
    
        
    
    st.header("🦈 Personal Trainer Shark! 🦈")
    st.info('👻 사용 방법  👻 : \n1. 왼쪽의 사이드바에 사용자 정보를 입력하세요.\n2. "(Click) 운동 계획표 받아보기"를 눌러주세요.\n3. 계획표에 대해 궁금한 내용이 있다면, 왼쪽에 "질문하기" 에 입력 후 버튼을 클릭해주세요.\n4. 계획표를 수정하고 싶다면, "계획표 수정하기"를 클릭해주세요.\n5. 구글링할 내용이 있다면, 아래에 "질문하기" 입력 후 버튼을 클릭해주세요.')


    # 사이드바 설정
    with st.sidebar:
        templ = sidebar()
        result = st.sidebar.button("(Click) 운동 계획표 받아보기",type='primary')
        if result :
            # 출력을 위한 user message
            
            st.session_state.messages.append(HumanMessage(content=templ))
            st.session_state.users.append('skip')
            
            
            # 로딩 시 활성화 문구 작성
            with st.spinner("계획표 작성 중입니다."):
                # 출력을 위한 AI message
                response = chat(st.session_state.messages)
            
            st.session_state.users.append('planner')
        
            st.session_state.messages.append(
                AIMessage(content=response.content))

        # sidebar로 챗봇 질문할 경우 활성화
        with st.sidebar.form('form', clear_on_submit=True):
            user_input = st.text_input('계획표에 대해 질문하기 & 수정하기 : ', '', key='user_input')
            submitted = st.form_submit_button('질문하기', type='primary')
            edit = st.form_submit_button('계획표 수정하기', type='primary')

        # 계획표에 대해 질문하기
        if submitted and user_input:
            # 유저 질문
            st.session_state.messages.append(HumanMessage(content=user_input))
            st.session_state.users.append('user')

            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            
            # AI답변
            st.session_state.messages.append(AIMessage(content=response.content))
            st.session_state.users.append('chatbot')
        # 계횩회에 대해 수정하기
        if user_input and edit :
            st.session_state.messages.append(HumanMessage(content=user_input))
            st.session_state.users.append('user')
            
            # 로딩 시 활성화 문구 작성
            with st.spinner("계획표 수정 중입니다."):
                # 출력을 위한 AI message
                response = chat(st.session_state.messages)
            
            st.session_state.users.append('planner')
        
            st.session_state.messages.append(
                AIMessage(content=response.content))
    
    # 질문을 입력하기위한 폼 생성
    with st.form('additional_questions_form',clear_on_submit=True):
        placeholder_text_additional = "질문을 입력해주세요"
        query = st.text_area('질문하기 : ',value="", help="", key="additional_input", placeholder=placeholder_text_additional)    
        submitted = st.form_submit_button(label='보내기')
    
        if submitted and query:
            # serpapi를 활용하기 위한 포맷 작성
            llm = OpenAI(temperature=0,max_tokens=512)
            tool_names = ["serpapi"]
            tools = load_tools(tool_names)
            agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
            # 유저 질문
            st.session_state.messages.append(query)
            st.session_state.users.append('serpapi_user')
            with st.spinner("Thinking..."):
                # serpapi 답변
                response = agent.run(query)
            st.session_state.messages.append(response)
            st.session_state.users.append('serpapi_chatbot')

            # # GPT 답변으로 변경 시
            # st.session_state.messages.append(HumanMessage(content=query))
            # with st.spinner("Thinking..."):
            #     response = chat(st.session_state.messages)
            # st.session_state.messages.append(
            #     AIMessage(content=response.content))

    
    # 출력을 위한 메시지 히스토리 활성
    messages = st.session_state.get('messages', [])
    users = st.session_state.users
    
    for i, (user, msg) in enumerate(zip(users,messages[1:])):
        if user == 'skip':
            continue
        elif user == 'chatbot':
            message(msg.content, is_user=False, key=str(i)+'_ai')
        elif user == 'user' :
            message(msg.content, is_user=True, key=str(i)+'_user')
        elif user == 'planner':
            st.markdown(msg.content)
        elif user == 'serpapi_user':
            message(msg, is_user = True, key=str(i)+'_user')
        elif user == 'serpapi_chatbot':
            message(msg, is_user=False, key=str(i)+'_ai')

if __name__ == '__main__':
    main()
