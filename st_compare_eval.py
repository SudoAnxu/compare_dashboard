import streamlit as st
import json
import sqlparse

# Load JSON files
with open("evaluation_results_base.json", encoding="utf-8") as f1:
    base = json.load(f1)

with open("evaluation_results_loop.json", encoding="utf-8") as f2:
    loop = json.load(f2)

# Index by question for fast lookup
base_dict = {item["question"]: item for item in base}
loop_dict = {item["question"]: item for item in loop}

# Find common questions
common_questions = sorted(set(base_dict) & set(loop_dict))

# Streamlit UI
st.title("🧠 SQL Evaluation Comparative Dashboard")
st.write("Compare results between two evaluation runs for the same set of queries.")

# Filter for queries with score difference
show_diff_only = st.checkbox("Show only queries with different scores")
if show_diff_only:
    common_questions = [
        q for q in common_questions
        if base_dict[q].get("score") != loop_dict[q].get("score")
    ]

query = st.selectbox("📌 Select a query to compare:", common_questions)

# Split into columns
col1, col2 = st.columns(2)

with col1:
    st.header("📘 Base Evaluation")
    item = base_dict[query]

    st.markdown(f"**Score:** `{item.get('score')}`")
    st.markdown(f"**Explanation:**\n\n{item.get('explanation', '')}")

    st.markdown("**Generated SQL:**")
    with st.expander("Show Generated SQL", expanded=True):
        gen_sql = item.get("generated_sql")
        if gen_sql:
            formatted_sql = sqlparse.format(gen_sql, reindent=True, keyword_case="upper")
            st.code(formatted_sql, language="sql")
        else:
            st.warning("⚠️ No generated SQL found.")

    st.markdown("**Ground Truth SQL:**")
    with st.expander("Show Ground Truth SQL", expanded=True):
        gt_sql = item.get("ground_truth_sql")
        if gt_sql:
            formatted_gt_sql = sqlparse.format(gt_sql, reindent=True, keyword_case="upper")
            st.code(formatted_gt_sql, language="sql")
        else:
            st.warning("⚠️ No ground truth SQL found.")

with col2:
    st.header("🔁 Loop Evaluation")
    item = loop_dict[query]

    st.markdown(f"**Score:** `{item.get('score')}`")
    st.markdown(f"**Explanation:**\n\n{item.get('explanation', '')}")

    st.markdown("**Generated SQL:**")
    with st.expander("Show Generated SQL", expanded=True):
        gen_sql = item.get("generated_sql")
        if gen_sql:
            formatted_sql = sqlparse.format(gen_sql, reindent=True, keyword_case="upper")
            st.code(formatted_sql, language="sql")
        else:
            st.warning("⚠️ No generated SQL found.")

    st.markdown("**Ground Truth SQL:**")
    with st.expander("Show Ground Truth SQL", expanded=True):
        gt_sql = item.get("ground_truth_sql")
        if gt_sql:
            formatted_gt_sql = sqlparse.format(gt_sql, reindent=True, keyword_case="upper")
            st.code(formatted_gt_sql, language="sql")
        else:
            st.warning("⚠️ No ground truth SQL found.")

# Show score difference
score1 = base_dict[query].get("score")
score2 = loop_dict[query].get("score")

if score1 is not None and score2 is not None:
    diff = round(score2 - score1, 3)
    st.info(f"📊 **Score Difference:** `{score2}` (loop) - `{score1}` (base) = **{diff}**")
