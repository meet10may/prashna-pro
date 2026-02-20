"""
PrashnaPro — प्रश्नप्रो
Handwritten Question Papers → Professional Print-Ready Documents
"""

import streamlit as st
import os, json, tempfile
from datetime import datetime

st.set_page_config(page_title="PrashnaPro", page_icon="📄", layout="wide", initial_sidebar_state="collapsed")

# ═══════════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM — Apple HIG inspired
# Clarity · Deference · Depth
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Canvas ── */
.stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #f5f5f7;
    -webkit-font-smoothing: antialiased;
}

/* Remove top whitespace */
.stMainBlockContainer { padding-top: 1rem !important; }
.block-container { padding-top: 1rem !important; }

/* ── App Header ── */
.pp-header {
    background: #fff;
    padding: 20px 28px;
    border-radius: 16px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 0 0 1px rgba(0,0,0,0.03);
}
.pp-logo {
    width: 44px; height: 44px; border-radius: 11px; flex-shrink: 0;
    background: linear-gradient(135deg, #5e5ce6, #bf5af2);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 2px 8px rgba(94,92,230,0.25);
}
.pp-logo svg { width: 24px; height: 24px; }
.pp-title { font-size: 1.25rem; font-weight: 700; color: #1d1d1f; letter-spacing: -0.3px; margin: 0; }
.pp-subtitle { font-size: 0.78rem; color: #86868b; font-weight: 400; margin: 2px 0 0 0; }

/* ── Step Bar ── */
.pp-steps {
    display: flex; justify-content: center; gap: 6px;
    margin: 0 0 20px 0; padding: 0;
}
.pp-step {
    font-size: 0.7rem; font-weight: 600; padding: 5px 14px;
    border-radius: 100px; letter-spacing: 0.01em;
    font-family: 'Inter', sans-serif;
}
.pp-step-active { background: #5e5ce6; color: #fff; }
.pp-step-done { background: #e8e8ed; color: #1d1d1f; }
.pp-step-wait { background: transparent; color: #c7c7cc; }

/* ── Section bar (editor) ── */
.pp-sec {
    background: #f5f5f7; border-radius: 10px; padding: 10px 14px;
    margin: 14px 0 8px 0; font-weight: 600; font-size: 0.82rem;
    color: #1d1d1f; letter-spacing: -0.1px;
    border-left: 3px solid #5e5ce6;
}

/* ── Question card ── */
.pp-qcard {
    background: #fff; border: 1px solid #e8e8ed; border-radius: 12px;
    padding: 12px 14px; margin: 6px 0;
}

/* ── Paper Preview ── */
.pp-paper {
    background: #fff; color: #1d1d1f; padding: 28px 32px; border-radius: 12px;
    border: 1px solid #e8e8ed; font-family: 'Times New Roman', 'Georgia', serif;
    line-height: 1.55; font-size: 0.84rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.04);
}
.pp-paper h2 { text-align: center; font-size: 1.05rem; margin: 0; color: #1d1d1f; font-weight: 700; }
.pp-paper h3 { text-align: center; font-size: 0.9rem; margin: 2px 0; color: #48484a; font-weight: 600; }
.pp-paper-meta {
    display: flex; justify-content: space-between; font-size: 0.78rem; color: #636366;
    margin: 8px 0; padding: 6px 0; border-top: 1px solid #e5e5ea; border-bottom: 1px solid #e5e5ea;
}
.pp-paper-sec {
    font-weight: 700; text-align: center; font-size: 0.85rem;
    margin: 12px 0 6px 0; text-transform: uppercase; color: #1d1d1f;
    letter-spacing: 0.4px;
}
.pp-paper-q { display: flex; justify-content: space-between; margin: 4px 0; font-size: 0.84rem; }
.pp-paper-m { font-weight: 700; white-space: nowrap; min-width: 28px; text-align: right; color: #636366; }
.pp-paper-sp { margin-left: 20px; font-size: 0.8rem; color: #48484a; }

/* ── Hindi tool ── */
.pp-hindi-bar {
    background: #f5f5f7; border-radius: 10px; padding: 8px 12px;
    font-size: 0.78rem; color: #636366; margin: 4px 0;
}

/* ── Success ── */
.pp-success {
    background: #fff; border-radius: 16px; padding: 32px; text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 0 0 1px rgba(0,0,0,0.03);
    margin: 12px 0;
}
.pp-success-icon {
    width: 56px; height: 56px; border-radius: 50%; margin: 0 auto 12px;
    background: linear-gradient(135deg, #30d158, #34c759);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 12px rgba(52,199,89,0.25);
}
.pp-success h2 { color: #1d1d1f; font-size: 1.3rem; font-weight: 700; margin: 0; letter-spacing: -0.3px; }
.pp-success p { color: #86868b; font-size: 0.85rem; margin: 4px 0 0 0; }

/* ── Streamlit overrides ── */
#MainMenu, footer, header {visibility: hidden;}
.stTextArea textarea {
    font-size: 0.85rem !important; border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important; border: 1px solid #d1d1d6 !important;
}
.stTextInput input {
    font-size: 0.85rem !important; border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important; border: 1px solid #d1d1d6 !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #5e5ce6 !important; box-shadow: 0 0 0 3px rgba(94,92,230,0.12) !important;
}
.stButton > button[kind="primary"] {
    background: #5e5ce6 !important; border: none !important; border-radius: 10px !important;
    font-weight: 600 !important; font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important; padding: 8px 20px !important;
    box-shadow: 0 1px 4px rgba(94,92,230,0.2) !important;
}
.stButton > button[kind="primary"]:hover { background: #4e4cd2 !important; }
.stButton > button {
    border-radius: 10px !important; font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.85rem !important;
    border: 1px solid #d1d1d6 !important; color: #1d1d1f !important;
}
.stProgress > div > div > div { background: #5e5ce6 !important; }
/* Hide sidebar entirely */
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }

/* Settings toolbar spacing */
.pp-toolbar-spacer { height: 4px; }
div[data-testid="stExpander"] { border: 1px solid #e8e8ed !important; border-radius: 12px !important; }
.stCaption { color: #86868b !important; }
.stMarkdown h3, .stMarkdown h4, .stMarkdown h5 {
    font-family: 'Inter', sans-serif !important; color: #1d1d1f !important;
    letter-spacing: -0.2px !important;
}
</style>
""", unsafe_allow_html=True)

# ─── State ─────────────────────────────────────────────────────────────────────
defaults = {"step": 0, "structured_data": None, "raw_text": None, "docx_path": None, "error": None}
for k, v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="pp-header">
    <div class="pp-logo">
        <svg viewBox="0 0 24 24" fill="none"><path d="M4 4h10l4 4v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" fill="rgba(255,255,255,0.9)"/><path d="M14 4l4 4h-4V4z" fill="rgba(255,255,255,0.6)"/><path d="M8 13h6M8 16h4" stroke="rgba(94,92,230,0.5)" stroke-width="1.2" stroke-linecap="round"/></svg>
    </div>
    <div>
        <p class="pp-title">PrashnaPro <span style="font-weight:400;color:#86868b;font-size:0.85rem;">प्रश्नप्रो</span></p>
        <p class="pp-subtitle">AI tool that converts photos of handwritten papers into structured, polished, print-ready exam documents</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Steps ────────────────────────────────────────────────────────────────────
labels = ["Upload", "Details", "Process", "Edit", "Download"]
bar = '<div class="pp-steps">'
for i, l in enumerate(labels):
    c = "pp-step-done" if i < st.session_state.step else ("pp-step-active" if i == st.session_state.step else "pp-step-wait")
    bar += f'<span class="pp-step {c}">{l}</span>'
bar += '</div>'
st.markdown(bar, unsafe_allow_html=True)

# ─── Settings Row (inline, no sidebar) ────────────────────────────────────────
_sc1, _sc2, _sc3, _sc4, _sc5 = st.columns([2, 1.5, 1, 1.2, 1.2])
with _sc1:
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...", label_visibility="collapsed")
with _sc2:
    model_choice = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-mini"], label_visibility="collapsed")
with _sc3:
    compact_mode = st.checkbox("Compact", value=True, help="Save paper")
with _sc4:
    if st.button("Load demo", use_container_width=True):
        st.session_state.structured_data = {
            "exam_title": "Half Yearly Examination 2024-25", "class": "IX",
            "subject": "Social Science", "time": "3 Hours", "total_marks": "80",
            "instructions": ["All questions are compulsory.",
                "This paper has 5 sections — A, B, C, D and E.",
                "Section A has 20 MCQs carrying 1 mark each.",
                "Section B has 5 questions carrying 2 marks each.",
                "Draw neat diagrams wherever required."],
            "sections": [
                {"section_name": "Section A — Multiple Choice Questions",
                 "questions": [
                    {"number":"1","text":"Which of the following is NOT a feature of democracy?","marks":"1",
                     "subparts":["(a) Elected representatives","(b) Free and fair elections","(c) Military rule","(d) Rule of law"]},
                    {"number":"2","text":"The French Revolution began in:","marks":"1",
                     "subparts":["(a) 1776","(b) 1789","(c) 1799","(d) 1804"]},
                    {"number":"3","text":"भारत का सबसे लंबा समुद्र तट किस राज्य में है?","marks":"1",
                     "subparts":["(a) केरल","(b) गुजरात","(c) तमिलनाडु","(d) महाराष्ट्र"]}]},
                {"section_name": "Section B — Short Answer",
                 "questions": [
                    {"number":"21","text":"Describe any three features of the Indian Constitution.","marks":"2","subparts":[]},
                    {"number":"22","text":"भारत की प्रमुख नदियों के नाम बताइए।","marks":"2","subparts":[]}]},
                {"section_name": "Section C — Long Answer",
                 "questions": [
                    {"number":"26","text":"Match the following:","marks":"4",
                     "subparts":["(i) Tundra\tExtremely cold","(ii) Monsoon\tSeasonal rainfall",
                                 "(iii) Desert\tHot and dry","(iv) Equatorial\tHot and humid"]},
                    {"number":"27","text":"Explain the storming of the Bastille.","marks":"5",
                     "subparts":["(a) Political significance","(b) Social impact","(c) Symbolic meaning"]}]}
            ]}
        st.session_state.raw_text = "(Demo)"
        st.session_state.school_name = "Delhi Public School"
        st.session_state.step = 3; st.rerun()
with _sc5:
    if st.button("Start over", use_container_width=True):
        for k in defaults: st.session_state[k] = defaults[k]
        st.rerun()

# ─── Helpers ──────────────────────────────────────────────────────────────────
def render_preview(data):
    h = '<div class="pp-paper">'
    school = st.session_state.get("school_name","")
    if school: h += f'<h2>{school.upper()}</h2>'
    if data.get("exam_title"): h += f'<h3>{data["exam_title"]}</h3>'
    ml, mr = [], []
    if data.get("class"): ml.append(f'Class: <b>{data["class"]}</b>')
    if data.get("subject"): ml.append(f'Subject: <b>{data["subject"]}</b>')
    if data.get("time"): mr.append(f'Time: <b>{data["time"]}</b>')
    if data.get("total_marks"): mr.append(f'Max Marks: <b>{data["total_marks"]}</b>')
    if ml or mr:
        h += f'<div class="pp-paper-meta"><span>{" &nbsp;·&nbsp; ".join(ml)}</span><span>{" &nbsp;·&nbsp; ".join(mr)}</span></div>'
    if data.get("instructions"):
        h += '<div style="margin:6px 0;font-size:0.76rem;color:#48484a"><b>General Instructions:</b><br>'
        for i,ins in enumerate(data["instructions"],1): h += f'<span style="color:#636366">{i}.</span> {ins}<br>'
        h += '</div><hr style="border:none;border-top:1px solid #e5e5ea;margin:8px 0">'
    for si, sec in enumerate(data.get("sections",[])):
        h += f'<div class="pp-paper-sec">{sec.get("section_name","")}</div>'
        for qi, q in enumerate(sec.get("questions",[])):
            m = f'<span class="pp-paper-m">[{q["marks"]}]</span>' if q.get("marks") else ''
            h += f'<div class="pp-paper-q"><span><b>Q{q["number"]}.</b> {q["text"]}</span>{m}</div>'
            for sp in q.get("subparts",[]): h += f'<div class="pp-paper-sp">{sp}</div>'
            if st.session_state.get(f"img_{si}_{qi}"):
                import base64
                img_b64 = base64.b64encode(st.session_state[f"img_{si}_{qi}"]).decode()
                h += f'<div style="margin:6px 0 6px 20px;"><img src="data:image/png;base64,{img_b64}" style="max-width:60%;max-height:180px;border-radius:4px;border:1px solid #e5e5ea;"/></div>'
    h += '<hr style="border:none;border-top:1px solid #e5e5ea;margin:10px 0">'
    h += '<div style="text-align:center;color:#aeaeb2;font-size:0.72rem;font-style:italic">End of Question Paper</div></div>'
    return h

def generate_docx(data):
    from formatter import create_question_paper, generate_filename
    td = tempfile.mkdtemp(); fn = generate_filename(data); op = os.path.join(td, fn)
    lp = None
    if st.session_state.get("logo_file"):
        lp = os.path.join(td,"logo.png")
        with open(lp,'wb') as f: f.write(st.session_state.logo_file.getbuffer())
    
    # Collect question images: dict of "si_qi" -> image_path
    q_images = {}
    for si, sec in enumerate(data.get("sections", [])):
        for qi, q in enumerate(sec.get("questions", [])):
            img_data = st.session_state.get(f"img_{si}_{qi}")
            if img_data:
                img_path = os.path.join(td, f"qimg_{si}_{qi}.png")
                with open(img_path, 'wb') as f: f.write(img_data)
                q_images[f"{si}_{qi}"] = img_path
    
    create_question_paper(data, op, school_name=st.session_state.get("school_name",""),
        logo_path=lp, compact=compact_mode, question_images=q_images)
    st.session_state.docx_path = op; st.session_state.docx_filename = fn

def hindi_tool():
    st.markdown('<div class="pp-hindi-bar">Type in English, press <b>Space</b> to convert each word. Use arrow keys to pick alternatives.</div>', unsafe_allow_html=True)
    st.components.v1.html("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <div style="font-family:'Inter',sans-serif; padding:4px 0;">
        <div style="position:relative; margin-bottom:10px;">
            <input id="hi" type="text" autocomplete="off" spellcheck="false"
                placeholder="Type here… e.g. bharat ka itihaas purana hai"
                style="width:100%;border:1.5px solid #d1d1d6;border-radius:10px;padding:12px 14px;
                font-size:15px;font-family:'Inter',sans-serif;background:#fff;outline:none;
                box-sizing:border-box;transition:border 0.2s;"
                onfocus="this.style.borderColor='#5e5ce6';this.style.boxShadow='0 0 0 3px rgba(94,92,230,0.1)'"
                onblur="this.style.borderColor='#d1d1d6';this.style.boxShadow='none'"
                oninput="T()" onkeydown="K(event)"/>
            <div id="ch" style="display:none;margin-top:6px;display:flex;gap:5px;flex-wrap:wrap;"></div>
        </div>
        <div style="background:#f5f5f7;border-radius:10px;padding:12px 14px;min-height:44px;
            font-size:16px;font-family:'Noto Sans Devanagari','Inter',sans-serif;color:#1d1d1f;
            line-height:1.7;letter-spacing:0.2px;" id="out">
            <span style="color:#c7c7cc">Hindi appears here…</span>
        </div>
        <div style="display:flex;gap:6px;margin-top:10px;align-items:center;">
            <button onclick="C()" style="background:#5e5ce6;color:#fff;border:none;border-radius:8px;
                padding:7px 16px;cursor:pointer;font-weight:600;font-size:12px;font-family:'Inter',sans-serif;">
                Copy text</button>
            <button onclick="U()" style="background:#fff;color:#636366;border:1px solid #d1d1d6;border-radius:8px;
                padding:7px 14px;cursor:pointer;font-size:12px;font-family:'Inter',sans-serif;">Undo</button>
            <button onclick="X()" style="background:#fff;color:#636366;border:1px solid #d1d1d6;border-radius:8px;
                padding:7px 14px;cursor:pointer;font-size:12px;font-family:'Inter',sans-serif;">Clear</button>
            <span id="st" style="font-size:11px;color:#34c759;font-weight:600;margin-left:6px;"></span>
        </div>
    </div>
    <script>
    var W=[],S=[],I=-1,tm;
    function T(){var v=document.getElementById('hi').value.split(' '),w=v[v.length-1];
    if(w.length>=1){clearTimeout(tm);tm=setTimeout(()=>F(w),120)}else H()}
    function K(e){if((e.key===' '||e.key==='Enter')&&S.length>0){e.preventDefault();
    A(I>=0?S[I]:S[0])}else if(e.key==='ArrowRight'&&S.length){e.preventDefault();
    I=Math.min(I+1,S.length-1);R()}else if(e.key==='ArrowLeft'&&S.length){e.preventDefault();
    I=Math.max(I-1,0);R()}else if(e.key==='Backspace'&&document.getElementById('hi').value===''&&W.length){
    e.preventDefault();U()}}
    async function F(w){try{var r=await fetch('https://inputtools.google.com/request?text='+
    encodeURIComponent(w)+'&itc=hi-t-i0-und&num=5&cp=0&cs=1&ie=utf-8&oe=utf-8&app=demopage');
    var d=await r.json();if(d&&d[0]==='SUCCESS'&&d[1]&&d[1][0]&&d[1][0][1]){S=d[1][0][1];I=0;R()}
    else H()}catch(e){H()}}
    function R(){var b=document.getElementById('ch');if(!S.length){b.style.display='none';return}
    b.style.display='flex';b.innerHTML=S.map((w,i)=>'<span onclick="A(S['+i+'])" style="'+
    'padding:5px 12px;border-radius:8px;cursor:pointer;font-size:14px;'+
    'font-family:Noto Sans Devanagari,sans-serif;transition:all 0.15s;'+
    (i===I?'background:#5e5ce6;color:#fff;':'background:#fff;color:#1d1d1f;border:1px solid #d1d1d6;')+
    '">'+w+'</span>').join('')}
    function A(w){W.push(w);D();document.getElementById('hi').value='';
    document.getElementById('hi').focus();S=[];I=-1;H()}
    function U(){if(W.length){W.pop();D()}}
    function D(){var o=document.getElementById('out');
    o.innerHTML=W.length?W.join(' '):"<span style='color:#c7c7cc'>Hindi appears here…</span>"}
    function H(){document.getElementById('ch').style.display='none';S=[];I=-1}
    function C(){if(!W.length)return;navigator.clipboard.writeText(W.join(' ')).then(()=>{
    document.getElementById('st').innerText='Copied!';
    setTimeout(()=>document.getElementById('st').innerText='',2500)})}
    function X(){W=[];S=[];I=-1;document.getElementById('hi').value='';D();H()}
    </script>""", height=230, scrolling=False)

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 0 — Upload
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.step == 0:
    st.markdown("#### Upload handwritten pages")
    st.caption("Upload clear photos of your question paper. 1–5 images, JPG or PNG.")
    files = st.file_uploader("Upload images", type=["jpg","jpeg","png"], accept_multiple_files=True, label_visibility="collapsed")
    if files:
        files = files[:5]
        cols = st.columns(min(len(files),5))
        for i,(c,f) in enumerate(zip(cols,files)):
            with c: st.image(f, caption=f"Page {i+1}", use_container_width=True)
        st.session_state.uploaded_files = files
        if st.button("Continue", type="primary", use_container_width=True):
            st.session_state.step = 1; st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Details
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 1:
    st.markdown("#### School and exam details")
    st.caption("Optional. Leave blank if already written on the paper.")
    c1, c2 = st.columns(2)
    with c1:
        sn = st.text_input("School name", value=st.session_state.get("school_name",""))
        cn = st.text_input("Class", value=st.session_state.get("class_name",""))
    with c2:
        su = st.text_input("Subject", value=st.session_state.get("subject",""))
        logo = st.file_uploader("School logo", type=["jpg","jpeg","png"])
    st.session_state.school_name = sn; st.session_state.class_name = cn; st.session_state.subject = su
    if logo: st.session_state.logo_file = logo
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Back", use_container_width=True): st.session_state.step = 0; st.rerun()
    with c2:
        if st.button("Generate", type="primary", use_container_width=True):
            if not api_key: st.error("Enter your OpenAI API key in the sidebar.")
            elif not getattr(st.session_state,'uploaded_files',None): st.error("Upload images first.")
            else: st.session_state.step = 2; st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Processing
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.markdown("#### Reading your paper…")
    from ocr import process_images_to_structured
    prog = st.progress(0); stat = st.empty()
    try:
        stat.caption("Preparing images…"); prog.progress(10)
        td = tempfile.mkdtemp(); paths = []
        for i,f in enumerate(st.session_state.uploaded_files):
            p = os.path.join(td,f"page_{i+1}.{f.name.split('.')[-1]}")
            with open(p,'wb') as fh: fh.write(f.getbuffer())
            paths.append(p)
        stat.caption("Extracting text with GPT-4o Vision…"); prog.progress(25)
        data, raw = process_images_to_structured(paths, api_key, model_name=model_choice)
        prog.progress(80)
        if st.session_state.get("class_name"): data["class"] = st.session_state.class_name
        if st.session_state.get("subject"): data["subject"] = st.session_state.subject
        st.session_state.structured_data = data; st.session_state.raw_text = raw
        prog.progress(100); st.session_state.step = 3; st.rerun()
    except Exception as e:
        prog.progress(0); stat.empty(); st.error(f"Something went wrong: {e}")
        if st.button("Try again", use_container_width=True): st.session_state.step = 1; st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Edit & Fix
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    data = st.session_state.structured_data
    if not data:
        st.error("No data found.")
        if st.button("Back"): st.session_state.step = 1; st.rerun()
    else:
        st.markdown("#### Review and edit")
        st.caption("Fix any mistakes. Refresh the preview after making changes.")

        ed, pv = st.columns([3, 2], gap="medium")

        with ed:
            # ── Details ──
            c1,c2 = st.columns(2)
            with c1:
                data["exam_title"] = st.text_input("Exam title", value=data.get("exam_title",""), key="e_t")
                data["class"] = st.text_input("Class", value=data.get("class",""), key="e_c")
                data["subject"] = st.text_input("Subject", value=data.get("subject",""), key="e_s")
            with c2:
                data["time"] = st.text_input("Time", value=data.get("time",""), key="e_tm")
                data["total_marks"] = st.text_input("Total marks", value=data.get("total_marks",""), key="e_mk")

            # ── Instructions ──
            st.markdown("###### Instructions")
            it = st.text_area("i", value="\n".join(data.get("instructions",[])), height=90, key="e_i", label_visibility="collapsed")
            data["instructions"] = [l.strip() for l in it.split("\n") if l.strip()]

            # ── Hindi Tool ──
            with st.expander("Hindi typing tool", expanded=False):
                hindi_tool()

            # ── Sections ──
            st.markdown("###### Sections and questions")
            sections = data.get("sections",[]); sdel = []
            for si,sec in enumerate(sections):
                st.markdown(f'<div class="pp-sec">{sec.get("section_name",f"Section {si+1}")}</div>', unsafe_allow_html=True)
                sc1,sc2 = st.columns([5,1])
                with sc1:
                    sec["section_name"] = st.text_input(f"s{si}", value=sec.get("section_name",""),
                        key=f"sn_{si}", label_visibility="collapsed", placeholder="Section name")
                with sc2:
                    if st.button("Delete", key=f"ds_{si}"): sdel.append(si)

                qs = sec.get("questions",[]); qdel = []
                for qi,q in enumerate(qs):
                    st.markdown('<div class="pp-qcard">', unsafe_allow_html=True)
                    r1,r2,r3 = st.columns([1.2,1.2,1])
                    with r1: q["number"] = st.text_input("Q#", value=q.get("number",""), key=f"qn_{si}_{qi}")
                    with r2: q["marks"] = st.text_input("Marks", value=q.get("marks",""), key=f"qm_{si}_{qi}")
                    with r3:
                        st.write("")
                        if st.button(f"Delete Q{q.get('number','')}", key=f"dq_{si}_{qi}"): qdel.append(qi)
                    q["text"] = st.text_area(f"q{si}{qi}", value=q.get("text",""), key=f"qt_{si}_{qi}",
                        height=70, label_visibility="collapsed", placeholder="Question text…")
                    subs = q.get("subparts",[])
                    if subs:
                        st.caption("One option per line. For match-the-following use Tab between columns.")
                        sv = st.text_area(f"sp{si}{qi}", value="\n".join(subs), key=f"qs_{si}_{qi}",
                            height=max(45,min(len(subs)*24,150)), label_visibility="collapsed")
                        q["subparts"] = [l for l in sv.split("\n") if l.strip()]
                        if st.button("Remove options", key=f"rs_{si}_{qi}"): q["subparts"]=[]; st.rerun()
                    else:
                        if st.button("Add options", key=f"as_{si}_{qi}"):
                            q["subparts"]=["(a) ","(b) ","(c) ","(d) "]; st.rerun()

                    # ── Image attachment ──
                    img_key = f"qimg_{si}_{qi}"
                    state_img_key = f"img_{si}_{qi}"
                    has_img = st.session_state.get(state_img_key) is not None
                    
                    ic1, ic2 = st.columns([3, 1])
                    with ic1:
                        img_file = st.file_uploader(
                            f"Attach diagram/image", 
                            type=["jpg","jpeg","png"],
                            key=img_key,
                            label_visibility="collapsed",
                            help="Attach a photo of diagram, graph, map, or figure for this question"
                        )
                        if img_file:
                            st.session_state[state_img_key] = img_file.getvalue()
                        if not has_img:
                            st.caption("Tip: Crop the image on your phone before uploading for best fit.")
                        if img_file:
                            st.session_state[state_img_key] = img_file.getvalue()
                    with ic2:
                        if has_img:
                            st.image(st.session_state[state_img_key], width=80)
                            if st.button("✕", key=f"rmimg_{si}_{qi}", help="Remove image"):
                                st.session_state[state_img_key] = None; st.rerun()
                        else:
                            st.caption("📎 No image")
                    st.markdown('</div>', unsafe_allow_html=True)
                for qi in sorted(qdel, reverse=True): qs.pop(qi)
                if qdel: st.rerun()
                if st.button("Add question", key=f"aq_{si}"):
                    n = str(int(qs[-1]["number"])+1) if qs and qs[-1].get("number","").isdigit() else str(len(qs)+1)
                    qs.append({"number":n,"text":"","marks":"","subparts":[]}); st.rerun()

            for si in sorted(sdel, reverse=True): sections.pop(si)
            if sdel: st.rerun()
            if st.button("Add section"):
                sections.append({"section_name":f"Section {chr(65+len(sections))}","questions":[]}); st.rerun()
            data["sections"] = sections; st.session_state.structured_data = data

        with pv:
            st.markdown("###### Preview")
            if st.button("Refresh preview", use_container_width=True): st.rerun()
            st.markdown(render_preview(data), unsafe_allow_html=True)

        st.markdown("---")
        c1,c2 = st.columns(2)
        with c1:
            if st.button("Back", use_container_width=True, key="bb"): st.session_state.step = 1; st.rerun()
        with c2:
            if st.button("Generate document", type="primary", use_container_width=True):
                try: generate_docx(data); st.session_state.step = 4; st.rerun()
                except Exception as e: st.error(f"Error: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4 — Download
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    st.markdown("""
    <div class="pp-success">
        <div class="pp-success-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none"><path d="M5 13l4 4L19 7" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <h2>Your paper is ready</h2>
        <p>Download the formatted document below.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.docx_path and os.path.exists(st.session_state.docx_path):
        with open(st.session_state.docx_path,"rb") as f: db = f.read()
        fn = st.session_state.get("docx_filename","Question_Paper.docx")
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            st.download_button(f"Download {fn}", data=db, file_name=fn,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True, type="primary")
        st.markdown("---")
        st.markdown("###### Preview")
        st.markdown(render_preview(st.session_state.structured_data), unsafe_allow_html=True)
        st.markdown("---")
        c1,c2 = st.columns(2)
        with c1:
            if st.button("Back to edit", use_container_width=True): st.session_state.step = 3; st.rerun()
        with c2:
            if st.button("New paper", type="primary", use_container_width=True):
                for k in defaults: st.session_state[k] = defaults[k]
                st.rerun()
    else:
        st.error("File not found.")
        if st.button("Back"): st.session_state.step = 3; st.rerun()
