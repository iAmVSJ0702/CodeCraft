---
title: Pro Code Playground
emoji: 💻
colorFrom: indigo
colorTo: blue
sdk: streamlit
sdk_version: 1.47.0
app_file: app.py
pinned: true
---

# 💻 Pro Code Playground

**Pro Code Playground** is an interactive, multi-language coding environment with a built-in AI assistant and live execution — all accessible directly from your browser.

Powered by Hugging Face Spaces, Streamlit, and Groq’s LLaMA 3.3–70B, this project merges code editing, language support, AI debugging, and even narration in a single clean, responsive app. No installations. No setup. Just code, ask, listen, and learn.

---

## 🔥 Features

- 🧠 AI-powered Code Assistant via **Groq + LangChain**
- ✍️ Support for **Python, Java, C++, C, JavaScript, C#**
- 📤 File upload with **auto language detection**
- 📥 Stdin simulation for programs needing user input
- 🔊 **Voice narration** of assistant responses (Edge TTS)
- 💬 Scrollable chatbot with memory and summarization
- 🌓 **Dark/light theme toggle** with instant styling
- 💾 One-click code download with proper extension
- 🧪 Runtime stats (execution time, memory used)

---

## 🚀 Try It Live

👉 [Click here to run it](https://huggingface.co/spaces/vsj0702/Code_editor)  
No login or install required — it runs right in your browser.

---

# 📘 Usage Guide

### 🌙 1. Toggle Light/Dark Theme

- Click the theme button (🌙 or ☀️) on the top-right to switch between dark and light modes.
- Styling is fully dynamic and applies instantly to all components including the code editor and chat.

---

### 🧑‍💻 2. Select a Language

- Choose from: Python, Java, C, C++, JavaScript, or C#
- Language auto-switches when uploading supported files

---

### 📝 3. Write or Upload Code

- Start writing code directly in the editor
- Or upload a file: `.py`, `.cpp`, `.c`, `.java`, `.js`, `.cs`, `.txt`
- The editor auto-switches to the detected language

---

### 🧪 4. Input (stdin)

- Use the **Input (stdin)** text box for user inputs
- Inputs are passed line-by-line to your code

---

### ▶️ 5. Run the Code

- Hit **▶️ Run**
- Output is shown in a result panel
- Errors are displayed separately in red
- Runtime and memory stats appear below the result

---

### 💬 6. Ask the AI Assistant

- Use the chat sidebar to ask anything about your code
- The AI uses full context (code, input, output, errors, history)
- Great for debugging, refactoring, or learning

---

### 🔊 7. Narrate Responses

- Click "🔊 Narrate" to generate a voice explanation of the AI’s answer
- Plays using Edge TTS voices
- You can replay the audio or skip it

---

### 💾 8. Download Your Code

- Download the edited code anytime
- File is automatically named with the correct extension

---

# 🌳 File Structure: Think of It Like a Tree

Imagine your app like a growing tree.

At the **trunk**, there’s `app.py` — the brain of your app. Everything connects to it, and it sends life (data, layout, session state) to all other components. From this trunk, other files branch out like **modules**, each handling a specific responsibility. The result? A modular, clean, powerful structure that makes debugging and extending your app a breeze.

---

### 🌲 `app.py` — The Trunk of the Tree

This is the **entry point** of the application — the first file Streamlit runs. Think of it as the control center. Its responsibilities include:

- Setting page layout and title
- Initializing theme and session state
- Dividing the screen into columns
- Calling the editor module (`code_editor.py`) on the left
- Calling the chatbot module (`chatbot.py`) on the right

**Without this file, nothing would render.** It acts as the coordinator, delegating tasks to the appropriate submodules like a team lead.

---

### 🌿 `code_editor.py` — The Code Branch

This file handles everything related to writing and running code. It’s like the **workbench** where users type, upload, and execute their programs.

Key responsibilities:
- Displaying the code editor using `streamlit_ace`
- Handling file uploads and auto-detecting language
- Taking user input (stdin)
- Running code via the backend (local or OneCompiler API)
- Showing output, errors, runtime, and memory stats
- Offering code download with the correct extension

It’s tightly integrated with `utils.py`, which handles the actual logic for compiling and executing the code.

---

### 🌿 `chatbot.py` — The Smart Brain Branch

This file gives your app its **AI assistant powers**. It's responsible for:

- Talking to Groq's LLaMA 3.3 model via LangChain
- Generating code explanations, debugging suggestions, and summaries
- Managing a memory-aware chat history
- Handling narration of responses using Edge TTS
- Controlling how chatbot responses are shown (Markdown + CSS)
- Making sure your assistant sounds human-like, helpful, and context-aware

It’s the most dynamic and intelligent part of the app — and beautifully modular.

---

### 🌿 `layout.py` — The Skin and Styling Layer

This file controls the **aesthetic** of your app. It defines:

- Light and dark themes
- Custom CSS injected into Streamlit
- Fonts, button styles, scroll behavior, sidebar visuals
- Consistent layout feel across components

Whenever the user toggles dark mode, `layout.py` updates everything instantly. It makes your app look polished and consistent, like a professionally built product.

---

### 🌿 `utils.py` — The Engine Room

This is your app’s **execution engine**.

It abstracts the messy stuff — compiling, running, capturing outputs, handling errors — so that the rest of the app stays clean.

Responsibilities include:
- Executing Python code using `exec()` with stdin override
- Compiling and running C/C++ code via `gcc`/`g++`
- Sending Java, JavaScript, and C# code to OneCompiler API
- Gracefully falling back between API keys if one fails
- Returning outputs, stderr, and exceptions for display

If `code_editor.py` is the workbench, this file is the **machine under the hood**.

---

### 🌿 `requirements.txt` — The DNA

This file contains all the dependencies needed to run the app.

From Streamlit to LangChain, Edge TTS to Groq’s SDK — this file ensures your app has all the tools it needs to function.

---

### 🌱 Summary: A Living, Breathing System

Every file has a job. Every module connects like a healthy tree:

- `app.py` = Trunk (controls everything)
- `layout.py` = Skin and theme
- `code_editor.py` = Workbench for code
- `utils.py` = Engine for execution
- `chatbot.py` = Brain for intelligence
- `requirements.txt` = Genetic blueprint

This modular structure lets you:
- Debug easily
- Extend individual parts without breaking others
- Understand how data flows
- Keep your code organized and clean

---

If you’re reading this to understand or contribute — welcome aboard! The structure is made for developers like you.

Feel free to explore each module and give feedback 🙌

---

## 👤 Author

**Vaibhav Shankar (vsj0702)**  
📧 Email: [vsj0702@gmail.com](mailto:vsj0702@gmail.com)  
🔗 LinkedIn: [vaibhavshankar](https://www.linkedin.com/in/vaibhavshankar?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)  
🤗 Hugging Face: [@vsj0702](https://huggingface.co/vsj0702)

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0 (GVL-3)**.  
You are free to use, modify, and distribute the project under the terms of this license.

---

Thanks for exploring **Pro Code Playground** 💻  
Let me know what you build with it!