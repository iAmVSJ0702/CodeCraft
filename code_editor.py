# code_editor.py

import streamlit as st
import streamlit_ace as st_ace
import os
import time, psutil
from pathlib import Path
from utils import execute_code

# Default code snippets
DEFAULT_SNIPPETS = {
    "Python": '''# default code\na = int(input())\nb = int(input())\nprint("Sum:", a + b)''',
    "C": '''// default code\n#include <stdio.h>\nint main() {\n    int a, b;\n    scanf("%d %d", &a, &b);\n    printf("Sum: %d\\n", a + b);\n    return 0;\n}''',
    "C++": '''// default code\n#include <iostream>\nusing namespace std;\nint main() {\n    int a, b;\n    cin >> a >> b;\n    cout << "Sum: " << a + b << endl;\n    return 0;\n}''',
    "Java": '''// default code\nimport java.util.Scanner;\npublic class Program {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int a = sc.nextInt();\n        int b = sc.nextInt();\n        System.out.println("Sum: " + (a + b));\n    }\n}''',
    "JavaScript": '''// default code\nconst readline = require('readline');\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet inputs = [];\nrl.on('line', (line) => {\n  inputs.push(parseInt(line));\n  if (inputs.length === 2) {\n    console.log("Sum:", inputs[0] + inputs[1]);\n    rl.close();\n  }\n});''',
    "C#": '''// default code\nusing System;\npublic class Program {\n    public static void Main(string[] args) {\n        int a = Convert.ToInt32(Console.ReadLine());\n        int b = Convert.ToInt32(Console.ReadLine());\n        Console.WriteLine("Sum: " + (a + b));\n    }\n}'''
}

# Extension-to-language mapping
EXT_LANG_MAP = {
    ".py": "Python",
    ".cpp": "C++",
    ".c": "C",
    ".java": "Java",
    ".js": "JavaScript",
    ".cs": "C#"
}

def render_code_editor(ace_theme):
    # ── Language Selector ──────────────────────────────
    lang_list = list(DEFAULT_SNIPPETS.keys())
    default_lang = st.session_state.get("language", "Python")
    selected_lang = st.selectbox("Language", lang_list, index=lang_list.index(default_lang))
    st.session_state.language = selected_lang
    editor_key = f"editor_{selected_lang}"

    # ── File Upload ──────────────────────────────
    uploaded_file = st.file_uploader("📤 Upload file", type=["py", "cpp", "c", "java", "js", "cs", "txt"])

    if uploaded_file:
        if uploaded_file.size > 10 * 1024 * 1024:
            st.error("🚫 File too large. Max allowed is 10MB.")
        else:
            content = uploaded_file.read().decode("utf-8", errors="ignore")
            filename = uploaded_file.name
            ext = Path(filename).suffix.lower()

            prev_name = st.session_state.get("uploaded_file_name")
            prev_content = st.session_state.get("uploaded_file_content")

            # Only react to new uploads
            if content != prev_content or filename != prev_name:
                st.session_state.uploaded_file_name = filename
                st.session_state.uploaded_file_content = content

                detected_lang = EXT_LANG_MAP.get(ext)
                if detected_lang:
                    st.session_state.language = detected_lang
                    st.session_state.prev_language = detected_lang
                    st.session_state.code = content
                    st.toast(f"✅ Auto-switched to {detected_lang}", icon="🔄")
                    st.rerun()
                elif ext == ".txt":
                    st.session_state.code = content
                    st.toast("📄 Loaded text file", icon="📄")
                else:
                    st.error("❌ Unsupported file format.")
                    return

    # ── Fallback Default Code ──────────────────────────────
    prev_lang = st.session_state.get("prev_language")
    default_code = DEFAULT_SNIPPETS[selected_lang]

    if (
        st.session_state.get("code") is None
        or st.session_state.code.strip() == ""
        or selected_lang != prev_lang
        or st.session_state.code.strip() == DEFAULT_SNIPPETS.get(prev_lang, "")
    ):
        st.session_state.code = default_code
        st.session_state.prev_language = selected_lang

    # ── ACE Code Editor ──────────────────────────────
    code = st_ace.st_ace(
        value=st.session_state.code,
        placeholder=f"Start typing your {selected_lang} code…",
        language=selected_lang.lower() if selected_lang != "C++" else "c_cpp",
        theme=ace_theme,
        keybinding="vscode",
        font_size=14,
        min_lines=20,
        show_gutter=True,
        wrap=True,
        auto_update=True,
        key=editor_key
    )

    if code != st.session_state.code:
        st.session_state.code = code

    # ── Stdin Input ──────────────────────────────
    user_input = st.text_area(
        "📥 Input (stdin)",
        value=st.session_state.stdin,
        height=100,
        placeholder="Enter input values, one per line",
        key="stdin_input"
    )
    if user_input != st.session_state.stdin:
        st.session_state.stdin = user_input

    # ── Run Button ──────────────────────────────
    if st.button("▶️ Run"):
        start_time = time.perf_counter()
        process = psutil.Process()
        mem_before = process.memory_info().rss

        out, err, exc = execute_code(
            code=st.session_state.code,
            stdin=st.session_state.stdin,
            language=selected_lang
        )

        exec_time = time.perf_counter() - start_time
        mem_after = process.memory_info().rss
        mem_used = (mem_after - mem_before) / 1024

        st.session_state.code_output = out
        st.session_state.error_output = err or exc

        st.text_area("📤 Output", out or "(no output)", height=120)
        if err or exc:
            st.error(err or exc)
        st.markdown(f"⏱️ **Execution Time:** {exec_time:.4f}s")
        st.markdown(f"💾 **Memory Used:** {mem_used:.2f} KB")

    # ── Download Code ──────────────────────────────
    if st.session_state.code:
        lang_ext = {
            "Python": "py", "C": "c", "C++": "cpp", "Java": "java",
            "JavaScript": "js", "C#": "cs"
        }
        ext = lang_ext.get(selected_lang, "txt")

        st.download_button(
            label="💾 Download Code",
            data=st.session_state.code,
            file_name=f"code.{ext}",
            mime="text/plain"
        )