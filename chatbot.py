import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from html import escape
import edge_tts
import asyncio
import os
import uuid

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class CodeAssistantBot:
    def __init__(self):
        self.model = ChatOpenAI(
            model="meta-llama/llama-3.1-405b-instruct:free",
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            temperature=0.6
        )

        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a skilled coding assistant. Use the following context and user input to help."
             " Refer to previous summary and recent interactions to make answers accurate."
             " Keep your response short, relevant, and conversational."),
            ("user",
             "Code: {code}\nInput: {input}\nOutput: {output}\nError: {error}\n"
             "Summary: {summary}\nRecent: {recent}\nQuestion: {question}")
        ])
        self.summary_prompt = ChatPromptTemplate.from_messages([
            ("system", "Summarize key technical points from the conversation so far."),
            ("user", "Conversation: {conversation}")
        ])
        self.voice_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a friendly narrator voice bot. Given a technical answer and its context,"
             " explain it aloud like you're helping someone understand the topic clearly and confidently."
             " Keep your response conversational and short not too long, but not over short."),
            ("user",
             "Code: {code}\nInput: {input}\nOutput: {output}\nError: {error}\n"
             "Conversation so far: {summary}\nAnswer to explain: {answer}")
        ])

    def analyze_code(self, code, input, output, error, question, summary="", history=None):
        parser = StrOutputParser()
        recent = "\n".join([f"User: {q}\nBot: {a}" for q, a in (history or [])[-4:]])
        chain = self.analysis_prompt | self.model | parser
        return chain.invoke({
            'code': code,
            'input': input,
            'output': output,
            'error': error,
            'summary': summary,
            'recent': recent,
            'question': question
        })

    def narrate_response(self, code, input, output, error, answer, summary=""):
        parser = StrOutputParser()
        narration_chain = self.voice_prompt | self.model | parser
        return narration_chain.invoke({
            'code': code,
            'input': input,
            'output': output,
            'error': error,
            'summary': summary,
            'answer': answer
        })

async def text_to_speech(text, filename):
    voice = "fr-FR-VivienneMultilingualNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

def render_chatbot(code, input, output, error):
    st.markdown("""
    <style>
    .chat-container {
        max-height: 60vh;
        overflow-y: auto;
        padding-right: 0.5rem;
        border: 1px solid #ddd;
        border-radius: 8px;
        margin-top: 1rem;
        padding: 1rem;
        background-color: #f9f9f9;
    }
    .chat-message {
        margin-bottom: 1rem;
        word-wrap: break-word;
    }
    .user-message {
        font-weight: bold;
        color: #1a73e8;
    }
    .bot-message pre {
        background-color: #f0f0f0;
        padding: 0.5rem;
        border-radius: 5px;
        overflow-x: auto;
    }
    </style>
    """, unsafe_allow_html=True)

    st.session_state.setdefault('conversation', [])
    st.session_state.setdefault('chat_summary', "")
    st.session_state.setdefault('chat_display_count', 5)
    st.session_state.setdefault('narrated_audio', {})

    c1, c2 = st.columns([4, 1], gap='small')
    with c1:
        question = st.text_input("Ask something about your code...", key="chat_input")
    with c2:
        send = st.button("🚀")

    if send and question:
        bot = CodeAssistantBot()
        history = st.session_state.conversation[-4:]
        summary = st.session_state.chat_summary
        response = bot.analyze_code(code, input, output, error, question, summary, history)
        st.session_state.conversation.append((question, response))
        st.session_state.chat_display_count = 5
        if len(st.session_state.conversation) >= 3:
            try:
                full_chat = "\n".join([f"User: {q}\nBot: {a}" for q, a in st.session_state.conversation[-10:]])
                summarizer = bot.summary_prompt | bot.model | StrOutputParser()
                st.session_state.chat_summary = summarizer.invoke({'conversation': full_chat})
            except:
                pass

    total = len(st.session_state.conversation)
    start = max(0, total - st.session_state.chat_display_count)
    visible = list(reversed(st.session_state.conversation[start:]))

    for idx, (q, a) in enumerate(visible):
        st.markdown(f'<div class="chat-message user-message">{escape(q)}</div>', unsafe_allow_html=True)

        def format_response(txt):
            parts = txt.split('```')
            result = ''
            for j, part in enumerate(parts):
                if j % 2 == 1:
                    lines = part.splitlines()
                    if lines and lines[0].isalpha():
                        lines = lines[1:]
                    code_html = escape("\n".join(lines))
                    result += f'<pre><code>{code_html}</code></pre>'
                else:
                    result += escape(part)
            return result

        formatted = format_response(a)
        st.markdown(f'<div class="chat-message bot-message">{formatted}</div>', unsafe_allow_html=True)

        audio_file = st.session_state.narrated_audio.get((q, a))
        if not audio_file:
            if st.button("🔊 Narrate", key=f"narrate_{idx}"):
                status_placeholder = st.empty()
                status_placeholder.info("🧠 Generating narration...")
                bot = CodeAssistantBot()
                narration = bot.narrate_response(code, input, output, error, a, st.session_state.chat_summary)
                status_placeholder.info("🎙️ Converting to audio...")
                audio_file = f"audio_{uuid.uuid4().hex}.mp3"
                asyncio.run(text_to_speech(narration, audio_file))
                st.session_state.narrated_audio[(q, a)] = audio_file
                status_placeholder.success("🔊 Narration ready!")
                st.audio(audio_file, format="audio/mp3", autoplay=True)
        else:
            st.audio(audio_file, format="audio/mp3", autoplay=False)

    if start > 0 and st.button("🔽 Show more"):
        st.session_state.chat_display_count += 5
        st.rerun()

    st.markdown("""
    <script>
    const c = window.parent.document.querySelector('.chat-container');
    if (c) c.scrollTop = c.scrollHeight;
    </script>
    """, unsafe_allow_html=True)