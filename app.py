from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


st.title("こどもの医療・健康相談 受付アプリ")
st.write("####動作モード1: 保育・子育ての相談受付")
st.write("入力フォームにテキストを入力し、「実行」ボタンを押すことで保育・子育ての相談を受け付けます。")
st.write("####動作モード2: 医療・健康相談受付")
st.write("入力フォームにテキストを入力し、「実行」ボタンを押すことで医療・健康相談を受け付けます。")

selected_item = st.radio(
    "動作モードを選択してください。",
    ["保育・子育ての相談受付", "医療・健康相談受付"]
)
st.divider()

if selected_item == "保育・子育ての相談受付":
    st.header("保育・子育ての相談受付モード")
    input_message = st.text_input(label="相談内容を入力してください。")

else: # selected_item == "医療・健康相談受付"
    st.header("医療・健康相談受付モード")
    input_message = st.text_input(label="相談内容を入力してください。")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=1,
)


def generate_response(mode, message):
    if mode == "保育・子育ての相談受付":
        system_prompt = "あなたは優秀な保育士です。以下の相談内容に対して、親身になってアドバイスを提供してください。"
    elif mode == "医療・健康相談受付":
        system_prompt = "あなたは優秀な小児科医です。以下の相談内容に対して、専門的かつ分かりやすいアドバイスを提供してください。"
    else:
        system_prompt = (
            "あなたは保護者向けに、子どもの健康と育ちについてわかりやすく説明するアシスタントです。"
            "一般的な情報提供にとどめ、最終判断は必ず医師・専門職に委ねるように促してください。"
        )
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=message),
    ]

    response = llm.invoke(messages)
    return response.content

if st.button("実行"):
    st.divider()
    if selected_item == "保育・子育ての相談受付":
        if input_message:
            st.write(f"保育・子育ての相談内容: **{input_message}**")
            ai_answer = generate_response(selected_item, input_message)
            st.write("### LLMからの回答")
            st.write(ai_answer)
        else:
            st.write("相談内容が入力されていません。")
    else: # selected_item == "医療・健康相談受付"
        if input_message:
            st.write(f"医療・健康相談内容: **{input_message}**")
            ai_answer = generate_response(selected_item, input_message)
            st.write("### LLMからの回答")
            st.write(ai_answer)
        else:
            st.write("相談内容が入力されていません。")
